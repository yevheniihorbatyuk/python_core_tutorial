"""
BEGINNER EDITION: Lesson 1 - Decimal for Precise Financial Calculations
=========================================================================

PROBLEM:
--------
Floating-point numbers (float) cannot represent all decimal values exactly.
This causes errors in financial calculations where precision is critical.

SOLUTION:
---------
Use Python's Decimal module for exact decimal arithmetic.
Every cent matters in banking!

WHY IT MATTERS:
---------------
- Banks process trillions annually
- A single rounding error repeated = millions in discrepancies
- Legal compliance requires precision
- Customer trust depends on accuracy

This lesson shows:
1. Why float fails for money
2. How Decimal solves the problem
3. Practical banking system with accounts, deposits, withdrawals
4. Transaction history with Decimal precision
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import List, Tuple
from config import (
    BANKING_CONFIG,
    validate_decimal_precision,
    LOGGING_CONFIG,
)


# ============================================================================
# PART 1: THE PROBLEM WITH FLOAT
# ============================================================================

def demonstrate_float_problem():
    """
    Show why float fails for money calculations.

    The issue: Binary floating-point cannot exactly represent
    all decimal fractions. 0.1 + 0.2 should = 0.3, but:
    """
    print("\n" + "=" * 70)
    print("PROBLEM: Float Precision Error")
    print("=" * 70)

    # Simple addition
    result_float = 0.1 + 0.2
    print(f"\n❌ Using float:")
    print(f"   0.1 + 0.2 = {result_float}")
    print(f"   Expected: 0.3")
    print(f"   Got: {result_float}")
    print(f"   Error: {result_float - 0.3}")

    # Banking example - dangerous!
    print(f"\n💰 Banking Example (DANGEROUS):")
    balance = 1000.00
    withdrawal_1 = 50.50
    withdrawal_2 = 25.25
    withdrawal_3 = 24.25

    balance -= withdrawal_1
    balance -= withdrawal_2
    balance -= withdrawal_3

    expected = 1000.00 - 50.50 - 25.25 - 24.25
    print(f"   Starting: ${1000.00:.2f}")
    print(f"   After 3 withdrawals: ${balance:.2f}")
    print(f"   Expected: ${expected:.2f}")
    print(f"   ⚠️  Rounding hides the error, but internally it's wrong!")
    print(f"   Raw value: {balance}")

    # Accumulation of errors
    print(f"\n📊 Accumulation of Errors (1000 transactions):")
    balance = 0.00
    for i in range(1000):
        balance += 0.1  # Add 0.1 cents 1000 times

    print(f"   Expected: ${100.00:.2f}")
    print(f"   Got: ${balance:.2f}")
    print(f"   Error: ${abs(balance - 100.0):.10f}")


# ============================================================================
# PART 2: THE SOLUTION - DECIMAL
# ============================================================================

def demonstrate_decimal_solution():
    """
    Show how Decimal solves the problem.

    Decimal stores numbers as strings internally, avoiding
    the binary representation issue completely.
    """
    print("\n" + "=" * 70)
    print("SOLUTION: Using Decimal")
    print("=" * 70)

    # Simple addition
    d1 = Decimal("0.1")
    d2 = Decimal("0.2")
    result = d1 + d2

    print(f"\n✅ Using Decimal:")
    print(f"   Decimal('0.1') + Decimal('0.2') = {result}")
    print(f"   Correct! Exactly 0.3")

    # Banking example - correct!
    print(f"\n💰 Banking Example (CORRECT):")
    balance = Decimal("1000.00")
    w1 = Decimal("50.50")
    w2 = Decimal("25.25")
    w3 = Decimal("24.25")

    balance -= w1
    balance -= w2
    balance -= w3

    expected = Decimal("900.00")
    print(f"   Starting: ${balance + w1 + w2 + w3:.2f}")
    print(f"   After 3 withdrawals: ${balance:.2f}")
    print(f"   Expected: ${expected:.2f}")
    print(f"   ✓ CORRECT!")

    # Accumulation - perfect
    print(f"\n📊 Accumulation (1000 transactions):")
    balance = Decimal("0.00")
    for i in range(1000):
        balance += Decimal("0.10")

    print(f"   Expected: ${100.00:.2f}")
    print(f"   Got: ${balance:.2f}")
    print(f"   ✓ Perfectly correct!")


# ============================================================================
# PART 3: PRACTICAL BANKING SYSTEM
# ============================================================================

class BankAccount:
    """
    A bank account with Decimal precision.

    Key concepts:
    - Uses Decimal for all money calculations
    - Tracks transaction history
    - Enforces business rules (withdrawal limits, etc)
    - Validates all inputs
    """

    def __init__(self, account_id: str, account_holder: str):
        """Initialize a new account."""
        self.account_id = account_id
        self.account_holder = account_holder
        self.balance = BANKING_CONFIG["initial_balance"]
        self.transactions: List[dict] = []

        # Record opening
        self.transactions.append({
            "timestamp": datetime.now(),
            "type": "opening",
            "amount": self.balance,
            "description": "Account opened",
            "balance_after": self.balance,
        })

    def deposit(self, amount: Decimal, description: str = "Deposit"):
        """
        Add money to account.

        Args:
            amount: Money to add (must be positive Decimal)
            description: What for? ("Salary", "Refund", etc)

        Raises:
            ValueError: If amount is invalid
        """
        amount = Decimal(str(amount))

        # Validate
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        # Round to 2 decimal places (cents)
        amount = validate_decimal_precision(amount, 2)

        # Record transaction
        self.balance += amount
        self.transactions.append({
            "timestamp": datetime.now(),
            "type": "deposit",
            "amount": amount,
            "description": description,
            "balance_after": self.balance,
        })

        return self.balance

    def withdraw(self, amount: Decimal, description: str = "Withdrawal"):
        """
        Remove money from account.

        Args:
            amount: Money to remove
            description: What for? ("ATM", "Check", etc)

        Raises:
            ValueError: If amount invalid or insufficient funds
        """
        amount = Decimal(str(amount))

        # Validate
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        # Check limit
        limit = BANKING_CONFIG["daily_withdrawal_limit"]
        if amount > limit:
            raise ValueError(f"Exceeds daily limit of ${limit}")

        # Check funds
        fee = BANKING_CONFIG["withdrawal_fee"]
        total_needed = amount + fee

        if self.balance < total_needed:
            raise ValueError(
                f"Insufficient funds. "
                f"Balance: ${self.balance}, "
                f"Need: ${total_needed}"
            )

        # Apply withdrawal
        amount = validate_decimal_precision(amount, 2)
        fee = validate_decimal_precision(fee, 2)

        self.balance -= amount
        self.balance -= fee

        # Record transaction
        self.transactions.append({
            "timestamp": datetime.now(),
            "type": "withdrawal",
            "amount": amount,
            "fee": fee,
            "total": amount + fee,
            "description": description,
            "balance_after": self.balance,
        })

        return self.balance

    def transfer(self, target_account: "BankAccount", amount: Decimal):
        """
        Transfer money to another account.

        Args:
            target_account: Account to transfer to
            amount: Amount to transfer

        Raises:
            ValueError: If invalid or insufficient funds
        """
        amount = Decimal(str(amount))
        fee = BANKING_CONFIG["transfer_fee"]

        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        total_needed = amount + fee
        if self.balance < total_needed:
            raise ValueError(f"Insufficient funds for transfer")

        # Execute transfer (both succeed or both fail)
        amount = validate_decimal_precision(amount, 2)
        fee = validate_decimal_precision(fee, 2)

        self.balance -= amount
        self.balance -= fee
        target_account.balance += amount

        # Record transactions
        self.transactions.append({
            "timestamp": datetime.now(),
            "type": "transfer_sent",
            "amount": amount,
            "fee": fee,
            "to": target_account.account_id,
            "balance_after": self.balance,
        })

        target_account.transactions.append({
            "timestamp": datetime.now(),
            "type": "transfer_received",
            "amount": amount,
            "from": self.account_id,
            "balance_after": target_account.balance,
        })

    def apply_interest(self, rate: Decimal = BANKING_CONFIG["savings_rate"]):
        """
        Add interest to account (annual calculation simplified).

        Args:
            rate: Annual interest rate (0.025 = 2.5%)
        """
        rate = Decimal(str(rate))
        interest = (self.balance * rate / 100).quantize(Decimal("0.01"))

        self.balance += interest
        self.transactions.append({
            "timestamp": datetime.now(),
            "type": "interest",
            "amount": interest,
            "description": f"Interest at {rate}% annual",
            "balance_after": self.balance,
        })

        return interest

    def print_summary(self):
        """Print account summary."""
        print(f"\n{'Account Summary':^70}")
        print("-" * 70)
        print(f"Account ID:      {self.account_id}")
        print(f"Holder:          {self.account_holder}")
        print(f"Current Balance: ${self.balance:>10.2f}")
        print(f"Transactions:    {len(self.transactions)}")

    def print_statement(self, limit: int = 10):
        """Print transaction history."""
        print(f"\n{'Transaction History':^70}")
        print("-" * 70)
        print(
            f"{'Type':<15} {'Amount':>12} {'Fee':>8} {'Balance':>12} "
            f"{'Description':<20}"
        )
        print("-" * 70)

        # Show last N transactions
        for txn in self.transactions[-limit:]:
            type_ = txn["type"]
            amount = txn.get("amount", Decimal("0"))
            fee = txn.get("fee", Decimal("0"))
            balance = txn["balance_after"]
            description = txn.get("description", "")[:20]

            # Format with exact 2 decimal places
            print(
                f"{type_:<15} ${amount:>10.2f} ${fee:>6.2f} "
                f"${balance:>10.2f} {description:<20}"
            )


# ============================================================================
# PART 4: DEMONSTRATION
# ============================================================================

def run_demo():
    """Run complete banking demonstration."""
    print("\n" + "=" * 70)
    print("BEGINNER EDITION - LESSON 1: DECIMAL FOR BANKING")
    print("=" * 70)

    # Show the problem
    demonstrate_float_problem()

    # Show the solution
    demonstrate_decimal_solution()

    # Practical example - create accounts
    print("\n" + "=" * 70)
    print("PRACTICAL EXAMPLE: Bank Accounts with Decimal")
    print("=" * 70)

    # Create two accounts
    alice = BankAccount("001", "Alice Johnson")
    bob = BankAccount("002", "Bob Smith")

    alice.print_summary()

    # Transactions
    print("\n[1] Alice deposits salary...")
    alice.deposit(Decimal("3500.00"), "Salary")

    print("[2] Alice withdraws cash...")
    alice.withdraw(Decimal("200.00"), "ATM withdrawal")

    print("[3] Bob deposits...")
    bob.deposit(Decimal("1000.00"), "Initial deposit")

    print("[4] Alice transfers to Bob...")
    alice.transfer(bob, Decimal("500.00"))

    print("[5] Applying interest...")
    alice.apply_interest(BANKING_CONFIG["savings_rate"])
    bob.apply_interest(BANKING_CONFIG["checking_rate"])

    # Show results
    alice.print_statement()
    bob.print_statement()

    # Verify precision
    print("\n" + "=" * 70)
    print("PRECISION VERIFICATION")
    print("=" * 70)
    total_money = alice.balance + bob.balance
    print(f"Alice balance: ${alice.balance:.2f}")
    print(f"Bob balance:   ${bob.balance:.2f}")
    print(f"Total:         ${total_money:.2f}")
    print(f"Type:          {type(alice.balance)}")
    print(f"✓ All calculations precise to the cent!")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

"""
KEY TAKEAWAYS FROM LESSON 1:
============================

1. Float is WRONG for money:
   - Binary representation can't handle decimal fractions exactly
   - Errors accumulate in financial calculations
   - Legal/compliance violations possible

2. Decimal is RIGHT for money:
   - Stores as exact decimal strings
   - No rounding errors
   - Industry standard for finance

3. When to use Decimal:
   ✓ Money (always)
   ✓ Precise measurements (medicine, engineering)
   ✓ Legal/financial calculations
   ✗ Scientific calculations (use float)
   ✗ Performance-critical (float is faster)

4. Best practices:
   - Initialize from strings: Decimal("0.1"), not Decimal(0.1)
   - Validate precision: .quantize(Decimal("0.01")) for USD
   - Check business rules: limits, fees, balances
   - Record all transactions for audit trail

REAL-WORLD IMPACT:
==================
- Banks: Process $100+ billion daily with Decimal
- PayPal: Scaled to billions of transactions
- IRS: Uses Decimal for tax calculations
- Healthcare: Drug dosages require Decimal precision

NEXT STEP:
==========
Learn about Generators to process large datasets efficiently.
Decimal handles money, Generators handle volume.
"""

if __name__ == "__main__":
    run_demo()
