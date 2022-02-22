{% if pm %}#include <memory>
#include <string>

#include <catch2/catch.hpp>{% else %}#include <string.h>{% end %}

{% if pm %}extern "C" {
{% end %}#include "lib.h"
{% if pm %}}

namespace {

struct library_delete
{
  void operator()(void* p) const
  {
    destroy_library(static_cast<library*>(p));
  }
};

} // namespace

TEST_CASE("Name is {= name =}", "[library]")
{
  library lib = create_library();
  auto ptr = std::unique_ptr<library, library_delete>(&lib, {});

  REQUIRE(std::string("{= name =}") == lib.name);
}{% else %}
int main(int argc, const char* argv[])
{
  library lib = create_library();

  (void)argc;
  (void)argv;

  return strcmp(lib.name, "{= name =}") == 0 ? 0 : 1;
}{% end %}
