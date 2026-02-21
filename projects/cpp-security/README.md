# Secure C++ - Buffer Overflow Prevention & Advanced Security

## Project Overview
This project demonstrates secure C++ development practices, focusing on buffer overflow prevention, memory management, and secure coding principles.

## Key Topics

### 1. Buffer Overflow Vulnerabilities

#### Vulnerable Code Example:
```cpp
#include <cstring>

void copy_user_input(char* buffer, const char* input) {
    strcpy(buffer, input);  // DANGEROUS: No bounds checking
}

int main() {
    char buffer[10];
    copy_user_input(buffer, "This is a very long string that exceeds buffer size");
    return 0;
}
```

**Problem:**
- `strcpy` doesn't check buffer size
- Input exceeds 10 bytes
- Overwrites adjacent memory
- Can overwrite return address on stack (Stack Smashing)
- Attacker can execute arbitrary code

#### Secure Implementation:
```cpp
#include <cstring>
#include <iostream>

bool copy_user_input_safe(char* buffer, size_t buffer_size, const char* input) {
    if (!buffer || !input || buffer_size == 0) {
        return false;
    }
    
    #ifdef _WIN32
        strncpy_s(buffer, buffer_size, input, buffer_size - 1);
    #else
        strncpy(buffer, input, buffer_size - 1);
        buffer[buffer_size - 1] = '\0';
    #endif
    
    return true;
}

int main() {
    char buffer[10];
    const char* user_input = "This is a long string";
    
    if (copy_user_input_safe(buffer, sizeof(buffer), user_input)) {
        std::cout << "Safe copy: " << buffer << std::endl;
    }
    return 0;
}
```

### 2. Memory Safety Issues

#### Stack vs Heap Overflows:

**Stack Overflow:**
```cpp
// Vulnerable to stack smashing
void vulnerable_function() {
    char password[16];
    gets(password);  // NEVER use gets()
    // Attacker overwrites return address
}
```

**Heap Overflow:**
```cpp
// Vulnerable to heap corruption
char* heap_buffer = new char[10];
strcpy(heap_buffer, "Too long string");  // Overflow
delete[] heap_buffer;
```

#### Secure Memory Management:
```cpp
#include <memory>
#include <vector>

// Use std::unique_ptr for automatic cleanup
std::unique_ptr<char[]> secure_buffer(new char[256]);

// Use std::vector for dynamic arrays
std::vector<char> buffer(256);
// Automatic bounds checking with at()
buffer.at(100) = 'x';
```

### 3. Input Validation

#### Vulnerable:
```cpp
void process_user_id(const std::string& user_id) {
    int id = std::stoi(user_id);  // No validation
    query_user(id);
}
```

#### Secure:
```cpp
bool is_valid_user_id(const std::string& user_id) {
    if (user_id.empty() || user_id.length() > 10) {
        return false;
    }
    
    // Check all characters are digits
    for (char c : user_id) {
        if (!std::isdigit(c)) {
            return false;
        }
    }
    
    // Check range
    try {
        int id = std::stoi(user_id);
        return id > 0 && id <= 999999;
    } catch (const std::exception& e) {
        return false;
    }
}

void process_user_id_secure(const std::string& user_id) {
    if (!is_valid_user_id(user_id)) {
        throw std::invalid_argument("Invalid user ID");
    }
    int id = std::stoi(user_id);
    query_user(id);
}
```

### 4. Integer Overflow

#### Vulnerable:
```cpp
void allocate_buffer(int size) {
    if (size > 0 && size < 1000000) {
        // Integer can overflow during calculation
        char* buffer = new char[size * 2];  // size * 2 might overflow
        // Buffer allocated smaller than expected
    }
}
```

