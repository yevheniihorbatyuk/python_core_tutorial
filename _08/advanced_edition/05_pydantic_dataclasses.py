"""
Module 8.5 (Advanced): Pydantic & Advanced Validation
======================================================

Learning Goals:
- Master Pydantic for production validation
- Implement field validators and root validators
- Create custom serializers/deserializers
- Use Pydantic with FastAPI
- Handle complex validation scenarios

⚡ Real-World Applications:
- API request/response validation
- Configuration management
- Database ORM integration
- ML pipeline validation
- ETL data validation

🏗️ Production Patterns:
- Type-safe APIs with Pydantic
- FastAPI integration
- Complex business logic validation
- Serialization hooks
"""

from __future__ import annotations

try:
    from pydantic import (
        BaseModel,
        Field,
        field_validator,
        field_serializer,
        model_validator,
        ConfigDict,
        ValidationError,
    )
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    print("⚠️  Pydantic not installed. Install with: pip install pydantic")

from typing import Optional, Any
from datetime import datetime, timezone
import json
import re


# ========================================================================
# SECTION 1: BASIC PYDANTIC MODELS
# ========================================================================

print("=" * 80)
print("SECTION 1: PYDANTIC MODELS - AUTOMATIC VALIDATION")
print("=" * 80)

if HAS_PYDANTIC:

    class Email(BaseModel):
        """Simple model with automatic validation."""
        email: str
        verified: bool = False

    print("\nAutomatic type validation:")
    try:
        # Valid email
        e1 = Email(email="user@example.com")
        print(f"✅ Valid: {e1}")

        # Invalid email (wrong type)
        e2 = Email(email=123)  # Will fail
    except ValidationError as err:
        print(f"❌ Type error: {err}")

    print("\nDefault values:")
    e3 = Email(email="test@test.com")  # verified defaults to False
    print(f"  {e3}")
    print(f"  verified={e3.verified}")

else:
    print("Skipping Pydantic examples (not installed)")


# ========================================================================
# SECTION 2: FIELD VALIDATORS
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 2: FIELD VALIDATORS")
print("=" * 80)

if HAS_PYDANTIC:

    class User(BaseModel):
        """User with validation rules."""
        username: str = Field(..., min_length=3, max_length=20)
        email: str = Field(...)
        age: int = Field(..., ge=0, le=150)
        password: str = Field(..., min_length=8)

        @field_validator("username")
        @classmethod
        def username_alphanumeric(cls, v: str) -> str:
            """Validate username is alphanumeric + underscore."""
            if not re.match(r"^[a-zA-Z0-9_]+$", v):
                raise ValueError("Username must be alphanumeric + underscore")
            return v.lower()  # Normalize to lowercase

        @field_validator("email")
        @classmethod
        def email_valid(cls, v: str) -> str:
            """Validate email format."""
            if "@" not in v or "." not in v.split("@")[1]:
                raise ValueError("Invalid email format")
            return v.lower()

        @field_validator("password")
        @classmethod
        def password_strong(cls, v: str) -> str:
            """Validate password strength."""
            if not any(c.isupper() for c in v):
                raise ValueError("Password must contain uppercase")
            if not any(c.isdigit() for c in v):
                raise ValueError("Password must contain digit")
            return v

    print("\nValidating user with field validators:\n")

    try:
        # Valid user
        user = User(
            username="john_doe",
            email="john@example.com",
            age=30,
            password="SecurePass123"
        )
        print(f"✅ Valid user: {user}")
        print(f"   Username normalized: {user.username}")
        print(f"   Email normalized: {user.email}")

    except ValidationError as err:
        print(f"❌ Validation error:")
        for error in err.errors():
            print(f"   {error['loc']}: {error['msg']}")

    print("\nAttempting invalid user:")
    try:
        invalid = User(
            username="short",
            email="notanemail",
            age=200,
            password="weak"
        )
    except ValidationError as err:
        print(f"❌ Validation errors:")
        for error in err.errors():
            print(f"   {error['loc'][0]}: {error['msg']}")

else:
    print("Pydantic not available")


# ========================================================================
# SECTION 3: MODEL VALIDATORS (CROSS-FIELD)
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 3: MODEL VALIDATORS (CROSS-FIELD VALIDATION)")
print("=" * 80)

