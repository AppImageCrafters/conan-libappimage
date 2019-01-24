from conans import ConanFile, CMake, tools
import os


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
    default_options = "shared=True"
    generators = "cmake"
    build_requires = ["gtest/1.8.1@bincrafters/stable"]
    exports_sources = "patches/*"

    def requirements(self):
        self.requires("squashfuse/0.1.103@azubieta/testing")
        self.requires("cairo/1.15.14@bincrafters/stable")
        self.requires("libarchive/3.3.3@azubieta/testing")

    def configure(self):
        self.options["squashfuse"].shared = False
        self.options["libarchive"].shared = False

    def source(self):
        self.run("git clone https://github.com/AppImage/libappimage.git")
        self.run("cd libappimage && git checkout v0.1.8 && git submodule update --init --recursive")
        tools.patch(base_path="libappimage", patch_file="patches/use_conan.patch")

    def build(self):
        cmake = CMake(self)
        config_args = ["-DUSE_SYSTEM_LIBARCHIVE=On", "-DUSE_SYSTEM_SQUASHFUSE=On", "-DUSE_SYSTEM_XZ=On"]
        cmake.configure(source_folder="libappimage", args=config_args)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="libappimage/include")
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)

    def package_info(self):
        common_libs = ["appimage_shared", "xdg-basedir", "glib-2.0", "gio-2.0", "gobject-2.0", "z", "lzma", "cairo"]
        if (self.options["shared"]):
            self.cpp_info.libs = ["appimage"] + common_libs
        else:
            self.cpp_info.libs = ["appimage_static"] + common_libs
