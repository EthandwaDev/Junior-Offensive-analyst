// Secure C++ Code - Buffer Overflow Prevention
// BEST PRACTICES FOR SECURE IMPLEMENTATION

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <cstring>
#include <limits>
#include <stdexcept>

// Secure Function 1: Safe string copy using std::string
void secure_copy_username(std::string& dest) {
    std::cout << "Enter username (max 50 chars): ";
    std::getline(std::cin, dest);  // std::string handles size automatically
    
    if (dest.empty() || dest.length() > 50) {
        throw std::invalid_argument("Username must be 1-50 characters");
    }
}

// Secure Function 2: Safe C-style string copy with bounds checking
bool secure_copy_username_c_style(char* dest, size_t dest_size, const char* src) {
    if (!dest || !src || dest_size == 0) {
        return false;
    }
    
    // strncpy_s is Windows-specific MSVC function
    #ifdef _MSC_VER
        errno_t err = strncpy_s(dest, dest_size, src, dest_size - 1);
        return err == 0;
    #else
        // POSIX approach
        strncpy(dest, src, dest_size - 1);
        dest[dest_size - 1] = '\0';  // Ensure null termination
        return true;
    #endif
}

// Secure Function 3: Safe password input without storing in plain
std::string get_secure_password() {
    std::string password;
    std::cout << "Enter password: ";
    std::getline(std::cin, password);
    
    if (password.empty() || password.length() > 255) {
        throw std::invalid_argument("Invalid password length");
    }
    
    return password;
}

// Secure Function 4: Logging with fixed format string
void secure_log(const std::string& message) {
    if (message.length() > 1000) {
        std::cerr << "Message too long to log" << std::endl;
        return;
    }
    
    // Format string is controlled by code, not user
    printf("[LOG] %s\n", message.c_str());
}

// Secure Function 5: Safe integer multiplication check
bool safe_multiply(size_t a, size_t b, size_t& result) {
    if (a == 0 || b == 0) {
        result = 0;
        return true;
    }
    
    // Check if multiplication would overflow
    if (a > std::numeric_limits<size_t>::max() / b) {
        return false;  // Overflow detected
    }
    
    result = a * b;
    return true;
}

// Secure Function 6: Safe array allocation with overflow protection
std::vector<int> secure_allocate(size_t count) {
    const size_t MAX_ELEMENTS = 1000000;
    
    if (count == 0 || count > MAX_ELEMENTS) {
        throw std::invalid_argument("Invalid element count");
    }
    
    // std::vector handles all memory management
    return std::vector<int>(count);
}

// Secure Function 7: Safe buffer access with bounds checking
void secure_array_access() {
    std::vector<char> buffer(10);  // Safer than char[10]
    
    // Using proper bounds
    for (size_t i = 0; i < buffer.size(); ++i) {
        buffer[i] = 'A';  // Safe: i is always < size
    }
}

// Secure Function 8: Shell command execution protection
bool safe_execute_command(const std::string& filename) {
    // Input validation
    if (filename.empty() || filename.length() > 255) {
        return false;
    }
    
    // Check for dangerous characters
    for (char c : filename) {
        if (c == ';' || c == '|' || c == '&' || c == '$' || c == '`') {
            std::cerr << "Invalid characters in filename" << std::endl;
            return false;
        }
    }
    
    // Alternative: Use system library with proper escaping
    // Or better: Use direct file operations instead of system()
    std::string safe_command = std::string("cat ./") + filename;
    // system(safe_command.c_str());
    
    return true;
}

// Secure class for managing buffers
class SecureBuffer {
private:
    std::vector<char> data;
    size_t current_size;
    
public:
    SecureBuffer(size_t capacity) : data(capacity), current_size(0) {}
    
    bool write(const std::string& str) {
        if (current_size + str.length() > data.size()) {
            return false;  // Buffer full
        }
        
        std::copy(str.begin(), str.end(), data.begin() + current_size);
        current_size += str.length();
        data[current_size] = '\0';
        return true;
    }
    
    const char* get_data() const {
        return data.data();
    }
    
    size_t get_size() const {
        return current_size;
    }
    
    void clear() {
        std::fill(data.begin(), data.end(), '\0');
        current_size = 0;
    }
};

// Secure Function 9: Using smart pointers for dynamic allocation
void secure_dynamic_allocation() {
    size_t size = 256;
    
    // std::unique_ptr automatically deletes when out of scope
    std::unique_ptr<char[]> buffer(new char[size]);
    std::memset(buffer.get(), 0, size);
    
    // Use buffer...
    std::cout << "Buffer allocated securely" << std::endl;
    // Automatic cleanup here - no memory leak
}

// Secure Function 10: Input validation helper
bool is_valid_email(const std::string& email) {
    // Simple email validation
    if (email.empty() || email.length() > 255) {
        return false;
    }
    
    // Check for @ and .
    size_t at_pos = email.find('@');
    size_t dot_pos = email.rfind('.');
    
    if (at_pos == std::string::npos || dot_pos == std::string::npos) {
        return false;
    }
    
    if (at_pos == 0 || dot_pos <= at_pos + 1 || dot_pos == email.length() - 1) {
        return false;
    }
    
    return true;
}

int main() {
    try {
        std::cout << "=== SECURE C++ CODE EXAMPLES ===" << std::endl;
        std::cout << "Best practices for secure implementation" << std::endl << std::endl;
        
        // Example 1: String handling
        std::string username;
        std::cout << "Example 1: Secure username entry" << std::endl;
        // secure_copy_username(username);
        
        // Example 2: Safe multiplication
        std::cout << "\nExample 2: Safe integer multiplication" << std::endl;
        size_t result;
        if (safe_multiply(1000, 1000, result)) {
            std::cout << "1000 * 1000 = " << result << std::endl;
        }
        
        // Example 3: Vector allocation
        std::cout << "\nExample 3: Safe vector allocation" << std::endl;
        auto vec = secure_allocate(100);
        std::cout << "Allocated " << vec.size() << " elements safely" << std::endl;
        
        // Example 4: Secure buffer class
        std::cout << "\nExample 4: Secure buffer class" << std::endl;
        SecureBuffer sb(100);
        sb.write("Secure message");
        std::cout << "Buffer contains: " << sb.get_data() << std::endl;
        
        // Example 5: Email validation
        std::cout << "\nExample 5: Input validation" << std::endl;
        std::string email = "user@example.com";
        if (is_valid_email(email)) {
            std::cout << "Email is valid" << std::endl;
        }
        
        std::cout << "\nAll examples completed successfully!" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}

/* Compilation Instructions:
 * 
 * Basic compilation:
 * g++ -std=c++17 -Wall -Wextra -o secure secure.cpp
 * 
 * With sanitizers (recommended for development):
 * g++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined -o secure secure.cpp
 * 
 * With all security flags:
 * g++ -std=c++17 -Wall -Wextra -O2 -fstack-protector-all -fPIE -pie \
 *     -fsanitize=address,undefined -o secure secure.cpp
 * 
 * Run:
 * ./secure
 */
