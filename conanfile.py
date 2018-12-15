from conans import ConanFile, CMake, tools
import sys, os, shutil

class QuazipConan(ConanFile):
    name = "quazip"
    version = "0.7.6"
    license = "LGPL-2.1, zlib/png"
    url = "https://github.com/altairwei/conan-quazip"
    description = "A Qt/C++ wrapper for Gilles Vollant's ZIP/UNZIP C package (minizip). Provides access to ZIP archives from Qt programs using QIODevice API."
    settings = "os", "compiler", "build_type", "arch"
    requires = "zlib/1.2.11@conan/stable"
    options = {
        "shared": [True, False]
    }
    default_options = {
        "shared": False,
        "zlib:shared": False
    }
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake_find_package"
    _source_subfolder = "source_subfolder"

    def source(self):
        url = 'https://github.com/stachenov/quazip/archive/%s.tar.gz' % self.version
        tools.get(url)
        os.rename("quazip-" + self.version, self._source_subfolder)
        os.rename(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                  os.path.join(self._source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("CMakeLists.txt",
                    os.path.join(self._source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def build_id(self):
        self.info_build.options.shared = "shared_and_static"

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.h", dst="include/quazip", 
            src=os.path.join(self._source_subfolder, "quazip"))
        if self.options.shared:
            self.copy(pattern="*.dll", dst="bin", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", keep_path=False)
        else:
            self.copy(pattern="*quazip5.lib", dst="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        #self.cpp_info.libs = ["quazip5d"] if self.settings.build_type == "Debug" else ["quazip5"]
        self.cpp_info.libs = tools.collect_libs(self)
