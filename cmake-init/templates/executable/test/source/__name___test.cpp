#include <lib.h>

auto main() -> int {
  library lib;

  return lib.name == "%(name)s" ? 0 : 1;
}
