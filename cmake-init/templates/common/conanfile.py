from conan import ConanFile


class Recipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps", "VirtualRunEnv"
    default_options = {
        "catch2/*:with_main": True,
    }

    def layout(self):
        self.folders.generators = "conan"

    def requirements(self):{% if c %}{% if exe %}
        self.requires("hedley/15"){% end %}
        self.requires("json-c/0.15"){% else %}
        self.requires("fmt/8.1.1"){% end %}

        # Testing only dependencies below
        self.requires("catch2/2.13.8")
