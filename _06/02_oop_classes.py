"""
MODULE 6.2: Object-Oriented Programming (OOP)
==============================================

PURPOSE:
  Design systems using classes, inheritance, and composition patterns.
  Understand why OOP is fundamental to all modern software.

CONTENTS:
  1. Basics: Classes and objects
  2. Inheritance and polymorphism
  3. Composition vs Inheritance (HAS-A vs IS-A)
  4. Method Resolution Order (MRO)
  5. Real-world examples (Data Science, Web, Finance)

PRACTICAL VALUE:
  ✓ Web: All frameworks (Flask, Django) built on OOP
  ✓ Data Science: sklearn, pandas, TensorFlow are classes
  ✓ Finance: Models for instruments (stocks, bonds)
  ✓ Systems: Architecture through classes and inheritance
"""

from datetime import datetime
from decimal import Decimal

print("=" * 80)
print("MODULE 6.2: OBJECT-ORIENTED PROGRAMMING")
print("=" * 80)


# ============================================================================
# 1. BASICS: Classes and Objects
# ============================================================================

print("\n\n[1] BASICS: Classes and Objects")
print("-" * 80)

print("\n✅ Simple Class: Person")


class Person:
    """
    Represents a person with basic information.

    ATTRIBUTES:
      name (str): Person's name
      age (int): Age in years
      email (str): Email address

    METHODS:
      info() - Return information string
      birthday() - Increment age by 1
      __str__() - How it looks when printed
    """

    def __init__(self, name, age, email):
        """
        Constructor (__init__).

        Called automatically when creating Person(...).
        self = reference to the current object.
        """
        self.name = name
        self.age = age
        self.email = email
        print(f"  ✓ Created object: {name}")

    def info(self):
        """Return information about the person"""
        return f"{self.name} ({self.age} years), {self.email}"

    def birthday(self):
        """Celebrate a birthday"""
        self.age += 1
        return f"🎉 Happy birthday {self.name}! Now {self.age} years old"

    def __str__(self):
        """How it looks when printed"""
        return self.info()


# Create objects (instances)
print("\n  Creating objects:")
p1 = Person("Alice", 30, "alice@example.com")
p2 = Person("Bob", 25, "bob@example.com")

print(f"\n  Information:")
print(f"    {p1}")
print(f"    {p2}")

print(f"\n  Birthday celebration:")
print(f"    {p1.birthday()}")


# ============================================================================
# 2. INHERITANCE: Code Reuse
# ============================================================================

print("\n\n[2] INHERITANCE: Employee Inherits from Person")
print("-" * 80)

print("\n❌ WITHOUT Inheritance: Code Duplication")
print("""
  class Person:
      name, age, email, info()  ← base

  class Employee:
      name, age, email          ← DUPLICATE!
      info()                    ← DUPLICATE!
      salary                    ← own

  PROBLEM: Change info() → must change 3 places!
""")

print("✅ WITH Inheritance: DRY (Don't Repeat Yourself)")
print("""
  class Person:
      name, age, email, info()  ← base (one place)

  class Employee(Person):  ← inherits everything
      salary                ← adds its own
      info()                ← overrides (polymorph)
""")


class Employee(Person):
    """
    Employee (inherits from Person).

    Has ALL attributes and methods from Person.
    Adds its own: salary, position, hire_date.
    Overrides: info() with more details.
    """

    def __init__(self, name, age, email, salary, position):
        """
        Employee constructor.

        super().__init__() = call parent constructor.
        """
        super().__init__(name, age, email)  # Initialize parent fields

        self.salary = salary
        self.position = position
        self.hire_date = datetime.now()

    # OVERRIDE: Replace parent method
    def info(self):
        """
        Overridden info() that includes salary and position.

        super().info() = get parent info() and add to it.
        """
        base_info = super().info()
        return f"{base_info} | {self.position}, ${self.salary:,}/year"

    def give_raise(self, percentage):
        """Increase salary by percentage"""
        raise_amount = self.salary * percentage / 100
        self.salary += raise_amount
        return f"💰 Salary increased by ${raise_amount:,.2f}. New: ${self.salary:,}/year"


