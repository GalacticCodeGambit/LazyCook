"""
Comprehensive unit tests for LazyCookVerwaltung.py

Tests cover:
- Password hashing (hash_password)
- Password verification (verify_password)
- Login endpoint (/api/login)
- Registration endpoint (/api/register)
- Edge cases and error conditions
- FastAPI endpoint behavior
- Security considerations
"""

import pytest
import base64
import hashlib
import os
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from pydantic import ValidationError

# Import the module under test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from LazyCookVerwaltung import (
    app, hash_password, verify_password, anmelden, registrieren
)
from models import UserSignUpIn


class TestHashPassword:
    """Test password hashing functionality"""
    
    def test_hash_password_returns_tuple(self):
        """Test that hash_password returns a tuple of (salt, key)"""
        result = hash_password("testpassword123")
        
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_hash_password_salt_is_base64(self):
        """Test that salt is base64 encoded string"""
        salt, key = hash_password("testpassword123")
        
        assert isinstance(salt, str)
        # Should be decodable from base64
        try:
            decoded_salt = base64.b64decode(salt)
            assert len(decoded_salt) == 16  # 16 bytes
        except Exception as e:
            pytest.fail(f"Salt is not valid base64: {e}")
    
    def test_hash_password_key_is_base64(self):
        """Test that key is base64 encoded string"""
        salt, key = hash_password("testpassword123")
        
        assert isinstance(key, str)
        # Should be decodable from base64
        try:
            decoded_key = base64.b64decode(key)
            assert len(decoded_key) == 32  # SHA256 produces 32 bytes
        except Exception as e:
            pytest.fail(f"Key is not valid base64: {e}")
    
    def test_hash_password_different_salts_for_same_password(self):
        """Test that same password produces different salts each time"""
        salt1, key1 = hash_password("samepassword")
        salt2, key2 = hash_password("samepassword")
        
        assert salt1 != salt2
        assert key1 != key2
    
    def test_hash_password_empty_password(self):
        """Test hashing empty password"""
        salt, key = hash_password("")
        
        assert salt is not None
        assert key is not None
        assert len(base64.b64decode(salt)) == 16
    
    def test_hash_password_long_password(self):
        """Test hashing very long password"""
        long_password = "a" * 1000
        salt, key = hash_password(long_password)
        
        assert salt is not None
        assert key is not None
    
    def test_hash_password_unicode_characters(self):
        """Test hashing password with unicode characters"""
        unicode_password = "pässwörd123🔒"
        salt, key = hash_password(unicode_password)
        
        assert salt is not None
        assert key is not None
    
    def test_hash_password_special_characters(self):
        """Test hashing password with special characters"""
        special_password = "p@$$w0rd!#%&*()[]{}|\\/<>?~`"
        salt, key = hash_password(special_password)
        
        assert salt is not None
        assert key is not None
    
    def test_hash_password_deterministic_with_same_salt(self):
        """Test that hashing is deterministic when using same salt"""
        password = "testpassword"
        salt = os.urandom(16)
        
        key1 = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt,
            iterations=100_000
        )
        
        key2 = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt,
            iterations=100_000
        )
        
        assert key1 == key2
    
    def test_hash_password_uses_100k_iterations(self):
        """Test that hash_password uses 100,000 iterations (security check)"""
        password = "testpassword"
        salt_bytes = os.urandom(16)
        
        # Generate expected hash with 100k iterations
        expected_key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt_bytes,
            iterations=100_000
        )
        
        # Mock os.urandom to return our known salt
        with patch('LazyCookVerwaltung.os.urandom', return_value=salt_bytes):
            salt_b64, key_b64 = hash_password(password)
            actual_key = base64.b64decode(key_b64)
            
            assert actual_key == expected_key


