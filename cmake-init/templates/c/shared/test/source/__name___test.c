#include "%(name)s/%(name)s.h"

#include <string.h>

int main(int argc, const char* argv[])
{
  (void)argc;
  (void)argv;

  return strcmp("%(name)s", exported_function()) == 0 ? 0 : 1;
}
