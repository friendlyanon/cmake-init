#include <string>

#include "{= name =}/{= name =}.hpp"
{% if pm %}
#include <catch2/catch{% if catch3 %}_test_macros{% end %}.hpp>

TEST_CASE("Name is {= name =}", "[library]")
{
  auto const exported = exported_class {};
  REQUIRE(std::string("{= name =}") == exported.name());
}{% else %}
auto main() -> int
{
  auto const exported = exported_class {};

  return std::string("{= name =}") == exported.name() ? 0 : 1;
}{% end %}
