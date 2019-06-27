cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

find_package(libappimage REQUIRED)
find_package(PkgConfig)
pkg_check_modules(PANGO REQUIRED IMPORTED_TARGET pango pangocairo pangoft2)

pkg_check_modules(GDK_PIXBUF REQUIRED IMPORTED_TARGET gdk-pixbuf-2.0)
pkg_check_modules(LIBFFI REQUIRED IMPORTED_TARGET libffi)

add_executable(example example.cpp)
target_link_libraries(example
    PkgConfig::PANGO
    PkgConfig::GDK_PIXBUF
    PkgConfig::LIBFFI
    libappimage
    )
