import setuptools
import subprocess
import os
import re
import shutil

with open("../cmake-init/cmake_init.py") as f:
    for line in f:
        match = re.match("^__version__ = \"([^\"]+)\"$", line)
        if match is not None:
            version = match[1]
            break

os.makedirs("cmake_init_lib", exist_ok=True)

shutil.make_archive(
    "cmake_init_lib/cmake-init",
    "zip",
    "../cmake-init",
    "templates",
    True,
)

shutil.copy("../cmake-init/cmake_init.py", "cmake_init_lib")
shutil.copy("../cmake-init/template.py", "cmake_init_lib")

with open("cmake_init_lib/__init__.py", "w") as f:
    f.write("""\
import os
import zipfile

from .cmake_init import main
from .template import compile_template

def pypi_main():
    zip = zipfile.ZipFile(
        os.path.join(os.path.dirname(__file__), "cmake-init.zip"),
        "r",
    )
    try:
        # open a dummy fd to keep the zip from being closed
        with zip.open("templates/common/.gitignore") as dummy_fp:
            main(zip, compile_template)
    except KeyboardInterrupt:
        pass
""")

with open("cmake_init_lib/__main__.py", "w") as f:
    f.write("""\
from . import pypi_main

if __name__ == "__main__":
    pypi_main()
""")

with open("../README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="cmake-init",
    version=version,
    author="friendlyanon",
    author_email="friendlyanon_@hotmail.com",
    description="The missing CMake project initializer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/friendlyanon/cmake-init",
    packages=["cmake_init_lib"],
    package_data={"cmake_init_lib": ["cmake-init.zip"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
    license="GPLv3+",
    license_files="../COPYING",
    platforms="OS Independent",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["cmake-init = cmake_init_lib:pypi_main"],
    },
)
