#include "lib.hpp"

auto main() -> int
{
  library lib;

  return lib.name == "{= name =}" ? 0 : 1;
}
