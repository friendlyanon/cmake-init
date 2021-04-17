#include <string>

#include <%(name)s/%(name)s.h>

exported_class::exported_class() : name_("%(name)s") {}

std::string exported_class::name() {
  return name_;
}
