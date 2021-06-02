#include <string>

#include <%(name)s/%(name)s.h>

exported_class::exported_class() : name_("%(name)s") {}

auto exported_class::name() -> const char* {
  return name_.c_str();
}
