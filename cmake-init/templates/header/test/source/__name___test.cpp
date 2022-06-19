#include "{= name =}/{= name =}.hpp"
{% if pm %}
#include <catch2/catch{% if catch3 %}_test_macros{% end %}.hpp>

TEST_CASE("Name is {= name =}", "[library]")
{
  REQUIRE(name() == "{= name =}");
}{% else %}
auto main() -> int
{
  auto const result = name();

  return result == "{= name =}" ? 0 : 1;
}{% end %}
