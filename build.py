from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    docker_entry_script = \
        "conan remote add appimage https://api.bintray.com/conan/azubieta/AppImage &&" \
        "conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan &&" \
        "sudo apt-get -qq update && sudo apt-get -qq install -y desktop-file-utils libglib2.0-dev"

    builder = ConanMultiPackager(docker_entry_script=docker_entry_script)
    builder.add_common_builds(shared_option_name="libappimage:shared")
    builder.run()
