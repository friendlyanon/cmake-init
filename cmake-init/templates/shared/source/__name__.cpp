#include <string>

#include <%(name)s/%(name)s.hpp>

exported_class::exported_class()
    : m_name("%(name)s")
{
}

auto exported_class::name() -> const char*
{
  return m_name.c_str();
}
