#include <iostream>
#include "appimage/appimage.h"

int main() {
    std::cout << appimage_get_md5("/test") << std::endl;
}
