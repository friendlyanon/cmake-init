{% if pm %}#include <catch2/catch.hpp>

{% end %}#include "lib.hpp"
{% if pm %}
TEST_CASE("Name is {= name =}", "[library]")
{
  auto const lib = library {};
  REQUIRE(lib.name == "{= name =}");
}{% else %}
auto main() -> int
{
  auto const lib = library {};

  return lib.name == "{= name =}" ? 0 : 1;
}{% end %}
