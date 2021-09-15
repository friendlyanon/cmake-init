#include "%(name)s/%(name)s.hpp"

auto main() -> int
{
  auto result = name();
  return result == "%(name)s" ? 0 : 1;
}
