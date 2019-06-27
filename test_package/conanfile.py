import os
from shutil import copyfile
from conans import ConanFile, CMake, tools


class LibappimageTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    build_requires = "cmake_installer/3.13.0@conan/stable"
    generators = ("cmake_paths", "pkg_config")

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
            cmake.definitions["CMAKE_PROJECT_PackageTest_INCLUDE"] = self.build_folder + "/conan_paths.cmake"
            cmake.configure()
            cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(".%sexample" % os.sep)
