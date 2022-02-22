{% if pm %}#include <catch2/catch.hpp>

{% end %}#include "{= name =}/{= name =}.hpp"
{% if pm %}
TEST_CASE("Name is {= name =}", "[library]")
{
  REQUIRE(name() == "{= name =}");
}{% else %}

auto main() -> int
{
  auto result = name();
  return result == "{= name =}" ? 0 : 1;
}{% end %}
