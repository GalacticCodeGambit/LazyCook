"""
Comprehensive unit tests for models.py

Tests cover:
- UserSignUpIn model validation
- UserResponse model validation
- SessionResponse model validation
- Email validation
- Field requirements
- Data integrity
"""

import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models import UserSignUpIn, UserResponse, SessionResponse


class TestUserSignUpIn:
    """Test UserSignUpIn model"""
    
    def test_valid_user_signup(self):
        """Test creating valid UserSignUpIn instance"""
        user = UserSignUpIn(
            email="test@example.com",
            password="securepassword123"
        )
        
        assert user.email == "test@example.com"
        assert user.password == "securepassword123"
    
    def test_valid_email_formats(self):
        """Test various valid email formats"""
        valid_emails = [
            "simple@example.com",
            "user+tag@example.com",
            "user.name@example.com",
            "user_name@example.com",
            "user-name@example.com",
            "123@example.com",
            "test@sub.example.com",
            "test@example.co.uk",
        ]
        
        for email in valid_emails:
            user = UserSignUpIn(email=email, password="password")
            assert user.email == email
    
    def test_invalid_email_format(self):
        """Test that invalid email formats raise validation error"""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user@@example.com",
            "user@.com",
            "user @example.com",
            "user@example",
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                UserSignUpIn(email=email, password="password")
    
    def test_missing_email(self):
        """Test that missing email raises validation error"""
        with pytest.raises(ValidationError):
            UserSignUpIn(password="password")
    
    def test_missing_password(self):
        """Test that missing password raises validation error"""
        with pytest.raises(ValidationError):
            UserSignUpIn(email="test@example.com")
    
    def test_empty_password_allowed(self):
        """Test that empty password is allowed (validation at business logic layer)"""
        user = UserSignUpIn(email="test@example.com", password="")
        assert user.password == ""
    
    def test_long_password(self):
        """Test that long passwords are accepted"""
        long_password = "a" * 1000
        user = UserSignUpIn(email="test@example.com", password=long_password)
        assert user.password == long_password
    
    def test_unicode_password(self):
        """Test that unicode characters in password are accepted"""
        unicode_password = "pässwörd🔒"
        user = UserSignUpIn(email="test@example.com", password=unicode_password)
        assert user.password == unicode_password
    
    def test_special_characters_in_password(self):
        """Test that special characters in password are accepted"""
        special_password = "p@$$w0rd!#%&*()[]{}|\\/<>?~`"
        user = UserSignUpIn(email="test@example.com", password=special_password)
        assert user.password == special_password
    
    def test_whitespace_in_password(self):
        """Test that whitespace in password is preserved"""
        password_with_spaces = "pass word with spaces"
        user = UserSignUpIn(email="test@example.com", password=password_with_spaces)
        assert user.password == password_with_spaces
    
    def test_model_dict_export(self):
        """Test exporting model to dictionary"""
        user = UserSignUpIn(email="test@example.com", password="password123")
        user_dict = user.model_dump()
        
        assert user_dict["email"] == "test@example.com"
        assert user_dict["password"] == "password123"
    
    def test_model_json_export(self):
        """Test exporting model to JSON"""
        user = UserSignUpIn(email="test@example.com", password="password123")
        user_json = user.model_dump_json()
        
        assert "test@example.com" in user_json
        assert "password123" in user_json
    
    def test_extra_fields_rejected(self):
        """Test that extra fields are rejected"""
        with pytest.raises(ValidationError):
            UserSignUpIn(
                email="test@example.com",
                password="password",
                extra_field="should_fail"
            )
    
    def test_null_email(self):
        """Test that None email raises validation error"""
        with pytest.raises(ValidationError):
            UserSignUpIn(email=None, password="password")
    
    def test_null_password(self):
        """Test that None password raises validation error"""
        with pytest.raises(ValidationError):
            UserSignUpIn(email="test@example.com", password=None)


class TestUserResponse:
    """Test UserResponse model"""
    
    def test_valid_user_response(self):
        """Test creating valid UserResponse instance"""
        user = UserResponse(email="test@example.com")
        assert user.email == "test@example.com"
    
    def test_valid_email_formats(self):
        """Test various valid email formats"""
        valid_emails = [
            "simple@example.com",
            "user+tag@example.com",
            "user.name@example.com",
            "test@sub.example.com",
        ]
        
        for email in valid_emails:
            user = UserResponse(email=email)
            assert user.email == email
    
    def test_invalid_email_format(self):
        """Test that invalid email formats raise validation error"""
        with pytest.raises(ValidationError):
            UserResponse(email="notanemail")
    
    def test_missing_email(self):
        """Test that missing email raises validation error"""
        with pytest.raises(ValidationError):
            UserResponse()
    
    def test_model_dict_export(self):
        """Test exporting model to dictionary"""
        user = UserResponse(email="test@example.com")
        user_dict = user.model_dump()
        
        assert user_dict["email"] == "test@example.com"
    
    def test_no_password_field(self):
        """Test that UserResponse doesn't expose password"""
        user = UserResponse(email="test@example.com")
        user_dict = user.model_dump()
        
        assert "password" not in user_dict
    
    def test_extra_fields_rejected(self):
        """Test that extra fields are rejected"""
        with pytest.raises(ValidationError):
            UserResponse(email="test@example.com", extra="field")


