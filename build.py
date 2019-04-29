from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    remotes = [("https://api.bintray.com/conan/bincrafters/public-conan", "yes", "bincrafters"),
               ("https://api.bintray.com/conan/appimage-conan-community/public-conan", "yes", "appimage"),
               ("https://api.bintray.com/conan/azubieta/AppImage", "yes", "azubieta"),
               ]
    docker_entry_script = \
        "sudo apt-get -qq update && " \
        "sudo apt-get -qq install -m -y desktop-file-utils libffi-dev libglib2.0-dev"

    builder = ConanMultiPackager(build_policy="missing", remotes=remotes, docker_entry_script=docker_entry_script)
    builder.add_common_builds(shared_option_name="libappimage:shared")

    # libstc++11 is required by gtest therefore by the whole build
    for settings, options, env_vars, build_requires, reference in builder.items:
        settings["compiler.libcxx"] = 'libstdc++11'

    builder.run()
