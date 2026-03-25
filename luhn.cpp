/**
 * luhn.cpp — Luhn Algorithm: Checksum Validation & Check Digit Generation
 *
 * Compile:  g++ -std=c++17 -o luhn luhn.cpp
 * Run:      ./luhn
 */

#include <iostream>
#include <string>
#include <vector>
#include <numeric>
#include <algorithm>
#include <cctype>

// -----------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------

static bool isDigitsOnly(const std::string& s) {
    return !s.empty() && std::all_of(s.begin(), s.end(), ::isdigit);
}

static std::string sanitize(std::string s) {
    s.erase(std::remove_if(s.begin(), s.end(),
                           [](char c){ return c == ' ' || c == '-'; }), s.end());
    return s;
}

static std::string identifyNumberType(const std::string& num) {
    const size_t len = num.size();
    const std::string p2 = (len >= 2) ? num.substr(0, 2) : "";
    const std::string p4 = (len >= 4) ? num.substr(0, 4) : "";
    const std::string p6 = (len >= 6) ? num.substr(0, 6) : "";

    if (num[0] == '4' && (len == 13 || len == 16 || len == 19))          return "Visa";
    if (num[0] == '5' && len == 16 && p2 >= "51" && p2 <= "55")          return "Mastercard";
    if (num[0] == '2' && len == 16 && p6 >= "222100" && p6 <= "272099")  return "Mastercard (2-series)";
    if (num[0] == '3' && len == 15 && (p2 == "34" || p2 == "37"))        return "American Express";
    if (num[0] == '3' && len == 14 && (p2 == "30" || p2 == "36" || p2 == "38")) return "Diners Club";
    if (len == 16 && (p4 == "6011" || (p2 >= "64" && p2 <= "65")))       return "Discover";
    if (len == 16 && p2 == "62")                                           return "UnionPay";
    if (len == 15 || len == 16)                                            return "IMEI / Credit Card (unrecognized network)";
    return "Unknown";
}

// -----------------------------------------------------------------------
// Mode 1: Validate a complete number
// -----------------------------------------------------------------------

static void runValidate() {
    std::string input;
    std::cout << "Enter the number to validate: ";
    std::cin >> input;
    input = sanitize(input);

    if (!isDigitsOnly(input)) { std::cerr << "\nError: Digits only.\n"; return; }
    if (input.size() < 13 || input.size() > 19) {
        std::cerr << "\nError: Expected 13–19 digits, got " << input.size() << ".\n"; return;
    }

    std::cout << "\nNumber type : " << identifyNumberType(input) << "\n";
    std::cout << "Digit count : " << input.size() << "\n";
    std::cout << "Digits      : ";
    for (char c : input) std::cout << c << " ";

    std::vector<int> d;
    for (char c : input) d.push_back(c - '0');

    // Double every second digit from the right, skipping the check digit
    for (int i = static_cast<int>(d.size()) - 2; i >= 0; i -= 2) d[i] *= 2;
    std::cout << "\n\n[Step 1] Double every second digit from the right:\n         ";
    for (int x : d) std::cout << x << " ";

    for (int& x : d) if (x > 9) x -= 9;
    std::cout << "\n\n[Step 2] Subtract 9 from values > 9:\n         ";
    for (int x : d) std::cout << x << " ";

    const int total = std::accumulate(d.begin(), d.end(), 0);
    std::cout << "\n\n[Step 3] Total sum : " << total << "  |  mod 10 : " << (total % 10)
              << "\n\nResult --> Luhn Checksum: " << (total % 10 == 0 ? "VALID" : "INVALID") << "\n";
}

// -----------------------------------------------------------------------
// Mode 2: Generate check digit for a partial number
// -----------------------------------------------------------------------

static void runCheckDigit() {
    std::string input;
    std::cout << "Enter the partial number (without check digit): ";
    std::cin >> input;
    input = sanitize(input);

    if (!isDigitsOnly(input)) { std::cerr << "\nError: Digits only.\n"; return; }
    if (input.size() < 12 || input.size() > 18) {
        std::cerr << "\nError: Expected 12–18 digits, got " << input.size() << ".\n"; return;
    }

    std::cout << "\nPartial number : ";
    for (char c : input) std::cout << c << " ";
    std::cout << "\nDigit count    : " << input.size() << "\n";

    std::vector<int> d;
    for (char c : input) d.push_back(c - '0');

    // Double starting from the rightmost digit of the partial number
    for (int i = static_cast<int>(d.size()) - 1; i >= 0; i -= 2) d[i] *= 2;
    std::cout << "\n[Step 1] Double every second digit from the right:\n         ";
    for (int x : d) std::cout << x << " ";

    for (int& x : d) if (x > 9) x -= 9;
    std::cout << "\n\n[Step 2] Subtract 9 from values > 9:\n         ";
    for (int x : d) std::cout << x << " ";

    const int total      = std::accumulate(d.begin(), d.end(), 0);
    const int checkDigit = (10 - (total % 10)) % 10;
    std::cout << "\n\n[Step 3] Sum : " << total
              << "  |  Check digit = (10 - " << (total % 10) << ") mod 10 = " << checkDigit
              << "\n\nResult --> Check Digit : " << checkDigit
              << "\n           Full number : " << input << checkDigit << "\n";
}

// -----------------------------------------------------------------------
// main
// -----------------------------------------------------------------------

int main() {
    std::cout << "================================\n";
    std::cout << "  Luhn Algorithm\n";
    std::cout << "================================\n";
    std::cout << "\n[1] Validate a complete number\n";
    std::cout << "[2] Generate a check digit\n";
    std::cout << "\nChoice (1/2): ";

    char choice;
    std::cin >> choice;
    std::cout << "\n";

    switch (choice) {
        case '1': runValidate();   break;
        case '2': runCheckDigit(); break;
        default:  std::cerr << "Invalid choice.\n"; return 1;
    }

    return 0;
}
