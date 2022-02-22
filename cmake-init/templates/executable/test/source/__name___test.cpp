{% if pm %}#include <catch2/catch.hpp>

{% end %}#include "lib.hpp"
{% if pm %}
TEST_CASE("Name is {= name =}", "[library]")
{
  library lib;
  REQUIRE(lib.name == "{= name =}");
}{% else %}

auto main() -> int
{
  library lib;

  return lib.name == "{= name =}" ? 0 : 1;
}{% end %}
