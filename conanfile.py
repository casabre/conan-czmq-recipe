from conans import ConanFile, CMake, tools
from sys import platform
import re
import os


class CzmqConan(ConanFile):
    name = "czmq"
    version = "4.2.0"
    license = "MPL-2.0"
    url = "https://github.com/zeromq/czmq.git"
    description = "CZMQ - High-level C binding for ØMQ."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False], }
    default_options = {"shared": True,
                       "fPIC": True, }
    generators = "cmake"

    def requirements(self):
        self.requires("libzmq/4.3.2@conan/stable")

    def source(self):
        git = tools.Git()
        git.clone(self.url, "v%s" % self.version, shallow=True)

    def system_requirements(self):
        pass

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder='cmake-build')
        return cmake

    def build(self):
        tools.replace_in_file("CMakeLists.txt", "project(czmq)",
                              '''project(czmq)
                              include(${CMAKE_CURRENT_SOURCE_DIR}/conanbuildinfo.cmake)
                              conan_basic_setup()''')
        env_build = self._configure_cmake()
        env_build.build()
        env_build.test()

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.name = "czmq"
        # Ordered list of include paths
        self.cpp_info.includedirs = ['include']
        # The libs to link against
        self.cpp_info.libs = [
            "libzyre.so"] if self.options.shared else ["libzyre.a"]
        # Directories where libraries can be found
        self.cpp_info.libdirs = ['lib']
        # Directories where resources, data, etc can be found
        self.cpp_info.resdirs = []
        # Directories where executables and shared libs can be found
        self.cpp_info.bindirs = []
        # Directories where sources can be found (debugging, reusing sources)
        self.cpp_info.srcdirs = []
        self.cpp_info.build_modules = []  # Build system utility module files
        self.cpp_info.defines = []  # preprocessor definitions
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cxxflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
        self.cpp_info.system_libs = []  # The system libs to link against