if HAS_PYDANTIC:

    class DateRange(BaseModel):
        """Validate relationship between fields."""
        start_date: datetime
        end_date: datetime
        duration_days: Optional[int] = None

        @model_validator(mode="after")
        def validate_date_range(self):
            """Ensure end_date > start_date and calculate duration."""
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")

            # Auto-calculate duration
            delta = self.end_date - self.start_date
            self.duration_days = delta.days

            return self

    print("\nValidating date ranges:\n")

    try:
        # Valid range
        range1 = DateRange(
            start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2026, 1, 31, tzinfo=timezone.utc)
        )
        print(f"✅ Valid: {range1.duration_days} days")

    except ValidationError as err:
        print(f"❌ Error: {err}")

    print("\nAttempting invalid range:")
    try:
        range2 = DateRange(
            start_date=datetime(2026, 2, 1, tzinfo=timezone.utc),
            end_date=datetime(2026, 1, 1, tzinfo=timezone.utc)
        )
    except ValidationError as err:
        print(f"❌ {err.errors()[0]['msg']}")

else:
    print("Pydantic not available")


# ========================================================================
# SECTION 4: CUSTOM SERIALIZATION
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 4: CUSTOM SERIALIZATION")
print("=" * 80)

if HAS_PYDANTIC:

    class SecureUser(BaseModel):
        """User with custom serialization (password masked)."""
        username: str
        email: str
        password: str  # Never serialize this!

        @field_serializer("password")
        def mask_password(self, value: str) -> str:
            """Mask password during serialization."""
            return "***REDACTED***"

    print("\nCustom serialization to mask sensitive data:\n")

    user = SecureUser(
        username="alice",
        email="alice@example.com",
        password="SecurePass123"
    )

    print(f"Python object password: {user.password}")
    print(f"Serialized (safe): {user.model_dump()}")
    print(f"JSON (safe): {user.model_dump_json()}")

else:
    print("Pydantic not available")


# ========================================================================
# SECTION 5: SETTINGS & ENVIRONMENT VARIABLES
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 5: SETTINGS FROM ENVIRONMENT")
print("=" * 80)

if HAS_PYDANTIC:
    from pydantic_settings import BaseSettings

    class AppSettings(BaseSettings):
        """Load configuration from environment variables."""
        api_key: str = "default-key"
        database_url: str = "sqlite:///default.db"
        debug: bool = False
        workers: int = 4

        model_config = ConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
        )

    print("\nSettings management (loads from .env):\n")

    settings = AppSettings(
        api_key="sk-1234567890",
        database_url="postgres://localhost/mydb",
        debug=True
    )

    print(f"API Key: {settings.api_key}")
    print(f"Database: {settings.database_url}")
    print(f"Debug: {settings.debug}")
    print(f"Workers: {settings.workers}")

    print("\n💡 In production:")
    print("  1. Create .env file with environment variables")
    print("  2. Load from BaseSettings")
    print("  3. Pydantic validates types automatically")

else:
    print("Pydantic or pydantic_settings not available")


# ========================================================================
# SECTION 6: FASTAPI INTEGRATION
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 6: FASTAPI INTEGRATION")
print("=" * 80)

print("""
FASTAPI uses Pydantic for automatic request/response validation:

    from fastapi import FastAPI
    from pydantic import BaseModel

    class CreateUserRequest(BaseModel):
        username: str
        email: str
        age: int = Field(..., ge=0, le=150)

    app = FastAPI()

    @app.post("/users/")
    async def create_user(user: CreateUserRequest):
        # Pydantic automatically:
        # 1. Validates request body as JSON
        # 2. Converts to CreateUserRequest object
        # 3. Validates all fields
        # 4. Returns 422 if validation fails
        return {"created": user.username}

FASTAPI BENEFITS:
✓ Automatic request validation (Pydantic)
✓ Automatic response serialization
✓ Automatic OpenAPI/Swagger documentation
✓ Type hints = API schema
✓ Validation errors return 422 status

EXAMPLE API:
    POST /users/
    {
        "username": "alice",
        "email": "alice@example.com",
        "age": 30
    }

    ✓ Valid → 200 OK
    ✗ Missing field → 422 Validation Error
    ✗ Invalid type → 422 Validation Error
    ✗ Age out of range → 422 Validation Error
""")


# ========================================================================
# SECTION 7: DISCRIMINATED UNIONS
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 7: DISCRIMINATED UNIONS (POLYMORPHISM)")
print("=" * 80)

