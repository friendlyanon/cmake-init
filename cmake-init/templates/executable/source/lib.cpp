#include "lib.hpp"{% if pm %}

#include <fmt/core.h>{% end %}

library::library()
    : name {{% if pm %}fmt::format("{}", "{= name =}"){% else %}"{= name =}"{% end %}}
{
}
