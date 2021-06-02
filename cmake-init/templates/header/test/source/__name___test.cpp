#include <%(name)s/%(name)s.h>

auto main() -> int {
  auto result = name();
  return result == "%(name)s" ? 0 : 1;
}
