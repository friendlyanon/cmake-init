#include <string>

#include <%(name)s/%(name)s.h>

auto main() -> int
{
  exported_class e;

  return std::string("%(name)s") == e.name() ? 0 : 1;
}
