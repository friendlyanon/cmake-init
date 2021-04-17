#pragma once

#include <string>

#include <%(name)s/%(name)s_export.h>

class %(uc_name)s_EXPORT exported_class {
public:
  exported_class();

  std::string name();

private:
  std::string name_;
};
