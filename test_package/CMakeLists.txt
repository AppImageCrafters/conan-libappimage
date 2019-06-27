cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

find_package(libappimage REQUIRED)
find_package(PkgConfig)
pkg_check_modules(FREETYPE REQUIRED IMPORTED_TARGET freetype)


add_executable(example example.cpp)
target_link_libraries(example libappimage PkgConfig::FREETYPE)