class Manager(Person):
    """
    Manager (inherits from Person).

    Unlike Employee, manages a team.
    """

    def __init__(self, name, age, email, salary, team_size):
        super().__init__(name, age, email)
        self.salary = salary
        self.team_size = team_size
        self.employees = []

    def info(self):
        base_info = super().info()
        return f"{base_info} | Manager of {self.team_size} people"

    def hire_employee(self, employee):
        """Hire an employee to the team"""
        self.employees.append(employee)
        return f"✓ {employee.name} hired to team {self.name}"


# Usage
print("\n  Creating objects:")
emp = Employee("John Smith", 35, "john@company.com", 80000, "Senior Engineer")
mgr = Manager("Sarah Johnson", 40, "sarah@company.com", 120000, 5)

print(f"\n  Information (inheritance + override):")
print(f"    {emp}")
print(f"    {mgr}")

print(f"\n  Employee method (its own):")
print(f"    {emp.give_raise(10)}")


# ============================================================================
# 3. COMPOSITION: Combining Objects (HAS-A)
# ============================================================================

print("\n\n[3] COMPOSITION: HAS-A Relationship")
print("-" * 80)

print("\n✅ Composition: Person HAS-A Address")


class Address:
    """Represents an address"""

    def __init__(self, street, city, country):
        self.street = street
        self.city = city
        self.country = country

    def full_address(self):
        return f"{self.street}, {self.city}, {self.country}"

    def __str__(self):
        return self.full_address()


class PersonWithAddress(Person):
    """
    Person with an address (composition).

    Instead of inheriting from Address,
    we compose an Address object inside.
    More flexible than inheritance.
    """

    def __init__(self, name, age, email, address):
        super().__init__(name, age, email)
        self.address = address  # HAS-A relationship

    def info(self):
        base_info = super().info()
        return f"{base_info} | Lives at {self.address}"


# Usage
print("\n  Creating addresses:")
addr_alice = Address("123 Main St", "Kyiv", "Ukraine")
addr_bob = Address("456 Oak Ave", "Lviv", "Ukraine")

print(f"    Alice: {addr_alice}")
print(f"    Bob: {addr_bob}")

print("\n  Creating people with addresses:")
alice = PersonWithAddress("Alice", 30, "alice@example.com", addr_alice)
bob = PersonWithAddress("Bob", 25, "bob@example.com", addr_bob)

print(f"    {alice}")
print(f"    {bob}")

print("\n  Flexible composition (easy to change):")
bob.address.city = "Kharkiv"  # Moved to Kharkiv
print(f"    Bob moved: {bob.address}")


# ============================================================================
# 4. METHOD RESOLUTION ORDER (MRO)
# ============================================================================

print("\n\n[4] METHOD RESOLUTION ORDER (MRO): Which Method Runs?")
print("-" * 80)

print("\n⚠️  PROBLEM: Multiple Inheritance")
print("""
  class A:
      def method(): return "A"

  class B(A):
      def method(): return "B"

  class C(A):
      def method(): return "C"

  class D(B, C):  ← Which method? B's or C's?
      pass

  d = D()
  d.method() ← "B" or "C"?
""")


class Animal:
    def speak(self):
        return "Some sound"

    def info(self):
        return "Animal info"


class Dog(Animal):
    def speak(self):
        return "Woof!"

    def info(self):
        return super().info() + " [Dog]"


class Cat(Animal):
    def speak(self):
        return "Meow!"

    def info(self):
        return super().info() + " [Cat]"


class ServiceAnimal(Dog, Cat):
    """
    Service Animal (multiple inheritance).

    MRO (Method Resolution Order):
    ServiceAnimal → Dog → Cat → Animal → object

    When calling speak(): first found in Dog → Woof!
    """
    pass


print("\n  MRO for ServiceAnimal:")
mro = ServiceAnimal.mro()
for i, cls in enumerate(mro):
    print(f"    {i}. {cls.__name__}")

sa = ServiceAnimal()
print(f"\n  Method calls (following MRO):")
print(f"    speak(): {sa.speak()}")  # Dog.speak() ← MRO order
print(f"    info(): {sa.info()}")


