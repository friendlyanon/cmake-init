#include "{= name =}/{= name =}.h"

#include <string.h>

int main(int argc, const char* argv[])
{
  (void)argc;
  (void)argv;

  return strcmp("{= name =}", header_only_name()) == 0 ? 0 : 1;
}
