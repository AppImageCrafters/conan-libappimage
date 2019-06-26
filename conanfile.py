from conans import ConanFile, CMake, tools
from shutil import copyfile
import os


class LibappimageConan(ConanFile):
    name = "libappimage"
    version = "1.0.2"
    license = "[LICENSE]"
    author = "Alexis Lopez Zubieta <contact@azubieta.net>"
    url = "https://github.com/appimage-conan-community/conan-libappimage"
    description = "Core library of the AppImage project. Reference implementation of the AppImage specification."
    topics = ("appimage",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = ("cmake", "pkg_config")
    build_requires = ("gtest/1.8.1@bincrafters/stable",
                      "cmake_installer/3.13.0@conan/stable")
    exports_sources = "patches/*"

    def system_requirements(self):
        pkgs_name = None
        if tools.os_info.linux_distro == "ubuntu":
            pkgs_name = ["desktop-file-utils", "libffi-dev", "gtk-doc-tools"]

        if pkgs_name:
            installer = tools.SystemPackageTool()
            for pkg_name in pkgs_name:
                installer.install(pkg_name)

    def requirements(self):
        self.requires("squashfuse/0.1.103@appimage-conan-community/stable", "private")
        self.requires("libarchive/3.3.3@appimage-conan-community/stable", "private")
        self.requires("xdg-utils-cxx/0.1.1@appimage-conan-community/stable", "private")
        self.requires("librsvg/2.40.20@appimage-conan-community/stable")
        self.requires("zlib/1.2.11@conan/stable")
        self.requires("boost_filesystem/1.69.0@bincrafters/stable")
        self.requires("boost_algorithm/1.69.0@bincrafters/stable")
        self.requires("boost_iostreams/1.69.0@bincrafters/stable")
        self.requires("cmake_findboost_modular/1.69.0@bincrafters/stable")

    def configure(self):
        self.options["squashfuse"].shared = False
        self.options["libarchive"].shared = False
        self.options["xdg-utils-cxx"].shared = False
        self.options["xdg-utils-cxx"].fPIC = True
        self.options["cairo"].shared = True
        self.options["pango"].shared = True
        self.options["librsvg"].shared = True
        self.options["glib"].shared = True
        self.options["zlib"].shared = True

    def source(self):
        self.run("git clone https://github.com/AppImage/libappimage.git --branch=v%s" % self.version)
        tools.patch(base_path="libappimage", patch_file="patches/use_conan.patch")

    def import_pkg_config_files(self, pkg, pkgconfig_path):
        for root, dirs, files in os.walk(self.deps_cpp_info[pkg].rootpath):
            for file in files:
                if file.endswith("pc"):
                    source_path = os.path.join(root, file)
                    target_path = os.path.join(pkgconfig_path, file)
                    print("Importing pkg_config file: %s" % target_path)
                    copyfile(source_path, target_path)
                    tools.replace_prefix_in_pc_file(target_path, self.deps_cpp_info[pkg].rootpath)

    def build(self):
        for lib in self.deps_cpp_info.deps:
            self.import_pkg_config_files(lib, self.build_folder)

        with tools.environment_append({'PKG_CONFIG_PATH': self.build_folder}):
            cmake = CMake(self)
            cmake.definitions["USE_CONAN"] = True
            cmake.definitions["USE_SYSTEM_XZ"] = True
            cmake.definitions["USE_SYSTEM_SQUASHFUSE"] = True
            cmake.definitions["USE_SYSTEM_LIBARCHIVE"] = True
            cmake.definitions["USE_SYSTEM_BOOST"] = True
            cmake.definitions["USE_SYSTEM_XDGUTILS"] = True
            cmake.definitions["BUILD_TESTING"] = False
            cmake.configure(source_folder="libappimage")
            cmake.build()
            cmake.install()

    def package_info(self):
        self.cpp_info.builddirs = ["lib/cmake/libappimage/"]
        common_libs = ["appimage_shared"]
        if (self.options["shared"]):
            self.cpp_info.libs = ["appimage"] + common_libs
        else:
            self.cpp_info.libs = ["appimage_static"] + common_libs
