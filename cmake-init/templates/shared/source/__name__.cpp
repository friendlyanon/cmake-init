#include <string>

#include <%(name)s/%(name)s.hpp>

exported_class::exported_class()
    : name_("%(name)s")
{
}

auto exported_class::name() -> const char*
{
  return name_.c_str();
}
