#include <lib.hpp>

auto main() -> int
{
  library lib;

  return lib.name == "%(name)s" ? 0 : 1;
}
