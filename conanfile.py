from conans import ConanFile, ConfigureEnvironment
from conans.tools import download, unzip
import os

class caresConan(ConanFile):
    name = "c-ares"
    version = "1.12.0"
    ZIP_FOLDER_NAME = "c-ares-cares-%s" % version.replace(".", "_")
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = ["CARESConfig.cmake"]
    build_policy = "missing"
    url="https://c-ares.haxx.se"
    license="https://c-ares.haxx.se/license.html"
    description="c-ares test Conan package"
    
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
        # Use configure && make in linux and Macos, and nmake in windows
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.run("cd %s && %s ./configure" % (self.ZIP_FOLDER_NAME, env.command_line_env))
            self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, env.command_line_env))
        else:
            # command_line_env comes with /. In Windows, \ are used
            if self.options.shared:
                cfg = "dll-debug" if self.settings.build_type == "Debug" else "dll-release"
                command = ('%s && cd %s && buildconf.bat' % (env.command_line_env, self.ZIP_FOLDER_NAME)) \
                + ('&& nmake /f Makefile.msvc CFG=%s' % cfg)
            else:
                cfg = "lib-debug" if self.settings.build_type == "Debug" else "lib-release"
                command = ('%s && cd %s && buildconf.bat' % (env.command_line_env, self.ZIP_FOLDER_NAME)) \
                + ('&& nmake /f Makefile.msvc CFG=%s' % cfg)
            self.run(command)

    def package(self):
        # Copy CARESConfig.cmake to package
        self.copy("CARESConfig.cmake", dst=".", src=".", keep_path=False)
        
        # Copying headers
        self.copy(pattern="*.h", dst="include", src=self.ZIP_FOLDER_NAME, keep_path=False)
        
        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            print "set option shared? %s" % self.options.shared
            print "copying from %s" % self.ZIP_FOLDER_NAME
            if self.options.shared:
                print "set option shared to true"
                self.copy(pattern="*.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*.dll", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                print "set option shared to false"
                self.copy(pattern="*.lib", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
        else:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="bin", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="bin", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
    
        print "Package settings.os %s" % self.settings.os
        print "Package settings.build_type %s" % self.settings.build_type
        # Define the libraries
        if self.settings.os == "Windows":
            print "Package settings.os set to windows"
            self.cpp_info.libs = ['cares'] if self.options.shared else ['libcares']
            if self.settings.build_type == "Debug":
                print "Package settings.build_type set to debug"
                self.cpp_info.libs[0] += "d"
            self.cpp_info.libs.append('Ws2_32')
            # self.cpp_info.libs.append('wsock32')
        else:
            pass
            
        # Definitions for static build
        if not self.options.shared:
            self.cpp_info.defines.append("CARES_STATICLIB=1")
        