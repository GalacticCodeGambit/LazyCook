"""
Comprehensive unit tests for Datenbank.py

Tests cover:
- Database initialization and table creation
- User registration (addNutzer)
- User login data retrieval (anmeldenNutzer)
- Edge cases and error conditions
- Text syntax removal utility
- Connection management
"""

import pytest
import sqlite3
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any


# Import the class under test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from Datenbank import Datenbank


class TestDatenbankInitialization:
    """Test database initialization and table creation"""
    
    def test_init_creates_connection(self):
        """Test that __init__ establishes a database connection"""
        with patch.object(Datenbank, 'verbindeDB') as mock_verbinde:
            db = Datenbank()
            mock_verbinde.assert_called_once()
    
    def test_verbindeDB_enables_foreign_keys(self):
        """Test that foreign keys are enabled on connection"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            with patch('Datenbank.sqlite3.connect') as mock_connect:
                mock_con = MagicMock()
                mock_cursor = MagicMock()
                mock_con.cursor.return_value = mock_cursor
                mock_connect.return_value = mock_con
                
                db = Datenbank()
                
                # Verify PRAGMA foreign_keys was called
                calls = [str(call) for call in mock_cursor.execute.call_args_list]
                assert any('PRAGMA foreign_keys' in str(call) for call in calls)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_create_tables_creates_zutat_table(self):
        """Test that Zutat table is created with correct schema"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Override the database path for testing
            with patch('Datenbank.sqlite3.connect') as mock_connect:
                test_con = sqlite3.connect(':memory:')
                test_con.row_factory = sqlite3.Row
                mock_connect.return_value = test_con
                
                db = Datenbank()
                
                # Check if Zutat table exists
                cursor = test_con.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Zutat'")
                result = cursor.fetchone()
                assert result is not None
                
                # Verify columns
                cursor.execute("PRAGMA table_info(Zutat)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                assert 'id' in column_names
                assert 'name' in column_names
                assert 'mengenArt' in column_names
                
                test_con.close()
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_create_tables_creates_konto_table(self):
        """Test that Konto table is created with correct schema"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            test_con = sqlite3.connect(':memory:')
            test_con.row_factory = sqlite3.Row
            mock_connect.return_value = test_con
            
            db = Datenbank()
            
            # Check if Konto table exists
            cursor = test_con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Konto'")
            result = cursor.fetchone()
            assert result is not None
            
            # Verify columns
            cursor.execute("PRAGMA table_info(Konto)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            assert 'id' in column_names
            assert 'email' in column_names
            assert 'passwort' in column_names
            assert 'salt' in column_names
            
            test_con.close()
    
    def test_create_tables_creates_nutzer_table(self):
        """Test that Nutzer table is created with foreign key to Konto"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            test_con = sqlite3.connect(':memory:')
            test_con.row_factory = sqlite3.Row
            mock_connect.return_value = test_con
            
            db = Datenbank()
            
            cursor = test_con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Nutzer'")
            result = cursor.fetchone()
            assert result is not None
            
            # Verify foreign key
            cursor.execute("PRAGMA foreign_key_list(Nutzer)")
            fks = cursor.fetchall()
            assert len(fks) > 0
            assert any(fk[2] == 'Konto' for fk in fks)
            
            test_con.close()
    
    def test_create_tables_creates_rezept_table(self):
        """Test that Rezept table is created"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            test_con = sqlite3.connect(':memory:')
            test_con.row_factory = sqlite3.Row
            mock_connect.return_value = test_con
            
            db = Datenbank()
            
            cursor = test_con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Rezept'")
            result = cursor.fetchone()
            assert result is not None
            
            test_con.close()
    
    def test_create_tables_handles_exceptions(self):
        """Test that table creation errors are handled gracefully"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_con = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.execute.side_effect = sqlite3.Error("Table creation failed")
            mock_con.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_con
            
            # Should not raise exception
            db = Datenbank()
            mock_con.rollback.assert_called()


class TestAddNutzer:
    """Test user registration functionality"""
    
    def setup_method(self):
        """Set up test database before each test"""
        self.test_con = sqlite3.connect(':memory:')
        self.test_con.row_factory = sqlite3.Row
        self.test_con.execute("PRAGMA foreign_keys = ON")
        
        # Create necessary tables
        self.test_con.execute("""
            CREATE TABLE IF NOT EXISTS Konto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(250) NOT NULL UNIQUE,
                passwort TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)
        self.test_con.execute("""
            CREATE TABLE IF NOT EXISTS Nutzer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                kid INTEGER NOT NULL,
                FOREIGN KEY (kid) REFERENCES Konto (id) ON DELETE CASCADE
            )
        """)
        self.test_con.commit()
    
    def teardown_method(self):
        """Clean up after each test"""
        self.test_con.close()
    
    def test_addNutzer_success_new_user(self):
        """Test successful registration of a new user"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.addNutzer(
                    email="test@example.com",
                    salt="test_salt_123",
                    passwort="hashed_password_123"
                )
                
                assert result == "Registrierung erfolgreich"
                
                # Verify user was added to database
                cursor = self.test_con.cursor()
                cursor.execute("SELECT * FROM Konto WHERE email = ?", ("test@example.com",))
                row = cursor.fetchone()
                
                assert row is not None
                assert row["email"] == "test@example.com"
                assert row["passwort"] == "hashed_password_123"
                assert row["salt"] == "test_salt_123"
    
    def test_addNutzer_duplicate_email(self):
        """Test that duplicate email registration is rejected"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                # Add first user
                db.addNutzer("duplicate@example.com", "salt1", "pass1")
                
                # Try to add second user with same email
                result = db.addNutzer("duplicate@example.com", "salt2", "pass2")
                
                assert result == "Email schon in einem Konto registriert"
    
    def test_addNutzer_multiple_unique_users(self):
        """Test adding multiple users with different emails"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result1 = db.addNutzer("user1@example.com", "salt1", "pass1")
                result2 = db.addNutzer("user2@example.com", "salt2", "pass2")
                result3 = db.addNutzer("user3@example.com", "salt3", "pass3")
                
                assert result1 == "Registrierung erfolgreich"
                assert result2 == "Registrierung erfolgreich"
                assert result3 == "Registrierung erfolgreich"
                
                # Verify all users exist
                cursor = self.test_con.cursor()
                cursor.execute("SELECT COUNT(*) FROM Konto")
                count = cursor.fetchone()[0]
                assert count == 3
    
    def test_addNutzer_empty_email(self):
        """Test registration with empty email"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.addNutzer("", "salt", "password")
                assert result == "Registrierung erfolgreich"  # SQLite allows empty strings
    
    def test_addNutzer_special_characters_in_email(self):
        """Test registration with special characters in email"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.addNutzer(
                    email="test+tag@sub.example.com",
                    salt="salt",
                    passwort="password"
                )
                
                assert result == "Registrierung erfolgreich"
    
    def test_addNutzer_long_password(self):
        """Test registration with very long password hash"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                long_password = "a" * 1000
                result = db.addNutzer("test@example.com", "salt", long_password)
                
                assert result == "Registrierung erfolgreich"
    
    def test_addNutzer_case_sensitive_email(self):
        """Test that email comparison is case-sensitive"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result1 = db.addNutzer("Test@Example.com", "salt1", "pass1")
                result2 = db.addNutzer("test@example.com", "salt2", "pass2")
                
                # Both should succeed as SQLite is case-sensitive by default
                assert result1 == "Registrierung erfolgreich"
                assert result2 == "Registrierung erfolgreich"


