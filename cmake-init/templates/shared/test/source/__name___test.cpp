#include <string>

#include "{= name =}/{= name =}.hpp"

auto main() -> int
{
  exported_class e;

  return std::string("{= name =}") == e.name() ? 0 : 1;
}