# ============================================================================
# 5. REAL-WORLD EXAMPLES
# ============================================================================

print("\n\n[5] REAL-WORLD EXAMPLES: Data Science + Web")
print("-" * 80)

# Real-World #1: Data Science User System
print("\n✅ Real-World #1: Data Science (User Segmentation)")


class User:
    """User in the system"""

    def __init__(self, name, email, registration_date):
        self.name = name
        self.email = email
        self.registration_date = registration_date
        self.purchases = []

    def add_purchase(self, amount, description):
        """Add a purchase"""
        self.purchases.append({
            'date': datetime.now(),
            'amount': Decimal(str(amount)),
            'description': description
        })

    def total_spent(self):
        """Total amount spent"""
        return sum(p['amount'] for p in self.purchases)

    def info(self):
        return f"{self.name} ({self.email}), Spent ${self.total_spent():.2f}"


class PremiumUser(User):
    """Premium user with benefits"""

    def __init__(self, name, email, registration_date, discount_percent=10):
        super().__init__(name, email, registration_date)
        self.discount_percent = discount_percent

    def apply_discount(self, amount):
        """Apply discount to price"""
        return Decimal(str(amount)) * (Decimal(100) - Decimal(self.discount_percent)) / Decimal(100)

    def info(self):
        base = super().info()
        return f"{base} | Premium ({self.discount_percent}% discount)"


print("  Users:")
user = User("Alice", "alice@example.com", datetime(2023, 1, 1))
user.add_purchase(50.00, "Book")
user.add_purchase(25.50, "Coffee")
print(f"    {user}")

premium = PremiumUser("Bob", "bob@example.com", datetime(2023, 6, 1))
premium.add_purchase(100.00, "Laptop")
original = Decimal('100.00')
discounted = premium.apply_discount(original)
print(f"    {premium}")
print(f"    Bob's purchase: ${original} → ${discounted} (after discount)")


# Real-World #2: Web Framework
print("\n\n✅ Real-World #2: Web Framework (Simple Routing)")


class Route:
    """HTTP route"""

    def __init__(self, path, method='GET'):
        self.path = path
        self.method = method
        self.handler = None

    def register(self, handler):
        """Register handler function"""
        self.handler = handler
        return handler


class WebApp:
    """Simple web framework (like Flask)"""

    def __init__(self, name):
        self.name = name
        self.routes = []

    def route(self, path, method='GET'):
        """
        Decorator to register routes.

        @app.route('/home')
        def home():
            return "Home page"
        """
        def decorator(func):
            route = Route(path, method)
            route.register(func)
            self.routes.append(route)
            return func
        return decorator

    def run(self):
        """Run server (simulation)"""
        print(f"  🚀 {self.name} is running\n")
        for route in self.routes:
            print(f"    {route.method:4} {route.path:20} → {route.handler.__name__}")


print("  Creating web app:")
app = WebApp("MyApp")

@app.route('/', method='GET')
def home():
    return "Home Page"

@app.route('/users/<id>', method='GET')
def get_user(user_id):
    return f"User {user_id}"

@app.route('/users', method='POST')
def create_user():
    return "User created"

app.run()


# ============================================================================
# SUMMARY
# ============================================================================

print("\n\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

print("""
✅ CLASSES - Blueprint for objects (plan → reality)

✅ INHERITANCE - Code reuse (DRY)
   - Employee inherits from Person
   - No duplication of name, age, email
   - Override info() (polymorphism)

✅ COMPOSITION - Flexible combining (HAS-A)
   - Person HAS-A Address (better than inheritance)
   - Easy to change without breaking hierarchy

✅ MRO - Method lookup order (sequence)
   - Child → Parent → GrandParent → object
   - super() calls parent method

👉 IN PRACTICE:
   - Web: Flask, Django = classes + inheritance
   - Data Science: sklearn = classes (Classifier, Regressor)
   - Finance: models for instruments (Stock, Bond)

👉 NEXT: Module 7 - Data Structures (LinkedList, Tree, Graph)
""")

print("=" * 80)
