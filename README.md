# Luhn's Algorithm for Checksum Validation

Implementation of the **Luhn (Mod 10) algorithm** in both **C++** and **Python**, used to validate credit card numbers, IMEI numbers, and similar identification numbers.

## What Is the Luhn Algorithm?

The Luhn algorithm is a checksum formula that detects accidental errors (e.g. mistyped digits) in identification numbers such as:
- Credit/debit card numbers (Visa, Mastercard, Amex, Discover, UnionPay)
- IMEI / IMEI-SV mobile device identifiers

---

## Algorithms

### Checksum Validation
1. Starting from the **second digit from the right**, double every other digit moving left.
2. If doubling produces a two-digit number, subtract 9.
3. Sum all digits — if divisible by 10, the number is **valid**.

### Check Digit Generation
1. Starting from the **rightmost digit** of the partial number, double every other digit moving left.
2. Apply the same subtraction rule for two-digit results.
3. **Check digit** = `(10 − sum mod 10) mod 10`

---

## Files

```
luhn.cpp   — C++:    validate a number or generate a check digit (menu-driven)
luhn.py    — Python: validate a number or generate a check digit (CLI + library)
```

---

## C++ Usage

**Compile**
```bash
g++ -std=c++17 -o luhn luhn.cpp
```

**Run**
```bash
./luhn
# Select 1 to validate:  e.g. 4532015112830366
# Select 2 for check digit: e.g. 453201511283036
```

---

## Python Usage

**Command-line**
```bash
python luhn.py validate   4532015112830366   # validate a complete number
python luhn.py checkdigit 453201511283036    # generate its check digit
python luhn.py                               # interactive mode
```

**As a library**
```python
from luhn import luhn_validate, luhn_check_digit, identify_card_type

luhn_validate("4532015112830366")      # True
luhn_check_digit("453201511283036")    # 6
identify_card_type("4532015112830366") # "Visa"
```

---

## Sample Output

```
Number type : Visa
Digit count : 16
Digits      : 4 5 3 2 0 1 5 1 1 2 8 3 0 3 6 6

[Step 1] Double every second digit from the right:
         8 5 6 2 0 1 10 1 2 2 16 3 0 3 12 6

[Step 2] Subtract 9 from values > 9:
         8 5 6 2 0 1 1 1 2 2 7 3 0 3 3 6

[Step 3] Total sum : 50  |  mod 10 : 0

Result --> Luhn Checksum: VALID
```

---

## Card Type Detection

| Network        | Prefix(es)            | Length(s)  |
|----------------|-----------------------|------------|
| Visa           | 4                     | 13, 16, 19 |
| Mastercard     | 51–55                 | 16         |
| Mastercard     | 2221–2720             | 16         |
| American Express | 34, 37              | 15         |
| Discover       | 6011, 644–649, 65     | 16         |
| Diners Club    | 30, 36, 38            | 14         |
| UnionPay       | 62                    | 16         |
