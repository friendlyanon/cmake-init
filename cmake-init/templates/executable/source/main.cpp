#include <iostream>
#include <string>

#include "lib.hpp"

auto main() -> int
{
  library lib;
  std::string message = "Hello from " + lib.name + "!";
  std::cout << message << '\n';
  return 0;
}
