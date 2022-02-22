#include <string>

#include "{= name =}/{= name =}.hpp"{% if pm %}

#include <catch2/catch.hpp>

TEST_CASE("Name is {= name =}", "[library]")
{
  exported_class e;
  REQUIRE(std::string("{= name =}") == e.name());
}{% else %}
auto main() -> int
{
  exported_class e;

  return std::string("{= name =}") == e.name() ? 0 : 1;
}{% end %}