class TestAnmeldenNutzer:
    """Test user login data retrieval functionality"""
    
    def setup_method(self):
        """Set up test database before each test"""
        self.test_con = sqlite3.connect(':memory:')
        self.test_con.row_factory = sqlite3.Row
        
        self.test_con.execute("""
            CREATE TABLE IF NOT EXISTS Konto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(250) NOT NULL UNIQUE,
                passwort TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)
        self.test_con.commit()
    
    def teardown_method(self):
        """Clean up after each test"""
        self.test_con.close()
    
    def test_anmeldenNutzer_existing_user(self):
        """Test retrieving credentials for an existing user"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            # Insert test user
            cursor = self.test_con.cursor()
            cursor.execute(
                "INSERT INTO Konto (email, passwort, salt) VALUES (?, ?, ?)",
                ("existing@example.com", "hashed_pw_123", "salt_abc_456")
            )
            self.test_con.commit()
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.anmeldenNutzer("existing@example.com")
                
                assert result is not None
                assert result["passwort"] == "hashed_pw_123"
                assert result["salt"] == "salt_abc_456"
    
    def test_anmeldenNutzer_non_existing_user(self):
        """Test retrieving credentials for a non-existing user returns None"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.anmeldenNutzer("nonexistent@example.com")
                
                assert result is None
    
    def test_anmeldenNutzer_empty_email(self):
        """Test retrieving credentials with empty email"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.anmeldenNutzer("")
                
                assert result is None
    
    def test_anmeldenNutzer_sql_injection_attempt(self):
        """Test that SQL injection attempts are handled safely"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            # Insert legitimate user
            cursor = self.test_con.cursor()
            cursor.execute(
                "INSERT INTO Konto (email, passwort, salt) VALUES (?, ?, ?)",
                ("legitimate@example.com", "password", "salt")
            )
            self.test_con.commit()
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                # Attempt SQL injection
                result = db.anmeldenNutzer("' OR '1'='1")
                
                # Should return None, not bypass security
                assert result is None
    
    def test_anmeldenNutzer_special_characters_in_email(self):
        """Test retrieving user with special characters in email"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            cursor = self.test_con.cursor()
            cursor.execute(
                "INSERT INTO Konto (email, passwort, salt) VALUES (?, ?, ?)",
                ("test+tag@example.com", "password", "salt")
            )
            self.test_con.commit()
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.anmeldenNutzer("test+tag@example.com")
                
                assert result is not None
                assert result["passwort"] == "password"
    
    def test_anmeldenNutzer_multiple_users_correct_retrieval(self):
        """Test that the correct user is retrieved when multiple users exist"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_connect.return_value = self.test_con
            
            cursor = self.test_con.cursor()
            cursor.execute(
                "INSERT INTO Konto (email, passwort, salt) VALUES (?, ?, ?)",
                ("user1@example.com", "pass1", "salt1")
            )
            cursor.execute(
                "INSERT INTO Konto (email, passwort, salt) VALUES (?, ?, ?)",
                ("user2@example.com", "pass2", "salt2")
            )
            cursor.execute(
                "INSERT INTO Konto (email, passwort, salt) VALUES (?, ?, ?)",
                ("user3@example.com", "pass3", "salt3")
            )
            self.test_con.commit()
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = self.test_con
                
                result = db.anmeldenNutzer("user2@example.com")
                
                assert result is not None
                assert result["passwort"] == "pass2"
                assert result["salt"] == "salt2"


class TestGetConnection:
    """Test connection management"""
    
    def test_get_connection_returns_new_connection(self):
        """Test that get_connection returns a new SQLite connection"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_con = MagicMock()
            mock_connect.return_value = mock_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                
                connection = db.get_connection()
                
                # Verify connect was called with correct parameters
                mock_connect.assert_called_with("LazyCookDB", check_same_thread=False)
    
    def test_get_connection_sets_row_factory(self):
        """Test that row_factory is set on new connection"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            test_con = sqlite3.connect(':memory:')
            mock_connect.return_value = test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                
                connection = db.get_connection()
                
                assert connection.row_factory == sqlite3.Row
            
            test_con.close()


class TestEntferneTextSyntax:
    """Test text cleaning utility function"""
    
    def test_entferneTextSyntax_removes_parentheses(self):
        """Test that parentheses are removed"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("(test)")
            assert result == "test"
    
    def test_entferneTextSyntax_removes_brackets(self):
        """Test that square brackets are removed"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("[test]")
            assert result == "test"
    
    def test_entferneTextSyntax_removes_quotes(self):
        """Test that single quotes are removed"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("'test'")
            assert result == "test"
    
    def test_entferneTextSyntax_removes_commas(self):
        """Test that commas are removed"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("test,value")
            assert result == "testvalue"
    
    def test_entferneTextSyntax_complex_string(self):
        """Test cleaning complex string with multiple special characters"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("(['test', 'value'])")
            assert result == "test value"
    
    def test_entferneTextSyntax_empty_string(self):
        """Test cleaning empty string"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("")
            assert result == ""
    
    def test_entferneTextSyntax_no_special_chars(self):
        """Test cleaning string with no special characters"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("test value")
            assert result == "test value"
    
    def test_entferneTextSyntax_preserves_other_chars(self):
        """Test that other characters are preserved"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            result = db.entferneTextSyntax("test@example.com")
            assert result == "test@example.com"


class TestClose:
    """Test database connection closing"""
    
    def test_close_calls_connection_close(self):
        """Test that close() calls connection.close()"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            mock_con = MagicMock()
            mock_connect.return_value = mock_con
            
            db = Datenbank()
            db.close()
            
            mock_con.close.assert_called_once()


class TestSpeichernInDB:
    """Test speichernInDB placeholder method"""
    
    def test_speichernInDB_exists(self):
        """Test that speichernInDB method exists (placeholder)"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            # Should not raise AttributeError
            result = db.speichernInDB({"test": "data"})
            assert result is None  # Currently returns None as it's not implemented


class TestHoleDaten:
    """Test holeDaten placeholder method"""
    
    def test_holeDaten_exists(self):
        """Test that holeDaten method exists (placeholder)"""
        with patch.object(Datenbank, 'verbindeDB'):
            db = Datenbank()
            
            # Should not raise AttributeError
            result = db.holeDaten("test_table")
            assert result is None  # Currently returns None as it's not implemented


class TestIntegration:
    """Integration tests for Datenbank class"""
    
    def test_full_user_registration_and_retrieval_flow(self):
        """Test complete flow: register user and retrieve credentials"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            test_con = sqlite3.connect(':memory:')
            test_con.row_factory = sqlite3.Row
            test_con.execute("PRAGMA foreign_keys = ON")
            
            # Create tables
            test_con.execute("""
                CREATE TABLE Konto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(250) NOT NULL UNIQUE,
                    passwort TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            """)
            test_con.commit()
            
            mock_connect.return_value = test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = test_con
                
                # Register user
                reg_result = db.addNutzer(
                    "integration@test.com",
                    "integration_salt",
                    "integration_password"
                )
                assert reg_result == "Registrierung erfolgreich"
                
                # Retrieve user credentials
                login_result = db.anmeldenNutzer("integration@test.com")
                assert login_result is not None
                assert login_result["passwort"] == "integration_password"
                assert login_result["salt"] == "integration_salt"
            
            test_con.close()
    
    def test_concurrent_user_registrations(self):
        """Test multiple sequential user registrations"""
        with patch('Datenbank.sqlite3.connect') as mock_connect:
            test_con = sqlite3.connect(':memory:')
            test_con.row_factory = sqlite3.Row
            
            test_con.execute("""
                CREATE TABLE Konto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(250) NOT NULL UNIQUE,
                    passwort TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            """)
            test_con.commit()
            
            mock_connect.return_value = test_con
            
            with patch.object(Datenbank, 'verbindeDB'):
                db = Datenbank()
                db.con = test_con
                
                users = [
                    ("user1@test.com", "salt1", "pass1"),
                    ("user2@test.com", "salt2", "pass2"),
                    ("user3@test.com", "salt3", "pass3"),
                ]
                
                for email, salt, password in users:
                    result = db.addNutzer(email, salt, password)
                    assert result == "Registrierung erfolgreich"
                
                # Verify all users can be retrieved
                for email, salt, password in users:
                    login_result = db.anmeldenNutzer(email)
                    assert login_result is not None
                    assert login_result["passwort"] == password
                    assert login_result["salt"] == salt
            
            test_con.close()