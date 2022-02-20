#include "{= name =}/{= name =}.hpp"

auto main() -> int
{
  auto result = name();
  return result == "{= name =}" ? 0 : 1;
}
