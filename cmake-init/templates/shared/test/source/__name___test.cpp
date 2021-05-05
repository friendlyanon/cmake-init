#include <string>

#include <%(name)s/%(name)s.h>

int main() {
  exported_class e;

  return std::string("%(name)s") == e.name() ? 0 : 1;
}
