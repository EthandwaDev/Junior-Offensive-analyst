// Vulnerable C++ Code - Buffer Overflow Examples
// EDUCATIONAL PURPOSES ONLY - DO NOT USE IN PRODUCTION

#include <iostream>
#include <cstring>
#include <cstdio>

// Vulnerable Function 1: strcpy without bounds checking
void vulnerable_copy_username(char* dest) {
    std::cout << "Enter username (max 20 chars): ";
    char user_input[256];
    std::cin.getline(user_input, sizeof(user_input));
    
    strcpy(dest, user_input);  // VULNERABLE: No buffer size check
}

// Vulnerable Function 2: Buffer on stack - Stack Smashing
void vulnerable_stack_function() {
    char password[16];
    std::cout << "Enter password: ";
    
    #ifdef _WIN32
        gets_s(password);  // Still risky even with _s
    #else
        gets(password);  // EXTREMELY DANGEROUS
    #endif
    
    std::cout << "Password: " << password << std::endl;
}

// Vulnerable Function 3: Format string vulnerability
void vulnerable_log(const char* user_message) {
    printf(user_message);  // DANGEROUS: User controls format string
}

// Vulnerable Function 4: Integer overflow in calculation
void vulnerable_allocation(int count) {
    if (count > 0 && count < 10000) {
        // Integer overflow possible here
        int size = count * sizeof(int);  // If count is large, size overflows
        int* arr = new int[size];
        // ...use arr
        delete[] arr;
    }
}

// Vulnerable Function 5: Off-by-one error
void vulnerable_array_access() {
    char buffer[10];
    for (int i = 0; i <= 10; ++i) {  // Should be i < 10
        buffer[i] = 'A';  // Accesses buffer[10] - out of bounds
    }
}

// Vulnerable Function 6: Command injection
void vulnerable_system_call(const char* filename) {
    char command[256];
    sprintf(command, "cat %s", filename);  // DANGEROUS: No validation
    system(command);  // Attacker can inject commands
}

int main() {
    std::cout << "=== VULNERABLE CODE EXAMPLES ===" << std::endl;
    std::cout << "These are for educational purposes only!" << std::endl;
    std::cout << "Do NOT use this code in production!" << std::endl;
    
    char username[20];
    
    // Uncommenting below would demonstrate vulnerabilities:
    // vulnerable_copy_username(username);  // Buffer overflow
    // vulnerable_stack_function();          // Stack smashing
    // vulnerable_log("%x %x %x");           // Format string
    // vulnerable_allocation(5000000);       // Integer overflow
    // vulnerable_array_access();            // Out of bounds
    // vulnerable_system_call("test.txt");   // Command injection
    
    std::cout << "\nView secure_examples.cpp for secure implementations" << std::endl;
    
    return 0;
}
