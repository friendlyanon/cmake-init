#include <lib.h>
#include <string.h>

int main()
{
  library lib = create_library();

  return strcmp(lib.name, "%(name)s") == 0 ? 0 : 1;
}
