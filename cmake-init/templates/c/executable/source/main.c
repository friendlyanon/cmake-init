{% if pm %}#include <stddef.h>
{% end %}#include <stdio.h>

#include "lib.h"

int main(int argc, char const* argv[])
{
  struct library lib = create_library();

  (void)argc;
  (void)argv;
{% if not pm %}
  (void)printf("Hello from %s!", lib.name);{% else %}
  if (lib.name == NULL) {
    (void)puts("Hello from unknown! (JSON parsing failed in library)");
  } else {
    (void)printf("Hello from %s!", lib.name);
  }
  destroy_library(&lib);{% end %}
  return 0;
}
