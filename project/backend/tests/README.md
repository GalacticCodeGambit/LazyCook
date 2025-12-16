# LazyCook Backend Tests

This directory contains comprehensive unit tests for the LazyCook backend application.

## Test Structure

### test_datenbank.py
Tests for the `Datenbank.py` module covering:
- Database initialization and table creation
- User registration (`addNutzer`)
- User login data retrieval (`anmeldenNutzer`)
- Connection management
- Text syntax removal utility
- Edge cases and error conditions
- SQL injection protection
- Integration tests

### test_lazycookverwaltung.py
Tests for the `LazyCookVerwaltung.py` module covering:
- Password hashing (`hash_password`)
- Password verification (`verify_password`)
- Login endpoint (`/api/login`)
- Registration endpoint (`/api/register`)
- CORS middleware configuration
- Security considerations (timing attacks, salt uniqueness)
- FastAPI endpoint behavior
- Unicode and special character handling

### test_models.py
Tests for the `models.py` module covering:
- `UserSignUpIn` model validation
- `UserResponse` model validation
- `SessionResponse` model validation
- Email format validation
- Field requirements and constraints
- Model interoperability
- Edge cases and boundary conditions

## Running Tests

### Run all tests
```bash
cd project/backend
pytest
```

### Run specific test file
```bash
pytest tests/test_datenbank.py
pytest tests/test_lazycookverwaltung.py
pytest tests/test_models.py
```

### Run tests with coverage
```bash
pytest --cov=. --cov-report=html
```

### Run tests with verbose output
```bash
pytest -v
```

### Run specific test class or function
```bash
pytest tests/test_datenbank.py::TestAddNutzer
pytest tests/test_datenbank.py::TestAddNutzer::test_addNutzer_success_new_user
```

## Test Coverage

The test suite provides comprehensive coverage including:
- ✅ Happy path scenarios
- ✅ Edge cases (empty strings, long inputs, special characters)
- ✅ Error conditions and exception handling
- ✅ Security considerations (SQL injection, timing attacks)
- ✅ Input validation
- ✅ Database operations
- ✅ API endpoints
- ✅ Password hashing and verification
- ✅ Model validation

## Dependencies

Tests require the following packages (already in requirements.txt):
- pytest
- pytest-asyncio
- pytest-mock
- fastapi
- pydantic

## Notes

- Tests use in-memory SQLite databases to avoid affecting production data
- Mocking is used extensively to isolate units under test
- All database operations are tested with proper cleanup
- Security-related tests verify hashing, salting, and injection protection