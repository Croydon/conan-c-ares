from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="inexorgame")
    # Try shared and not-shared builds
    builder.add_common_builds(shared_option_name="c-ares:shared", pure_c=True)
    builder.run()

    # Filter
    # filtered_builds = []
    # for settings, options in builder.builds:
        # if settings["compiler.version"] == "12":
            # filtered_builds.append([settings, options])
    # builder.builds = filtered_builds

    # builder.run()