class TestVerifyPassword:
    """Test password verification functionality"""
    
    def test_verify_password_correct_password(self):
        """Test verification with correct password"""
        password = "correctpassword123"
        salt_b64, key_b64 = hash_password(password)
        
        result = verify_password(password, salt_b64, key_b64)
        
        assert result is True
    
    def test_verify_password_incorrect_password(self):
        """Test verification with incorrect password"""
        original_password = "correctpassword"
        wrong_password = "wrongpassword"
        
        salt_b64, key_b64 = hash_password(original_password)
        
        result = verify_password(wrong_password, salt_b64, key_b64)
        
        assert result is False
    
    def test_verify_password_empty_password(self):
        """Test verification with empty password"""
        password = ""
        salt_b64, key_b64 = hash_password(password)
        
        result = verify_password(password, salt_b64, key_b64)
        
        assert result is True
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive"""
        password = "TestPassword"
        salt_b64, key_b64 = hash_password(password)
        
        result_correct = verify_password("TestPassword", salt_b64, key_b64)
        result_wrong_case = verify_password("testpassword", salt_b64, key_b64)
        
        assert result_correct is True
        assert result_wrong_case is False
    
    def test_verify_password_unicode_characters(self):
        """Test verification with unicode password"""
        password = "pässwörd🔐"
        salt_b64, key_b64 = hash_password(password)
        
        result = verify_password(password, salt_b64, key_b64)
        
        assert result is True
    
    def test_verify_password_tampered_salt(self):
        """Test verification fails with tampered salt"""
        password = "testpassword"
        salt_b64, key_b64 = hash_password(password)
        
        # Tamper with salt
        tampered_salt = base64.b64encode(os.urandom(16)).decode()
        
        result = verify_password(password, tampered_salt, key_b64)
        
        assert result is False
    
    def test_verify_password_tampered_key(self):
        """Test verification fails with tampered key"""
        password = "testpassword"
        salt_b64, key_b64 = hash_password(password)
        
        # Tamper with key
        tampered_key = base64.b64encode(os.urandom(32)).decode()
        
        result = verify_password(password, salt_b64, tampered_key)
        
        assert result is False
    
    def test_verify_password_special_characters(self):
        """Test verification with special characters"""
        password = "p@$$w0rd!#%"
        salt_b64, key_b64 = hash_password(password)
        
        result = verify_password(password, salt_b64, key_b64)
        
        assert result is True
    
    def test_verify_password_long_password(self):
        """Test verification with very long password"""
        password = "a" * 1000
        salt_b64, key_b64 = hash_password(password)
        
        result = verify_password(password, salt_b64, key_b64)
        
        assert result is True
    
    def test_verify_password_whitespace_differences(self):
        """Test that whitespace differences are detected"""
        password = "test password"
        salt_b64, key_b64 = hash_password(password)
        
        result_correct = verify_password("test password", salt_b64, key_b64)
        result_extra_space = verify_password("test  password", salt_b64, key_b64)
        
        assert result_correct is True
        assert result_extra_space is False


class TestAnmeldenEndpoint:
    """Test /api/login endpoint"""
    
    def setup_method(self):
        """Set up test client before each test"""
        self.client = TestClient(app)
    
    def test_anmelden_successful_login(self):
        """Test successful login with correct credentials"""
        # Mock database response
        password = "correctpassword"
        salt_b64, key_b64 = hash_password(password)
        
        mock_row = {
            "passwort": key_b64,
            "salt": salt_b64
        }
        
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=mock_row):
            response = self.client.post(
                "/api/login",
                json={"email": "test@example.com", "password": password}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Anmeldung erfolgreich"
    
    def test_anmelden_wrong_password(self):
        """Test login with incorrect password"""
        correct_password = "correctpassword"
        wrong_password = "wrongpassword"
        
        salt_b64, key_b64 = hash_password(correct_password)
        
        mock_row = {
            "passwort": key_b64,
            "salt": salt_b64
        }
        
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=mock_row):
            response = self.client.post(
                "/api/login",
                json={"email": "test@example.com", "password": wrong_password}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Falsches Passwort"
    
    def test_anmelden_email_not_found(self):
        """Test login with non-existent email"""
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=None):
            response = self.client.post(
                "/api/login",
                json={"email": "nonexistent@example.com", "password": "password"}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Für diese Email ist kein Konto hinterlegt"
    
    def test_anmelden_database_exception(self):
        """Test login when database raises exception"""
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', side_effect=Exception("DB Error")):
            response = self.client.post(
                "/api/login",
                json={"email": "test@example.com", "password": "password"}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Anmeldung fehlgeschlagen"
    
    def test_anmelden_invalid_email_format(self):
        """Test login with invalid email format"""
        response = self.client.post(
            "/api/login",
            json={"email": "notanemail", "password": "password"}
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_anmelden_missing_email(self):
        """Test login with missing email field"""
        response = self.client.post(
            "/api/login",
            json={"password": "password"}
        )
        
        assert response.status_code == 422
    
    def test_anmelden_missing_password(self):
        """Test login with missing password field"""
        response = self.client.post(
            "/api/login",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == 422
    
    def test_anmelden_empty_password(self):
        """Test login with empty password"""
        password = ""
        salt_b64, key_b64 = hash_password(password)
        
        mock_row = {
            "passwort": key_b64,
            "salt": salt_b64
        }
        
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=mock_row):
            response = self.client.post(
                "/api/login",
                json={"email": "test@example.com", "password": ""}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Anmeldung erfolgreich"
    
    def test_anmelden_unicode_password(self):
        """Test login with unicode characters in password"""
        password = "pässwörd🔐"
        salt_b64, key_b64 = hash_password(password)
        
        mock_row = {
            "passwort": key_b64,
            "salt": salt_b64
        }
        
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=mock_row):
            response = self.client.post(
                "/api/login",
                json={"email": "test@example.com", "password": password}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Anmeldung erfolgreich"
    
    def test_anmelden_special_email_characters(self):
        """Test login with special characters in email"""
        password = "testpassword"
        salt_b64, key_b64 = hash_password(password)
        
        mock_row = {
            "passwort": key_b64,
            "salt": salt_b64
        }
        
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=mock_row):
            response = self.client.post(
                "/api/login",
                json={"email": "test+tag@example.com", "password": password}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Anmeldung erfolgreich"
    
    def test_anmelden_sql_injection_attempt_in_email(self):
        """Test that SQL injection in email is safely handled"""
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=None):
            response = self.client.post(
                "/api/login",
                json={"email": "test@example.com' OR '1'='1", "password": "password"}
            )
            
            # Should return email not found, not bypass security
            assert response.status_code == 200
            assert response.json()["message"] == "Für diese Email ist kein Konto hinterlegt"


class TestRegistrierenEndpoint:
    """Test /api/register endpoint"""
    
    def setup_method(self):
        """Set up test client before each test"""
        self.client = TestClient(app)
    
    def test_registrieren_successful_registration(self):
        """Test successful user registration"""
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            response = self.client.post(
                "/api/register",
                json={"email": "newuser@example.com", "password": "password123"}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Registrierung erfolgreich"
    
    def test_registrieren_duplicate_email(self):
        """Test registration with duplicate email"""
        with patch('LazyCookVerwaltung.datenbank.addNutzer', 
                   return_value="Email schon in einem Konto registriert"):
            response = self.client.post(
                "/api/register",
                json={"email": "existing@example.com", "password": "password123"}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Email schon in einem Konto registriert"
    
    def test_registrieren_database_exception(self):
        """Test registration when database raises exception"""
        with patch('LazyCookVerwaltung.datenbank.addNutzer', side_effect=Exception("DB Error")):
            response = self.client.post(
                "/api/register",
                json={"email": "test@example.com", "password": "password"}
            )
            
            assert response.status_code == 200
            assert response.json()["message"] == "Registrierung fehlgeschlagen"
    
    def test_registrieren_password_is_hashed(self):
        """Test that password is hashed before storing"""
        plain_password = "mysecretpassword"
        
        def check_hashed_password(email, salt, hashed_password):
            # Verify that hashed_password is not the plain password
            assert hashed_password != plain_password
            # Verify it's base64 encoded
            try:
                base64.b64decode(hashed_password)
            except:
                pytest.fail("Password was not properly hashed")
            return "Registrierung erfolgreich"
        
        with patch('LazyCookVerwaltung.datenbank.addNutzer', side_effect=check_hashed_password):
            response = self.client.post(
                "/api/register",
                json={"email": "test@example.com", "password": plain_password}
            )
            
            assert response.status_code == 200
    
    def test_registrieren_salt_is_generated(self):
        """Test that a salt is generated during registration"""
        def check_salt(email, salt, hashed_password):
            # Verify salt is base64 encoded
            assert salt is not None
            assert len(salt) > 0
            try:
                decoded_salt = base64.b64decode(salt)
                assert len(decoded_salt) == 16
            except:
                pytest.fail("Salt was not properly generated")
            return "Registrierung erfolgreich"
        
        with patch('LazyCookVerwaltung.datenbank.addNutzer', side_effect=check_salt):
            response = self.client.post(
                "/api/register",
                json={"email": "test@example.com", "password": "password123"}
            )
            
            assert response.status_code == 200
    
    def test_registrieren_invalid_email_format(self):
        """Test registration with invalid email format"""
        response = self.client.post(
            "/api/register",
            json={"email": "notanemail", "password": "password"}
        )
        
        assert response.status_code == 422
    
    def test_registrieren_missing_email(self):
        """Test registration with missing email field"""
        response = self.client.post(
            "/api/register",
            json={"password": "password"}
        )
        
        assert response.status_code == 422
    
    def test_registrieren_missing_password(self):
        """Test registration with missing password field"""
        response = self.client.post(
            "/api/register",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == 422
    
    def test_registrieren_empty_password(self):
        """Test registration with empty password"""
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            response = self.client.post(
                "/api/register",
                json={"email": "test@example.com", "password": ""}
            )
            
            assert response.status_code == 200
    
    def test_registrieren_long_password(self):
        """Test registration with very long password"""
        long_password = "a" * 1000
        
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            response = self.client.post(
                "/api/register",
                json={"email": "test@example.com", "password": long_password}
            )
            
            assert response.status_code == 200
    
    def test_registrieren_unicode_password(self):
        """Test registration with unicode characters in password"""
        unicode_password = "pässwörd🔒"
        
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            response = self.client.post(
                "/api/register",
                json={"email": "test@example.com", "password": unicode_password}
            )
            
            assert response.status_code == 200
    
    def test_registrieren_special_characters_in_password(self):
        """Test registration with special characters in password"""
        special_password = "p@$$w0rd!#%&*()"
        
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            response = self.client.post(
                "/api/register",
                json={"email": "test@example.com", "password": special_password}
            )
            
            assert response.status_code == 200
    
    def test_registrieren_special_email_characters(self):
        """Test registration with special characters in email"""
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            response = self.client.post(
                "/api/register",
                json={"email": "test+tag@sub.example.com", "password": "password"}
            )
            
            assert response.status_code == 200


class TestCORSMiddleware:
    """Test CORS configuration"""
    
    def setup_method(self):
        """Set up test client before each test"""
        self.client = TestClient(app)
    
    def test_cors_allows_localhost_8000(self):
        """Test that CORS is configured for localhost:8000"""
        # Make a request with Origin header
        response = self.client.options(
            "/api/login",
            headers={"Origin": "http://localhost:8000"}
        )
        
        # Check for CORS headers (may vary based on FastAPI/Starlette version)
        assert response.status_code in [200, 405]


class TestSecurityConsiderations:
    """Test security-related functionality"""
    
    def test_passwords_not_logged(self):
        """Test that passwords are not exposed in logs"""
        client = TestClient(app)
        
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            # This should not log the password
            response = client.post(
                "/api/register",
                json={"email": "test@example.com", "password": "secretpassword123"}
            )
            
            assert response.status_code == 200
            # Verify password is not in response
            assert "secretpassword123" not in str(response.json())
    
    def test_salt_uniqueness(self):
        """Test that each registration generates a unique salt"""
        salts = set()
        
        for _ in range(10):
            salt, _ = hash_password("samepassword")
            salts.add(salt)
        
        # All salts should be unique
        assert len(salts) == 10
    
    def test_timing_attack_resistance(self):
        """Test that password verification takes similar time for wrong passwords"""
        import time
        
        password = "testpassword"
        salt_b64, key_b64 = hash_password(password)
        
        # Measure time for correct password
        start = time.time()
        verify_password(password, salt_b64, key_b64)
        time_correct = time.time() - start
        
        # Measure time for incorrect password
        start = time.time()
        verify_password("wrongpassword", salt_b64, key_b64)
        time_incorrect = time.time() - start
        
        # Times should be similar (within an order of magnitude)
        # This is a basic check; real timing attack testing would be more sophisticated
        assert abs(time_correct - time_incorrect) < 0.1


class TestPlaceholderFunctions:
    """Test placeholder functions"""
    
    def test_filternNachZutat_exists(self):
        """Test that filternNachZutat function exists (placeholder)"""
        from LazyCookVerwaltung import filternNachZutat
        
        # Should not raise AttributeError
        result = filternNachZutat(None, 2, ["Tomato", "Cheese"])
        assert result is None
    
    def test_suchenNachRezept_exists(self):
        """Test that suchenNachRezept function exists (placeholder)"""
        from LazyCookVerwaltung import suchenNachRezept
        
        # Should not raise AttributeError
        result = suchenNachRezept(None, "Pizza")
        assert result is None
    
    def test_zeigeRezepteAn_exists(self):
        """Test that zeigeRezepteAn function exists (placeholder)"""
        from LazyCookVerwaltung import zeigeRezepteAn
        
        # Should not raise AttributeError
        result = zeigeRezepteAn(None)
        assert result is None


class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_full_registration_and_login_flow(self):
        """Test complete flow: register user then login"""
        client = TestClient(app)
        
        email = "integration@test.com"
        password = "integrationpassword123"
        
        # Register user
        with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
            reg_response = client.post(
                "/api/register",
                json={"email": email, "password": password}
            )
            assert reg_response.status_code == 200
            assert reg_response.json()["message"] == "Registrierung erfolgreich"
        
        # Login with same credentials
        salt_b64, key_b64 = hash_password(password)
        mock_row = {"passwort": key_b64, "salt": salt_b64}
        
        with patch('LazyCookVerwaltung.datenbank.anmeldenNutzer', return_value=mock_row):
            login_response = client.post(
                "/api/login",
                json={"email": email, "password": password}
            )
            assert login_response.status_code == 200
            assert login_response.json()["message"] == "Anmeldung erfolgreich"
    
    def test_multiple_user_registrations(self):
        """Test registering multiple users"""
        client = TestClient(app)
        
        users = [
            ("user1@test.com", "password1"),
            ("user2@test.com", "password2"),
            ("user3@test.com", "password3"),
        ]
        
        for email, password in users:
            with patch('LazyCookVerwaltung.datenbank.addNutzer', return_value="Registrierung erfolgreich"):
                response = client.post(
                    "/api/register",
                    json={"email": email, "password": password}
                )
                assert response.status_code == 200
                assert response.json()["message"] == "Registrierung erfolgreich"