from conans import ConanFile, CMake, tools


class LibappimageConan(ConanFile):
    name = "libappimage"
    version = "0.1.8"
    license = "[LICENSE]"
    author = "Alexis Lopez Zubieta <contact@azubieta.net>"
    url = "https://github.com/azubieta/conan-libappimage"
    description = "Core library of the AppImage project. Reference implementation of the AppImage specification."
    topics = ("appimage",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/AppImage/libappimage.git")
        self.run("cd libappimage && git checkout v0.1.8 && git submodule update --init --recursive")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="libappimage")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="libappimage/include")
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)

    def package_info(self):
        common_libs = ["appimage_shared", "xdg-basedir", "glib-2.0", "gio-2.0", "gobject-2.0", "archive", "z",
                       "squashfuse", "lzma", "cairo"]
        if (self.options["shared"]):
            self.cpp_info.libs = ["appimage"] + common_libs
        else:
            self.cpp_info.libs = ["appimage_static"] + common_libs
