{% if pm %}#include <cstdlib>
#include <memory>
#include <string>
#include <type_traits>

#include <catch2/catch{% if catch3 %}_test_macros{% end %}.hpp>

{% end %}#include "{= name =}/{= name =}.h"
{% if pm %}
template<typename T>
static void c_free(T* ptr)
{
  using U = typename std::remove_cv<T>::type;
  std::free(static_cast<void*>(const_cast<U*>(ptr)));
}

TEST_CASE("Name is {= name =}", "[library]")
{
  using c_string_ptr = std::unique_ptr<const char, void(*)(const char*)>;
  auto name_ptr = c_string_ptr(header_only_name(), &c_free<const char>);

  REQUIRE(std::string("{= name =}") == name_ptr.get());
}{% else %}
#include <string.h>

int main(int argc, const char* argv[])
{
  (void)argc;
  (void)argv;

  return strcmp(header_only_name(), "{= name =}") == 0 ? 0 : 1;
}{% end %}
