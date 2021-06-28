#include <lib.h>
#include <stdio.h>

int main(int argc, const char* argv[])
{
  (void)argc;
  (void)argv;

  library lib = create_library();
  printf("Hello from %%s!", lib.name);
  return 0;
}
