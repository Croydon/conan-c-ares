from conans import ConanFile, CMake
import os

# This easily allows to copy the package in other user or channel
username = os.getenv("CONAN_USERNAME", "inexorgame")
channel = os.getenv("CONAN_CHANNEL", "testing")


class caresReuseConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "c-ares/1.12.0@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        self.run('cmake "%s" %s' % (self.build_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        # Copy shared libraries
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        # equal to ./bin/greet, but portable win: .\bin\greet
        self.run(os.sep.join([".","bin", "ahost.exe 127.0.0.1"]))
