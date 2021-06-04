#include <string>

#include <%(name)s/%(name)s.hpp>

auto main() -> int
{
  exported_class e;

  return std::string("%(name)s") == e.name() ? 0 : 1;
}