if HAS_PYDANTIC:
    from typing import Union, Literal
    from pydantic import RootModel

    class TextEvent(BaseModel):
        """Event type: text."""
        type: Literal["text"]
        content: str

    class ImageEvent(BaseModel):
        """Event type: image."""
        type: Literal["image"]
        url: str
        alt_text: Optional[str] = None

    class Event(RootModel[Union[TextEvent, ImageEvent]]):
        """Discriminated union of event types."""
        root: Union[TextEvent, ImageEvent] = Field(..., discriminator="type")

    print("\nHandling different event types:\n")

    # This is complex in Pydantic v1, simplified in v2
    print("Pydantic can validate polymorphic types using discriminators")
    print("Useful for:")
    print("  • Event processing (different event types)")
    print("  • Message queues (different message formats)")
    print("  • API responses (different response types)")

else:
    print("Pydantic not available")


# ========================================================================
# SECTION 8: PRODUCTION PATTERNS
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 8: PRODUCTION PATTERNS")
print("=" * 80)

production_patterns = """
PATTERN 1: API REQUEST/RESPONSE MODELS

    class UserCreateRequest(BaseModel):
        username: str = Field(..., min_length=3, max_length=20)
        email: str
        age: int = Field(..., ge=18, le=150)

    class UserResponse(BaseModel):
        user_id: int
        username: str
        email: str
        created_at: datetime

    @app.post("/users/", response_model=UserResponse)
    async def create_user(request: UserCreateRequest):
        # Pydantic validates input
        # Pydantic serializes response
        user = db.create_user(request)
        return user

PATTERN 2: CONFIGURATION VALIDATION

    class DatabaseConfig(BaseModel):
        host: str
        port: int = Field(..., ge=1, le=65535)
        database: str
        pool_size: int = Field(10, ge=1, le=100)

    config = DatabaseConfig(**os.environ)  # Validate env vars

PATTERN 3: DATA TRANSFORMATION

    class Input(BaseModel):
        raw_data: str

        @field_validator("raw_data")
        @classmethod
        def parse_data(cls, v: str):
            return json.loads(v)  # Transform string to JSON

PATTERN 4: CONDITIONAL VALIDATION

    class PaymentRequest(BaseModel):
        method: Literal["credit_card", "bank_transfer"]
        credit_card_number: Optional[str] = None
        bank_account: Optional[str] = None

        @model_validator(mode="after")
        def validate_payment(self):
            if self.method == "credit_card" and not self.credit_card_number:
                raise ValueError("credit_card_number required")
            if self.method == "bank_transfer" and not self.bank_account:
                raise ValueError("bank_account required")
            return self

PATTERN 5: NESTED MODELS WITH VALIDATION

    class Address(BaseModel):
        street: str
        city: str
        zip_code: str

    class Company(BaseModel):
        name: str
        address: Address
        employees: int = Field(..., ge=1)

    # Validates nested Address automatically!
"""

print(production_patterns)


# ========================================================================
# SUMMARY
# ========================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

summary = """
✅ PYDANTIC FOR PRODUCTION:

1. AUTOMATIC VALIDATION:
   ✓ Type checking (str, int, bool, etc.)
   ✓ Range validation (ge, le, min_length, max_length)
   ✓ Pattern matching (regex)
   ✓ Custom validators

2. FIELD VALIDATORS:
   ✓ Single-field validation (@field_validator)
   ✓ Cross-field validation (@model_validator)
   ✓ Transform values (normalize, parse, convert)
   ✓ Conditional logic

3. SERIALIZATION:
   ✓ Automatic JSON serialization
   ✓ Custom serialization hooks
   ✓ Exclude fields (sensitive data)
   ✓ Pretty printing

4. FASTAPI INTEGRATION:
   ✓ Automatic request validation
   ✓ Automatic response serialization
   ✓ OpenAPI/Swagger documentation
   ✓ Type hints = API schema

5. CONFIGURATION:
   ✓ BaseSettings for environment variables
   ✓ .env file support
   ✓ Type-safe configuration
   ✓ Validation of settings

🏗️ PRODUCTION ARCHITECTURE:

    API Request (JSON)
         ↓
    Pydantic validates
         ↓
    Python object
         ↓
    Business logic
         ↓
    Database save
         ↓
    Pydantic serializes
         ↓
    JSON Response

💡 WHEN TO USE:
   ✓ All external inputs (API requests, files, config)
   ✓ Data interchange between services
   ✓ Database models (with ORM)
   ✓ Configuration management
   ✓ Type safety in large teams

🔒 SECURITY BENEFITS:
   ✓ Prevents injection attacks (validates types)
   ✓ Automatic sanitization
   ✓ Custom validation for business rules
   ✓ Clear error messages (don't leak internals)

⚡ PERFORMANCE:
   • Pydantic is fast (C extension available)
   • Validation cost << network cost
   • Caches validation schemas
   • Worth the small overhead for safety
"""

print(summary)
