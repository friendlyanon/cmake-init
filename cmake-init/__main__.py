# cmake-init - The missing CMake project initializer
# Copyright (C) 2021  friendlyanon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Website: https://github.com/friendlyanon/cmake-init

import os
import zipfile

from cmake_init import main
from template import compile_template

if __name__ == "__main__":
    zip = zipfile.ZipFile(os.path.dirname(__file__), "r")
    try:
        # open a dummy fd to keep the zip from being closed
        with zip.open("__main__.py") as dummy_fp:
            main(zip, compile_template)
    except KeyboardInterrupt:
        pass
