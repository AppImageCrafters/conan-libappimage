from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    command = "sudo apt-get -qq update && " \
              "sudo apt-get -qq install -y libfuse-dev desktop-file-utils libcairo-dev libglib2.0-dev"

    builder = ConanMultiPackager(use_docker=True, docker_image='conanio/gcc49', docker_entry_script=command)
    builder.add_common_builds(shared_option_name="libappimage:shared")
    builder.run()
