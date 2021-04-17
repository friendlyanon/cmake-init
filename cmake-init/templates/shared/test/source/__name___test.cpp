#include <%(name)s/%(name)s.h>

int main() {
  exported_class e;

  return e.name() == "%(name)s" ? 0 : 1;
}
