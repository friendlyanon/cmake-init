#!/bin/bash

set -e

conan profile detect -f

std={= cpp_std =}
if [ "$RUNNER_OS" = Windows ]; then
  std={= msvc_cpp_std =}
fi

profile="$(conan profile path default)"

mv "$profile" "${profile}.bak"
sed 's/^\(compiler\.cppstd=\).\{1,\}$/\1'"$std/" "${profile}.bak" > "$profile"
rm "${profile}.bak"
