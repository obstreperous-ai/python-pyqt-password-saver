"""Storage module for secure password management with AES encryption."""

import base64
import json
import os
from pathlib import Path
from typing import Any, Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import keyring


class PasswordStorage:
    """Manages encrypted storage of passwords on disk."""

    SERVICE_NAME = "PyQtPasswordSaver"
    MASTER_KEY_ID = "master_encryption_key"
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize password storage.
        
        Args:
            data_dir: Directory to store encrypted password file. 
                     Defaults to ~/.password_saver/
        """
        if data_dir is None:
            data_dir = Path.home() / ".password_saver"
        
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "passwords.enc"
        self._master_key: Optional[bytes] = None
    
    def initialize_master_key(self, password: str) -> None:
        """Initialize or retrieve the master encryption key.
        
        Args:
            password: Master password to derive encryption key from
        """
        # Try to get existing salt from keyring
        stored_salt = keyring.get_password(self.SERVICE_NAME, "salt")
        
        if stored_salt:
            salt = base64.b64decode(stored_salt)
        else:
            # Generate new salt and store it
            salt = os.urandom(16)
            keyring.set_password(self.SERVICE_NAME, "salt", base64.b64encode(salt).decode())
        
        # Derive key from password using PBKDF2
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        self._master_key = kdf.derive(password.encode())
    
    def _encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data using AES-256-CBC.
        
        Args:
            data: Raw bytes to encrypt
            
        Returns:
            Encrypted bytes with IV prepended
        """
        if self._master_key is None:
            raise ValueError("Master key not initialized")
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Pad data to block size (16 bytes for AES)
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length] * padding_length)
        
        # Encrypt
        cipher = Cipher(
            algorithms.AES(self._master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Prepend IV to encrypted data
        return iv + encrypted_data
    
    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt AES-256-CBC encrypted data.
        
        Args:
            encrypted_data: Encrypted bytes with IV prepended
            
        Returns:
            Decrypted raw bytes
        """
        if self._master_key is None:
            raise ValueError("Master key not initialized")
        
        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(self._master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_data[-1]
        data = padded_data[:-padding_length]
        
        return data
    
    def save_passwords(self, passwords: dict[str, dict[str, Any]]) -> None:
        """Save passwords to encrypted file.
        
        Args:
            passwords: Dictionary mapping service names to password data
        """
        # Convert to JSON
        json_data = json.dumps(passwords, indent=2)
        
        # Encrypt and save
        encrypted_data = self._encrypt_data(json_data.encode())
        self.data_file.write_bytes(encrypted_data)
    
    def load_passwords(self) -> dict[str, dict[str, Any]]:
        """Load passwords from encrypted file.
        
        Returns:
            Dictionary mapping service names to password data
        """
        if not self.data_file.exists():
            return {}
        
        try:
            # Load and decrypt
            encrypted_data = self.data_file.read_bytes()
            decrypted_data = self._decrypt_data(encrypted_data)
            
            # Parse JSON
            return json.loads(decrypted_data.decode())
        except Exception as e:
            raise ValueError(f"Failed to load passwords: {e}")
    
    def add_password(
        self, 
        service: str, 
        username: str, 
        password: str, 
        notes: str = ""
    ) -> None:
        """Add or update a password entry.
        
        Args:
            service: Service/website name
            username: Username for the service
            password: Password to store
            notes: Optional notes
        """
        passwords = self.load_passwords()
        passwords[service] = {
            "username": username,
            "password": password,
            "notes": notes
        }
        self.save_passwords(passwords)
    
    def get_password(self, service: str) -> Optional[dict[str, Any]]:
        """Retrieve password entry for a service.
        
        Args:
            service: Service/website name
            
        Returns:
            Dictionary with username, password, and notes, or None if not found
        """
        passwords = self.load_passwords()
        return passwords.get(service)
    
    def delete_password(self, service: str) -> bool:
        """Delete a password entry.
        
        Args:
            service: Service/website name
            
        Returns:
            True if deleted, False if not found
        """
        passwords = self.load_passwords()
        if service in passwords:
            del passwords[service]
            self.save_passwords(passwords)
            return True
        return False
    
    def list_services(self) -> list[str]:
        """Get list of all stored services.
        
        Returns:
            List of service names
        """
        passwords = self.load_passwords()
        return sorted(passwords.keys())
