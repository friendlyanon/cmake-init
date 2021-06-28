#include <lib.h>

library create_library(void)
{
  library lib;
  lib.name = "%(name)s";
  return lib;
}
