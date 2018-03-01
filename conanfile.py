from conans import ConanFile, AutoToolsBuildEnvironment, tools, CMake
import os
import shutil

class caresConan(ConanFile):
    name = "c-ares"
    version = "1.14.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["FindCARES.cmake"]
    exports_sources = ["CMakeLists.txt"]
    url = "https://github.com/Croydon/conan-c-ares"
    license = "https://c-ares.haxx.se/license.html"
    description = "A C library for asynchronous DNS requests"
    generators = "cmake"
    ZIP_FOLDER_NAME = "c-ares-cares-%s" % version.replace(".", "_")

    def source(self):
        zip_name = "cares-%s.tar.gz" % self.version.replace(".", "_")
        tools.get("https://github.com/c-ares/c-ares/archive/%s" % zip_name, destination=".")
        shutil.move(self.ZIP_FOLDER_NAME, "cares")

    def build(self):
        self.output.info("c-ares build:")
        self.output.info("Shared? %s" % self.options.shared)

        cmake = CMake(self)
        cmake.definitions["CMAKE_BUILD_TYPE"] = "DEBUG" if self.settings.build_type == "Debug" else "RELEASE"
        cmake.definitions["CARES_STATIC"] = "OFF" if self.options.shared else "ON"
        cmake.definitions["CARES_SHARED"] = "OFF" if self.options.shared else "ON"
        cmake.definitions["CARES_STATIC_PIC"] = "ON"
        cmake.definitions["CARES_INSTALL"] = "OFF"
        cmake.configure()
        cmake.build()
        cmake.patch_config_paths()

    def package(self):
        self.copy("FindCARES.cmake", dst=".", src=".", keep_path=False)
        self.copy("c-ares-config.cmake", dst=".", src=".", keep_path=False)
        self.copy("ares_build.h", dst="include", src=".", keep_path=False)
        self.copy("ares_config.h", dst="include", src=".", keep_path=False)
        self.copy(pattern="*.h", dst="include", src=self.ZIP_FOLDER_NAME, keep_path=False)

        # Copying static and dynamic libs
        self.copy(pattern="*.dll", dst="lib", src="bin", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

        self.copy("*", dst="lib/cmake/c-ares", src="CMakeFiles/Export/lib/cmake/c-ares")

    # def package_info(self):
        # Define the libraries
        # if self.settings.os == "Windows":
            # self.cpp_info.libs = ['cares'] if self.options.shared else ['libcares']
            # if self.settings.build_type == "Debug":
            #     self.cpp_info.libs[0] += "d"
            # self.cpp_info.libs.append('Ws2_32')
            # self.cpp_info.libs.append('wsock32')
        # else:
            # pass

        # Definitions for static build
        # if not self.options.shared:
            # self.cpp_info.defines.append("CARES_STATICLIB=1")
