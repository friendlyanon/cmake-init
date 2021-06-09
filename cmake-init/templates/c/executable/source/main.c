#include <lib.h>
#include <stdio.h>

int main()
{
  library lib = create_library();
  printf("Hello from %%s!", lib.name);
  return 0;
}
