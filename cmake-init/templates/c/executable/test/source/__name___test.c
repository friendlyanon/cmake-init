#include <string.h>

#include "lib.h"

int main(int argc, const char* argv[])
{
  (void)argc;
  (void)argv;

  library lib = create_library();

  return strcmp(lib.name, "%(name)s") == 0 ? 0 : 1;
}
