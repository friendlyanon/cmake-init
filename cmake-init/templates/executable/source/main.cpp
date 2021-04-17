#include <iostream>
#include <string>

#include <lib.h>

int main() {
  library lib;
  std::string message = "Hello from " + lib.name + "!";
  std::cout << message << '\n';
  return 0;
}
