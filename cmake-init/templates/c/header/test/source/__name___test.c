#include "%(name)s/%(name)s.h"

#include <string.h>

int main()
{
  return strcmp("%(name)s", header_only_name()) == 0 ? 0 : 1;
}
