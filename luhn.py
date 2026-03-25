#!/usr/bin/env python3
"""
luhn.py — Luhn Algorithm: Checksum Validation & Check Digit Generation

The Luhn (Mod 10) algorithm verifies the integrity of identification numbers
such as credit card numbers and IMEI identifiers.

Usage:
    python luhn.py validate   <number>          # validate a complete number
    python luhn.py checkdigit <partial_number>  # generate the check digit
    python luhn.py                              # interactive mode
"""

import sys
import argparse


# ---------------------------------------------------------------------------
# Card / number type identification
# ---------------------------------------------------------------------------

def identify_card_type(number: str) -> str:
    n, p2, p4, p6 = len(number), number[:2], number[:4], number[:6]

    if number[0] == "4" and n in (13, 16, 19):                          return "Visa"
    if number[0] == "5" and n == 16 and "51" <= p2 <= "55":             return "Mastercard"
    if number[0] == "2" and n == 16 and "222100" <= p6 <= "272099":     return "Mastercard (2-series)"
    if number[0] == "3" and n == 15 and p2 in ("34", "37"):             return "American Express"
    if number[0] == "3" and n == 14 and p2 in ("30", "36", "38"):       return "Diners Club"
    if n == 16 and (p4 == "6011" or "644" <= p4[:3] <= "649" or p2 == "65"): return "Discover"
    if n == 16 and p2 == "62":                                           return "UnionPay"
    if n in (15, 16):                                                    return "IMEI / Credit Card (unrecognized network)"
    return "Unknown"


# ---------------------------------------------------------------------------
# Core algorithm — single pass, prints walkthrough, returns result
# ---------------------------------------------------------------------------

def _run_luhn(digits: list[int], start_from_right_offset: int) -> tuple[list[int], int]:
    """
    Double every second digit starting at index (len-1 - start_from_right_offset)
    going left. Return the modified digit list and the total sum.
    """
    working = digits[:]
    i = len(working) - 1 - start_from_right_offset
    while i >= 0:
        working[i] *= 2
        if working[i] > 9:
            working[i] -= 9
        i -= 2
    return working, sum(working)


def validate_verbose(number: str) -> None:
    """Validate a complete number with step-by-step output."""
    digits = [int(c) for c in number]

    print(f"\nNumber type : {identify_card_type(number)}")
    print(f"Digit count : {len(number)}")
    print(f"Digits      : {' '.join(number)}")

    # Validation: double starting from second-to-last (offset = 1)
    step1 = digits[:]
    i = len(step1) - 2
    while i >= 0:
        step1[i] *= 2
        i -= 2
    print(f"\n[Step 1] Double every second digit from the right:\n         {' '.join(map(str, step1))}")

    step2 = [x - 9 if x > 9 else x for x in step1]
    print(f"\n[Step 2] Subtract 9 from values > 9:\n         {' '.join(map(str, step2))}")

    total = sum(step2)
    print(f"\n[Step 3] Total sum : {total}  |  mod 10 : {total % 10}")
    print(f"\nResult --> Luhn Checksum: {'VALID' if total % 10 == 0 else 'INVALID'}")


def checkdigit_verbose(partial: str) -> None:
    """Compute and display the check digit with step-by-step output."""
    print(f"\nPartial number : {' '.join(partial)}")
    print(f"Digit count    : {len(partial)}")

    # Check-digit generation: double starting from the rightmost digit (offset = 0)
    step1 = [int(c) for c in partial]
    i = len(step1) - 1
    while i >= 0:
        step1[i] *= 2
        i -= 2
    print(f"\n[Step 1] Double every second digit from the right:\n         {' '.join(map(str, step1))}")

    step2 = [x - 9 if x > 9 else x for x in step1]
    print(f"\n[Step 2] Subtract 9 from values > 9:\n         {' '.join(map(str, step2))}")

    total = sum(step2)
    check = (10 - (total % 10)) % 10
    print(f"\n[Step 3] Sum : {total}  |  Check digit = (10 - {total % 10}) mod 10 = {check}")
    print(f"\nResult --> Check Digit : {check}")
    print(f"           Full number : {partial}{check}")


# ---------------------------------------------------------------------------
# Public API (importable)
# ---------------------------------------------------------------------------

def luhn_validate(number: str) -> bool:
    """Return True if *number* (string of digits) passes the Luhn check."""
    if not number.isdigit():
        raise ValueError("Input must contain digits only.")
    digits = [int(c) for c in number]
    i = len(digits) - 2
    while i >= 0:
        digits[i] = digits[i] * 2 - (9 if digits[i] * 2 > 9 else 0)
        i -= 2
    return sum(digits) % 10 == 0


def luhn_check_digit(partial: str) -> int:
    """Return the check digit to append to *partial* to make it Luhn-valid."""
    if not partial.isdigit():
        raise ValueError("Input must contain digits only.")
    digits = [int(c) for c in partial]
    i = len(digits) - 1
    while i >= 0:
        digits[i] = digits[i] * 2 - (9 if digits[i] * 2 > 9 else 0)
        i -= 2
    return (10 - (sum(digits) % 10)) % 10


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _interactive() -> None:
    print("=" * 48)
    print("  Luhn Algorithm — Interactive Mode")
    print("=" * 48)
    print("\n[1] Validate a complete number")
    print("[2] Generate a check digit")
    choice = input("\nChoice (1/2): ").strip()

    if choice == "1":
        raw = input("Enter the complete number: ").strip().replace(" ", "").replace("-", "")
        if not raw.isdigit() or not (13 <= len(raw) <= 19):
            print("Error: Must be 13–19 digits.")
            return
        validate_verbose(raw)

    elif choice == "2":
        raw = input("Enter the partial number (without check digit): ").strip().replace(" ", "").replace("-", "")
        if not raw.isdigit() or not (12 <= len(raw) <= 18):
            print("Error: Must be 12–18 digits.")
            return
        checkdigit_verbose(raw)

    else:
        print("Invalid choice.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Luhn Algorithm — Checksum Validation & Check Digit Generation",
        epilog=(
            "Examples:\n"
            "  python luhn.py validate   4532015112830366\n"
            "  python luhn.py checkdigit 453201511283036\n"
            "  python luhn.py"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_val = sub.add_parser("validate", help="Validate a complete number")
    p_val.add_argument("number", help="Full number including check digit")

    p_cd = sub.add_parser("checkdigit", help="Generate a Luhn check digit")
    p_cd.add_argument("partial", help="Partial number without check digit")

    args = parser.parse_args()

    if args.cmd == "validate":
        number = args.number.replace(" ", "").replace("-", "")
        if not number.isdigit():
            sys.exit("Error: Input must contain digits only.")
        if not (13 <= len(number) <= 19):
            sys.exit(f"Error: Expected 13–19 digits, got {len(number)}.")
        validate_verbose(number)

    elif args.cmd == "checkdigit":
        partial = args.partial.replace(" ", "").replace("-", "")
        if not partial.isdigit():
            sys.exit("Error: Input must contain digits only.")
        if not (12 <= len(partial) <= 18):
            sys.exit(f"Error: Expected 12–18 digits, got {len(partial)}.")
        checkdigit_verbose(partial)

    else:
        _interactive()


if __name__ == "__main__":
    main()
