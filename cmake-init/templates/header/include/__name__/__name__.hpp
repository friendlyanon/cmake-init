#pragma once

#include <string>

#include <fmt/core.h>

/**
 * @brief Return the name of this header-only library
 */
inline auto name() -> std::string
{
  return fmt::format("{}", "{= name =}");
}
