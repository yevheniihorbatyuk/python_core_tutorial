"""
BEGINNER EDITION: Lesson 5 - Classes for User Management System
==============================================================

PROBLEM:
--------
Managing users with functions is messy:
- Multiple function parameters (user_id, name, email, role, status)
- Easy to pass wrong data to wrong function
- No way to enforce business rules
- Hard to extend with new user types

SOLUTION:
---------
Use Classes: Bundle data (attributes) + behavior (methods) together.

WHY IT MATTERS:
---------------
- Every web framework (Flask, Django) uses classes
- Every database ORM (SQLAlchemy) uses classes
- Every API (REST, GraphQL) models data as classes
- Real systems need organization beyond functions

This lesson shows:
1. Why classes > functions for complex data
2. Creating simple User class
3. Inheritance: Employee extends User (code reuse)
4. Composition: User HAS-A Address
5. Polymorphism: Different user types, same interface
"""

from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from config import USER_MANAGEMENT_CONFIG, LOGGING_CONFIG


# ============================================================================
# PART 1: USER ROLES AND PERMISSIONS
# ============================================================================

class UserRole(Enum):
    """
    Enumeration for user roles.

    Using Enum prevents typos and makes code more robust.
    """

    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"


class UserStatus(Enum):
    """Enumeration for user account status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


# ============================================================================
# PART 2: THE PROBLEM - FUNCTIONS vs CLASSES
# ============================================================================

def demonstrate_function_approach():
    """
    Show the problem with managing users with just functions.
    """
    print("\n" + "=" * 70)
    print("PROBLEM: Managing Users with Functions")
    print("=" * 70)

    print("\n❌ Function-based approach:")
    print("""
    def create_user(user_id, name, email, role, status, permissions, created_at):
        user = {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "status": status,
            "permissions": permissions,
            "created_at": created_at,
        }
        return user

    def get_user_info(user):
        return f"{user['name']} ({user['email']}) - {user['role']}"

    def can_user_delete(user):
        return "delete" in user.get("permissions", [])

    def change_user_status(user, new_status):
        user["status"] = new_status  # No validation!

    def update_user_permissions(user, permissions):
        user["permissions"] = permissions  # Easy to break!
    """)

    print("\nProblems:")
    print("  1. Easy to pass wrong dict structure")
    print("  2. No validation of permissions")
    print("  3. No enforcement of business rules")
    print("  4. Extending with new user types = duplicate code")
    print("  5. Hard to add methods later (e.g., change_password)")
    print("  6. Mutable state, easy to accidentally break")


# ============================================================================
# PART 3: THE SOLUTION - CLASSES
# ============================================================================

class User:
    """
    Base User class - encapsulates user data and behavior.

    Key concepts:
    - __init__: Constructor, initialize attributes
    - Methods: Functions inside class
    - self: Reference to current instance
    - Encapsulation: Hide internal details
    """

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        role: UserRole = UserRole.USER,
    ):
        """
        Initialize a new user.

        Args:
            user_id: Unique identifier
            name: Full name
            email: Email address
            role: User role (admin, manager, user, guest)
        """
        # Validate inputs
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters")

        if "@" not in email:
            raise ValueError("Invalid email format")

        # Set attributes (attributes are properties of the object)
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.status = UserStatus.ACTIVE
        self.created_at = datetime.now()
        self._login_count = 0  # Private attribute (leading underscore)

    def get_info(self) -> str:
        """Return human-readable user information."""
        return f"{self.name} ({self.email}) - {self.role.value.upper()}"

    def can_perform(self, action: str) -> bool:
        """
        Check if user can perform an action.

        Uses configuration to look up permissions.
        """
        permissions = USER_MANAGEMENT_CONFIG["user_roles"].get(
            self.role.value, []
        )
        return action in permissions

    def login(self):
        """Record a login."""
        if self.status != UserStatus.ACTIVE:
            raise ValueError(f"Cannot login: account is {self.status.value}")

        self._login_count += 1
        return f"Welcome {self.name}! (Login #{self._login_count})"

    def change_status(self, new_status: UserStatus):
        """Change account status."""
        valid_statuses = [s.value for s in UserStatus]
        if new_status.value not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

        old_status = self.status
        self.status = new_status
        return f"Status changed: {old_status.value} → {new_status.value}"

    def change_email(self, new_email: str):
        """Change email with validation."""
        if "@" not in new_email:
            raise ValueError("Invalid email format")

        old_email = self.email
        self.email = new_email
        return f"Email changed: {old_email} → {new_email}"

    def print_summary(self):
        """Print user summary."""
        print(f"\nUser Summary:")
        print(f"  ID: {self.user_id}")
        print(f"  Name: {self.name}")
        print(f"  Email: {self.email}")
        print(f"  Role: {self.role.value}")
        print(f"  Status: {self.status.value}")
        print(f"  Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Logins: {self._login_count}")


# ============================================================================
# PART 4: INHERITANCE - CODE REUSE
# ============================================================================

class Employee(User):
    """
    Employee class inheriting from User.

    Demonstrates inheritance:
    - Child (Employee) inherits from Parent (User)
    - Child has all parent's methods/attributes
    - Child can add new attributes/methods
    - Child can override parent methods (polymorphism)

    DRY (Don't Repeat Yourself): User validation, login, etc.
    already defined in User class.
    """

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        role: UserRole,
        employee_id: str,
        department: str,
        salary: float = 0.0,
    ):
        """
        Initialize an employee.

        Calls parent __init__ using super().
        """
        super().__init__(user_id, name, email, role)

        self.employee_id = employee_id
        self.department = department
        self.salary = salary

    def get_info(self) -> str:
        """
        Override parent method to include employee details.

        Polymorphism: Same method name, different behavior
        depending on class.
        """
        parent_info = super().get_info()
        return f"{parent_info} | Emp:{self.employee_id} {self.department}"

    def give_raise(self, percentage: float):
        """
        Give salary increase (only available to employees).

        This method only exists in Employee, not User.
        """
        if percentage < 0 or percentage > 100:
            raise ValueError("Invalid percentage")

        old_salary = self.salary
        self.salary = self.salary * (1 + percentage / 100)
        return f"Raise given: ${old_salary:.2f} → ${self.salary:.2f}"

    def print_summary(self):
        """Override parent summary with employee info."""
        print(f"\nEmployee Summary:")
        print(f"  User ID: {self.user_id}")
        print(f"  Name: {self.name}")
        print(f"  Email: {self.email}")
        print(f"  Role: {self.role.value}")
        print(f"  Status: {self.status.value}")
        print(f"  Employee ID: {self.employee_id}")
        print(f"  Department: {self.department}")
        print(f"  Salary: ${self.salary:,.2f}")


# ============================================================================
# PART 5: COMPOSITION - FLEXIBLE COMBINING
# ============================================================================

class Address:
    """
    Address class (composition example).

    User HAS-A Address (not IS-A Address).
    """

    def __init__(
        self, street: str, city: str, country: str, postal_code: str
    ):
        """Initialize address."""
        self.street = street
        self.city = city
        self.country = country
        self.postal_code = postal_code

    def get_full_address(self) -> str:
        """Return formatted address."""
        return f"{self.street}, {self.city}, {self.country} {self.postal_code}"

    def __str__(self):
        return self.get_full_address()


class UserWithAddress(User):
    """
    User with address using composition.

    Different from inheritance:
    - Inheritance (IS-A): Employee IS-A User
    - Composition (HAS-A): User HAS-A Address

    Composition is more flexible.
    """

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        role: UserRole,
        address: Optional[Address] = None,
    ):
        """Initialize user with optional address."""
        super().__init__(user_id, name, email, role)
        self.address = address

    def get_info(self) -> str:
        """Include address in info."""
        info = super().get_info()
        if self.address:
            return f"{info} | {self.address}"
        return info

    def update_address(self, new_address: Address):
        """Change address."""
        self.address = new_address
        return f"Address updated: {new_address}"


# ============================================================================
# PART 6: POLYMORPHISM - SAME INTERFACE, DIFFERENT BEHAVIOR
# ============================================================================

def demonstrate_polymorphism():
    """
    Show polymorphism: different classes, same interface.
    """
    print("\n" + "=" * 70)
    print("POLYMORPHISM: Same Method, Different Behavior")
    print("=" * 70)

    # Create different user types
    regular_user = User("001", "Alice", "alice@example.com", UserRole.USER)
    employee = Employee(
        "002", "Bob", "bob@company.com", UserRole.MANAGER, "E123", "Engineering", 80000
    )

    address = Address("123 Main St", "Kyiv", "Ukraine", "01001")
    user_with_addr = UserWithAddress(
        "003", "Carol", "carol@example.com", UserRole.USER, address
    )

    # Call get_info() on different types
    # Same method name, different results!
    users = [regular_user, employee, user_with_addr]

    print("\nCalling get_info() on different user types:")
    for user in users:
        print(f"  {user.get_info()}")

    print("\n💡 Polymorphism: get_info() works on all types")
    print("   Each class implements it differently")


# ============================================================================
# PART 7: USER MANAGEMENT SYSTEM
# ============================================================================

class UserManagementSystem:
    """
    Simple user management system.

    Demonstrates:
    - Working with multiple user objects
    - Searching/filtering users
    - Business logic and validation
    """

    def __init__(self):
        """Initialize with empty user list."""
        self.users: Dict[str, User] = {}

    def add_user(self, user: User) -> str:
        """Add user to system."""
        if user.user_id in self.users:
            raise ValueError(f"User {user.user_id} already exists")

        self.users[user.user_id] = user
        return f"User {user.name} added successfully"

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self) -> List[User]:
        """Get all users."""
        return list(self.users.values())

    def get_users_by_role(self, role: UserRole) -> List[User]:
        """Get all users with specific role."""
        return [u for u in self.users.values() if u.role == role]

    def count_by_status(self) -> Dict[str, int]:
        """Count users by status."""
        counts = {}
        for status in UserStatus:
            count = sum(
                1 for u in self.users.values() if u.status == status
            )
            if count > 0:
                counts[status.value] = count
        return counts

    def print_all_users(self):
        """Print all users."""
        print(f"\n{'User Directory':^70}")
        print("-" * 70)

        if not self.users:
            print("  (No users)")
            return

        for user in self.users.values():
            print(f"  {user.get_info()}")

    def print_statistics(self):
        """Print system statistics."""
        print(f"\n{'User Management System Statistics':^70}")
        print("-" * 70)
        print(f"  Total users: {len(self.users)}")
        print(f"  Users by status:")
        for status, count in self.count_by_status().items():
            print(f"    {status}: {count}")
        print(f"  Users by role:")
        for role in UserRole:
            count = len(self.get_users_by_role(role))
            if count > 0:
                print(f"    {role.value}: {count}")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def run_demo():
    """Run complete user management demonstration."""
    print("\n" + "=" * 70)
    print("BEGINNER EDITION - LESSON 5: CLASSES & OOP")
    print("=" * 70)

    demonstrate_function_approach()

    # Create user management system
    print("\n" + "=" * 70)
    print("PRACTICAL: User Management System")
    print("=" * 70)

    system = UserManagementSystem()

    # Add users
    print("\n[1] Creating users...")
    try:
        user1 = User("001", "Alice Johnson", "alice@example.com", UserRole.USER)
        system.add_user(user1)

        user2 = Employee(
            "002",
            "Bob Smith",
            "bob@company.com",
            UserRole.MANAGER,
            "E001",
            "Engineering",
            85000.0,
        )
        system.add_user(user2)

        addr = Address("456 Oak Ave", "Lviv", "Ukraine", "79000")
        user3 = UserWithAddress(
            "003",
            "Carol Davis",
            "carol@example.com",
            UserRole.ADMIN,
            addr,
        )
        system.add_user(user3)

        print("  ✓ Users created successfully")
    except ValueError as e:
        print(f"  ✗ Error: {e}")

    # Show user info
    print("\n[2] User information:")
    system.print_all_users()

    # Test user actions
    print("\n[3] User actions...")
    try:
        message = user1.login()
        print(f"  Alice login: {message}")

        message = user2.give_raise(10)
        print(f"  Bob salary: {message}")

        message = user1.change_email("alice.new@example.com")
        print(f"  Alice email: {message}")
    except Exception as e:
        print(f"  Error: {e}")

    # Test permissions
    print("\n[4] Permission checks...")
    for user in [user1, user2, user3]:
        can_delete = user.can_perform("delete")
        can_read = user.can_perform("read")
        print(
            f"  {user.name:15} | "
            f"Delete: {str(can_delete):5} | Read: {str(can_read):5}"
        )

    # Polymorphism demo
    demonstrate_polymorphism()

    # Statistics
    system.print_statistics()


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

"""
KEY TAKEAWAYS FROM LESSON 5:
============================

1. Classes organize data + behavior:
   class User:
       def __init__(self, name, email):
           self.name = name
           self.email = email

       def login(self):
           return f"Welcome {self.name}"

2. Inheritance (IS-A) - code reuse:
   class Employee(User):
       Employee inherits name, email, login() from User
       Adds: employee_id, department, salary

3. Composition (HAS-A) - flexible combining:
   class User:
       address = Address(...)
       User HAS-A Address (not IS-A Address)

4. Polymorphism - same interface, different behavior:
   user.get_info()  → "Alice (alice@example.com) - USER"
   employee.get_info() → "Bob (bob@example.com) - MANAGER | Emp:E123"

5. Encapsulation - hide internal details:
   Public: name, email, get_info()
   Private: _login_count (leading underscore)

WHEN TO USE CLASSES:
====================
✓ Complex data with related behavior
✓ Multiple instances (users, products, orders)
✓ Inheritance hierarchy (Employee, Manager, Admin)
✓ Validation rules
✓ State that changes (status, permissions)

✗ Simple data lookup
✗ One-time calculations
✗ When dict is simpler

REAL-WORLD IMPACT:
==================
- Web frameworks: Flask/Django models are classes
- Databases: SQLAlchemy/ORM use classes for tables
- APIs: Every endpoint returns class instances
- Mobile apps: Same (Swift classes, Kotlin classes)

NEXT STEP:
==========
Combine Functional Programming + OOP:
- Use @lru_cache on class methods
- Use generators in class methods
- Use map/filter for data transformation

This is advanced Python!
"""

if __name__ == "__main__":
    run_demo()
