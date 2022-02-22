#pragma once

#include <string>{% if pm %}

#include <fmt/core.h>{% end %}

/**
 * @brief Return the name of this header-only library
 */
inline auto name() -> std::string
{
  return {% if pm %}fmt::format("{}", "{= name =}"){% else %}"{= name =}"{% end %};
}