#### Secure:
```cpp
#include <limits>

bool safe_multiply(size_t a, size_t b, size_t& result) {
    if (a == 0 || b == 0) {
        result = 0;
        return true;
    }
    
    if (a > std::numeric_limits<size_t>::max() / b) {
        return false;  // Overflow would occur
    }
    
    result = a * b;
    return true;
}

void allocate_buffer_secure(size_t size) {
    const size_t MAX_SIZE = 1000000;
    
    if (size == 0 || size > MAX_SIZE) {
        throw std::invalid_argument("Invalid size");
    }
    
    size_t buffer_size;
    if (!safe_multiply(size, 2, buffer_size)) {
        throw std::overflow_error("Buffer size calculation overflow");
    }
    
    std::unique_ptr<char[]> buffer(new char[buffer_size]);
}
```

### 5. Format String Vulnerabilities

#### Vulnerable:
```cpp
#include <cstdio>

void log_message(const char* user_input) {
    printf(user_input);  // DANGEROUS: user_input controls format
    // Attacker can use %x to read memory
}
```

#### Secure:
```cpp
#include <cstdio>

void log_message_secure(const char* user_input) {
    printf("%s\n", user_input);  // Format string is fixed
}
```

### 6. Secure String Handling

#### Use Modern C++ Features:
```cpp
#include <string>
#include <string_view>

// std::string handles memory automatically
std::string get_user_name() {
    std::string name;
    std::getline(std::cin, name);  // Automatic bounds
    return name;
}

void process_name(std::string_view name) {
    // std::string_view is non-owning, efficient
    if (name.empty() || name.length() > 100) {
        throw std::invalid_argument("Invalid name");
    }
}
```

## Compilation Security Flags

```bash
# Enable all warnings
g++ -Wall -Wextra -Wpedantic

# Enable Address Sanitizer (detects memory errors)
g++ -fsanitize=address -g

# Enable Undefined Behavior Sanitizer
g++ -fsanitize=undefined

# Stack protector against buffer overflows
g++ -fstack-protector-all

# Position Independent Executable (ASLR support)
g++ -fPIE -pie

# Read-only relocation (reduce attack surface)
g++ -Wl,-z,relro,-z,now

# Combined secure compilation
g++ -Wall -Wextra -fsanitize=address,undefined -fstack-protector-all -O2
```

## Security Best Practices

1. **Use Modern C++ Standards** (C++17 or later)
   - `std::string` instead of `char*`
   - `std::vector` instead of raw arrays
   - `std::optional` instead of error codes
   - `std::variant` instead of error codes

2. **Input Validation**
   - Always validate length
   - Validate data type
   - Validate range/format
   - Never trust user input

3. **Memory Management**
   - Use smart pointers (`unique_ptr`, `shared_ptr`)
   - Use RAII principle
   - Avoid raw `new`/`delete`

4. **Error Handling**
   - Use exceptions
   - Don't ignore errors
   - Log security-relevant events

5. **Compilation Flags**
   - Enable all warnings
   - Use sanitizers in development
   - Use position-independent code
   - Enable stack protector

## Testing & Verification

### Compile and Test:
```bash
# Compile vulnerable code with sanitizers
g++ -fsanitize=address,undefined vulnerable.cpp -o vulnerable

# Run with memory checker
./vulnerable

# Use static analysis tools
clang --analyze code.cpp

# Use fuzzing for robustness
afl-fuzz -i inputs -o outputs ./vulnerable
```

## Tools & Resources

- **LLVM/Clang**: Modern compiler with security features
- **AddressSanitizer**: Detects memory errors
- **UBSan**: Undefined behavior detection
- **Valgrind**: Memory debugging tool
- **CppCheck**: Static analysis tool
- **OWASP**: Secure coding guidelines

## References
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [CWE-120: Buffer Copy without Checking Size](https://cwe.mitre.org/data/definitions/120.html)
- [C++ Core Guidelines](https://github.com/isocpp/CppCoreGuidelines)
- [Modern C++ Best Practices](https://github.com/rigtorp/awesome-modern-cpp)

## Last Updated
February 2026