class TestSessionResponse:
    """Test SessionResponse model"""
    
    def test_valid_session_response(self):
        """Test creating valid SessionResponse instance"""
        user = UserResponse(email="test@example.com")
        expires_at = datetime.now() + timedelta(hours=1)
        
        session = SessionResponse(
            session_token="abc123token",
            user=user,
            expires_at=expires_at
        )
        
        assert session.session_token == "abc123token"
        assert session.user.email == "test@example.com"
        assert session.expires_at == expires_at
    
    def test_missing_session_token(self):
        """Test that missing session_token raises validation error"""
        user = UserResponse(email="test@example.com")
        expires_at = datetime.now()
        
        with pytest.raises(ValidationError):
            SessionResponse(user=user, expires_at=expires_at)
    
    def test_missing_user(self):
        """Test that missing user raises validation error"""
        expires_at = datetime.now()
        
        with pytest.raises(ValidationError):
            SessionResponse(session_token="token", expires_at=expires_at)
    
    def test_missing_expires_at(self):
        """Test that missing expires_at raises validation error"""
        user = UserResponse(email="test@example.com")
        
        with pytest.raises(ValidationError):
            SessionResponse(session_token="token", user=user)
    
    def test_expires_at_datetime_validation(self):
        """Test that expires_at must be a datetime object"""
        user = UserResponse(email="test@example.com")
        
        with pytest.raises(ValidationError):
            SessionResponse(
                session_token="token",
                user=user,
                expires_at="not a datetime"
            )
    
    def test_nested_user_validation(self):
        """Test that nested user object is validated"""
        expires_at = datetime.now()
        
        # Invalid email in nested user should raise error
        with pytest.raises(ValidationError):
            SessionResponse(
                session_token="token",
                user={"email": "notanemail"},
                expires_at=expires_at
            )
    
    def test_model_dict_export(self):
        """Test exporting model to dictionary"""
        user = UserResponse(email="test@example.com")
        expires_at = datetime(2025, 12, 31, 23, 59, 59)
        
        session = SessionResponse(
            session_token="abc123",
            user=user,
            expires_at=expires_at
        )
        
        session_dict = session.model_dump()
        
        assert session_dict["session_token"] == "abc123"
        assert session_dict["user"]["email"] == "test@example.com"
        assert session_dict["expires_at"] == expires_at
    
    def test_empty_session_token(self):
        """Test that empty session_token is allowed"""
        user = UserResponse(email="test@example.com")
        expires_at = datetime.now()
        
        session = SessionResponse(
            session_token="",
            user=user,
            expires_at=expires_at
        )
        
        assert session.session_token == ""
    
    def test_long_session_token(self):
        """Test that long session tokens are accepted"""
        user = UserResponse(email="test@example.com")
        expires_at = datetime.now()
        long_token = "a" * 1000
        
        session = SessionResponse(
            session_token=long_token,
            user=user,
            expires_at=expires_at
        )
        
        assert session.session_token == long_token
    
    def test_past_expiration_date(self):
        """Test that past expiration dates are accepted"""
        user = UserResponse(email="test@example.com")
        past_date = datetime(2020, 1, 1)
        
        session = SessionResponse(
            session_token="token",
            user=user,
            expires_at=past_date
        )
        
        assert session.expires_at == past_date
    
    def test_future_expiration_date(self):
        """Test that future expiration dates are accepted"""
        user = UserResponse(email="test@example.com")
        future_date = datetime(2030, 12, 31)
        
        session = SessionResponse(
            session_token="token",
            user=user,
            expires_at=future_date
        )
        
        assert session.expires_at == future_date


class TestModelInteroperability:
    """Test interactions between models"""
    
    def test_user_signup_to_response_conversion(self):
        """Test converting UserSignUpIn to UserResponse"""
        signup = UserSignUpIn(
            email="test@example.com",
            password="password123"
        )
        
        # Simulate conversion (password excluded)
        response = UserResponse(email=signup.email)
        
        assert response.email == signup.email
        assert not hasattr(response, 'password')
    
    def test_create_session_from_signup(self):
        """Test creating SessionResponse from UserSignUpIn"""
        signup = UserSignUpIn(
            email="test@example.com",
            password="password123"
        )
        
        user_response = UserResponse(email=signup.email)
        expires_at = datetime.now() + timedelta(hours=24)
        
        session = SessionResponse(
            session_token="generated_token_123",
            user=user_response,
            expires_at=expires_at
        )
        
        assert session.user.email == signup.email
        assert session.expires_at > datetime.now()


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_maximum_email_length(self):
        """Test email with maximum reasonable length"""
        # RFC 5321 specifies max 254 characters for email
        local_part = "a" * 64
        domain_part = "b" * 63 + ".com"
        long_email = f"{local_part}@{domain_part}"
        
        user = UserSignUpIn(email=long_email, password="password")
        assert len(user.email) <= 254
    
    def test_minimum_valid_email(self):
        """Test shortest valid email"""
        short_email = "a@b.c"
        user = UserSignUpIn(email=short_email, password="password")
        assert user.email == short_email
    
    def test_datetime_with_timezone(self):
        """Test SessionResponse with timezone-aware datetime"""
        from datetime import timezone
        
        user = UserResponse(email="test@example.com")
        expires_at = datetime.now(timezone.utc)
        
        session = SessionResponse(
            session_token="token",
            user=user,
            expires_at=expires_at
        )
        
        assert session.expires_at.tzinfo is not None
    
    def test_datetime_without_timezone(self):
        """Test SessionResponse with naive datetime"""
        user = UserResponse(email="test@example.com")
        expires_at = datetime.now()  # naive datetime
        
        session = SessionResponse(
            session_token="token",
            user=user,
            expires_at=expires_at
        )
        
        assert session.expires_at == expires_at