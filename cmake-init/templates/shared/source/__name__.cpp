#include <string>

#include "{= name =}/{= name =}.hpp"{% if pm %}

#include <fmt/core.h>{% end %}

exported_class::exported_class()
    : m_name({% if pm %}fmt::format("{}", "{= name =}"){% else %}"{= name =}"{% end %})
{
}

auto exported_class::name() const -> const char*
{
  return m_name.c_str();
}
