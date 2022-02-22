#include <string>

#include <fmt/core.h>

#include "{= name =}/{= name =}.hpp"

exported_class::exported_class()
    : m_name(fmt::format("{}", "{= name =}"))
{
}

auto exported_class::name() const -> const char*
{
  return m_name.c_str();
}
