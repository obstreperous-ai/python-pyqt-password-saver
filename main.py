"""Main entry point for the Password Saver application."""

import sys
from pathlib import Path
from typing import Optional

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QInputDialog,
)
from PyQt6.QtCore import Qt

from storage import PasswordStorage


class MasterPasswordDialog(QDialog):
    """Dialog for entering the master password."""

    def __init__(self, parent: Optional[QMainWindow] = None):
        super().__init__(parent)
        self.setWindowTitle("Master Password")
        self.setModal(True)
        self.password = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the dialog UI."""
        layout = QVBoxLayout()

        # Info label
        info_label = QLabel("Enter your master password to unlock the password manager:")
        layout.addWidget(info_label)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.accept)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.password_input.setFocus()

    def get_password(self) -> str:
        """Get the entered password."""
        return self.password_input.text()


class AddPasswordDialog(QDialog):
    """Dialog for adding a new password."""

    def __init__(self, parent: Optional[QMainWindow] = None):
        super().__init__(parent)
        self.setWindowTitle("Add Password")
        self.setModal(True)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the dialog UI."""
        layout = QVBoxLayout()

        # Service
        layout.addWidget(QLabel("Service/Website:"))
        self.service_input = QLineEdit()
        layout.addWidget(self.service_input)

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Notes
        layout.addWidget(QLabel("Notes (optional):"))
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(self.notes_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self) -> tuple[str, str, str, str]:
        """Get the entered data."""
        return (
            self.service_input.text(),
            self.username_input.text(),
            self.password_input.text(),
            self.notes_input.toPlainText(),
        )


class ViewPasswordDialog(QDialog):
    """Dialog for viewing password details."""

    def __init__(self, service: str, data: dict, parent: Optional[QMainWindow] = None):
        super().__init__(parent)
        self.setWindowTitle(f"Password Details - {service}")
        self.setModal(True)
        self._setup_ui(service, data)

    def _setup_ui(self, service: str, data: dict) -> None:
        """Setup the dialog UI."""
        layout = QVBoxLayout()

        # Service
        layout.addWidget(QLabel(f"<b>Service:</b> {service}"))

        # Username
        layout.addWidget(QLabel(f"<b>Username:</b> {data.get('username', 'N/A')}"))

        # Password (with show/hide)
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("<b>Password:</b>"))
        self.password_label = QLabel("********")
        self.password_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        password_layout.addWidget(self.password_label)
        
        self.show_button = QPushButton("Show")
        self.show_button.clicked.connect(lambda: self._toggle_password(data.get('password', '')))
        password_layout.addWidget(self.show_button)
        layout.addLayout(password_layout)

        # Notes
        if data.get('notes'):
            layout.addWidget(QLabel("<b>Notes:</b>"))
            notes_display = QTextEdit()
            notes_display.setPlainText(data['notes'])
            notes_display.setReadOnly(True)
            notes_display.setMaximumHeight(100)
            layout.addWidget(notes_display)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.password_visible = False

    def _toggle_password(self, password: str) -> None:
        """Toggle password visibility."""
        if self.password_visible:
            self.password_label.setText("********")
            self.show_button.setText("Show")
        else:
            self.password_label.setText(password)
            self.show_button.setText("Hide")
        self.password_visible = not self.password_visible


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.storage: Optional[PasswordStorage] = None
        self._load_ui()
        self._connect_signals()
        self._initialize_storage()
        self._refresh_list()

    def _load_ui(self) -> None:
        """Load the UI from .ui file."""
        ui_file = Path(__file__).parent / "ui" / "mainwindow.ui"
        uic.loadUi(ui_file, self)

    def _connect_signals(self) -> None:
        """Connect UI signals to slots."""
        self.addButton.clicked.connect(self._add_password)
        self.viewButton.clicked.connect(self._view_password)
        self.deleteButton.clicked.connect(self._delete_password)
        self.exitButton.clicked.connect(self.close)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self._show_about)
        self.serviceListWidget.itemDoubleClicked.connect(self._view_password)

    def _initialize_storage(self) -> None:
        """Initialize the password storage with master password."""
        while True:
            dialog = MasterPasswordDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                master_password = dialog.get_password()
                if master_password:
                    try:
                        self.storage = PasswordStorage()
                        self.storage.initialize_master_key(master_password)
                        # Test if we can load passwords (validates the password)
                        self.storage.load_passwords()
                        self.statusbar.showMessage("Password manager unlocked", 3000)
                        break
                    except ValueError as e:
                        QMessageBox.critical(
                            self,
                            "Error",
                            f"Failed to unlock password manager: {e}\n\n"
                            "If this is your first time, any password will create a new vault.",
                        )
                    except (OSError, IOError) as e:
                        QMessageBox.critical(
                            self,
                            "Error",
                            f"Failed to access password storage: {e}",
                        )
                else:
                    QMessageBox.warning(self, "Warning", "Master password cannot be empty")
            else:
                # User cancelled
                sys.exit(0)

    def _refresh_list(self) -> None:
        """Refresh the service list."""
        if self.storage is None:
            return

        self.serviceListWidget.clear()
        services = self.storage.list_services()
        self.serviceListWidget.addItems(services)
        self.statusbar.showMessage(f"{len(services)} password(s) stored", 3000)

    def _add_password(self) -> None:
        """Add a new password."""
        dialog = AddPasswordDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            service, username, password, notes = dialog.get_data()
            
            if not service or not username or not password:
                QMessageBox.warning(
                    self, "Warning", "Service, username, and password are required"
                )
                return

            try:
                self.storage.add_password(service, username, password, notes)
                self._refresh_list()
                QMessageBox.information(
                    self, "Success", f"Password for '{service}' saved successfully"
                )
            except ValueError as e:
                QMessageBox.critical(self, "Error", f"Failed to save password: {e}")
            except (OSError, IOError) as e:
                QMessageBox.critical(self, "Error", f"Failed to write password file: {e}")

    def _view_password(self) -> None:
        """View the selected password."""
        current_item = self.serviceListWidget.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a service to view")
            return

        service = current_item.text()
        try:
            data = self.storage.get_password(service)
            if data:
                dialog = ViewPasswordDialog(service, data, self)
                dialog.exec()
            else:
                QMessageBox.warning(self, "Warning", f"Password for '{service}' not found")
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Failed to load password: {e}")
        except (OSError, IOError) as e:
            QMessageBox.critical(self, "Error", f"Failed to read password file: {e}")

    def _delete_password(self) -> None:
        """Delete the selected password."""
        current_item = self.serviceListWidget.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a service to delete")
            return

        service = current_item.text()
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the password for '{service}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.storage.delete_password(service):
                    self._refresh_list()
                    QMessageBox.information(
                        self, "Success", f"Password for '{service}' deleted successfully"
                    )
                else:
                    QMessageBox.warning(self, "Warning", f"Password for '{service}' not found")
            except ValueError as e:
                QMessageBox.critical(self, "Error", f"Failed to delete password: {e}")
            except (OSError, IOError) as e:
                QMessageBox.critical(self, "Error", f"Failed to update password file: {e}")

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Password Saver",
            "<h2>Password Saver</h2>"
            "<p>A secure, cross-platform desktop password manager built with PyQt6.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>AES-256 encryption for password storage</li>"
            "<li>OS keyring integration for master key</li>"
            "<li>Cross-platform support (macOS, Linux)</li>"
            "</ul>"
            "<p>Version 0.1.0</p>",
        )


def main() -> None:
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Password Saver")
    app.setOrganizationName("PyQt Password Saver")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
