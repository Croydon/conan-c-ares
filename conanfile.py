from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download, unzip
import os


class caresConan(ConanFile):
    name = "c-ares"
    version = "1.12.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["FindCARES.cmake"]
    build_policy = "missing"
    url = "https://github.com/lhcorralo/conan-c-ares"
    license = "https://c-ares.haxx.se/license.html"
    description = "c-ares test Conan package"
    ZIP_FOLDER_NAME = "c-ares-cares-%s" % version.replace(".", "_")

    def config(self):
        # No specific config
        pass

    def source(self):
        # The file is extracted from github. The official release does not have the file msvc_ver.inc, and it does not compile under windows
        zip_name = "cares-%s.tar.gz" % self.version.replace(".", "_")
        download("https://github.com/c-ares/c-ares/archive/%s" % zip_name, zip_name, verify=True)
        unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):

        self.output.info("c-ares build:")
        self.output.info("Shared? %s" % self.options.shared)

        # Use configure && make in linux and Macos, and nmake in windows
        env = AutoToolsBuildEnvironment(self)
        envvars = env.vars

        if self.settings.os == "Linux" or self.settings.os == "Macos":
            with tools.environment_append(envvars):
                if self.options.shared:
                    self.run("cd %s && ./configure" % (self.ZIP_FOLDER_NAME))
                else:
                    self.run("cd %s && ./configure --disable-shared" % (self.ZIP_FOLDER_NAME))

                self.run("cd %s && make" % (self.ZIP_FOLDER_NAME))
        else:
            # Generate the cmake options
            nmake_options = "CFG="
            nmake_options += "dll-" if self.options.shared else "lib-"
            nmake_options += "debug" if self.settings.build_type == "Debug" else "release"
            # Check if it must be built using static CRT
            if(self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd"):
                nmake_options += " RTLIBCFG=static"

            # command_line_env comes with /. In Windows, \ are used
            self.output.info(nmake_options)
            with tools.environment_append(envvars):
                command = ('cd %s && buildconf.bat && nmake /f Makefile.msvc %s' \
                % (self.ZIP_FOLDER_NAME, nmake_options))
                self.run(command)

    def package(self):
        # Copy CARESConfig.cmake to package
        self.copy("FindCARES.cmake", dst=".", src=".", keep_path=False)

        # Copying headers
        self.copy(pattern="*.h", dst="include", src=self.ZIP_FOLDER_NAME, keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*.dll", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="bin", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        # Define the libraries
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['cares'] if self.options.shared else ['libcares']
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += "d"
            self.cpp_info.libs.append('Ws2_32')
            # self.cpp_info.libs.append('wsock32')
        else:
            pass

        # Definitions for static build
        if not self.options.shared:
            self.cpp_info.defines.append("CARES_STATICLIB=1")
