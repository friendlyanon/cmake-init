#include <string>

#include <%(name)s/%(name)s.h>

exported_class::exported_class() : name_("%(name)s") {}

const char* exported_class::name() {
  return name_.c_str();
}
