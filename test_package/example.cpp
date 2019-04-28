#include <iostream>
#include "appimage/appimage.h"

int main() {
    std::cout <<  "Hello World!" << std::endl;
    printf("RANDOM MD5 calculation using libappimage: %s\n", appimage_get_md5("/"));
}
