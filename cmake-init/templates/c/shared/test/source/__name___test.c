{% if pm %}#include <memory>
#include <string>

#include <catch2/catch.hpp>

{% end %}#include "{= name =}/{= name =}.h"
{% if pm %}
TEST_CASE("Name is {= name =}", "[library]")
{
  auto name_ptr = std::unique_ptr<const char>(exported_function());

  REQUIRE(std::string("{= name =}") == name_ptr.get());
}{% else %}
#include <string.h>

int main(int argc, const char* argv[])
{
  (void)argc;
  (void)argv;

  return strcmp(exported_function(), "{= name =}") == 0 ? 0 : 1;
}{% end %}
