#include <lib.h>

int main() {
  library lib;

  return lib.name == "%(name)s" ? 0 : 1;
}
