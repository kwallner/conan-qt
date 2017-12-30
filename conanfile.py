
import os
from distutils.spawn import find_executable
from conans import AutoToolsBuildEnvironment, ConanFile, tools, VisualStudioBuildEnvironment
from conans.tools import cpu_count

class QtConan(ConanFile):
    """ Qt Conan package """
    name = "Qt"
    version = "5.9.3"
    description = "Conan.io package for Qt library."
    source_dir = "qt5"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "activeqt": [True, False], # Only supported on windows
        "canvas3d": [True, False],
        "connectivity": [True, False],
        "gamepad": [True, False],
        "graphicaleffects": [True, False],
        "imageformats": [True, False],
        "location": [True, False],
        "serialport": [True, False],
        "svg": [True, False],
        "tools": [True, False],
        "translations": [True, False],
        "webengine": [True, False],
        "websockets": [True, False],
        "xmlpatterns": [True, False],
        # Third party libraries: See http://doc.qt.io/qt-5/configure-options.html
        "opengl": ["no", "desktop", "dynamic", "es2" ], # FIXME: es2 seems to be the default for windows
        "openssl": ["no", "runtime", "linked"],
        "zlib": ["qt", "system" ], # Yet only system is supported
        "libjpeg": ["qt", "system" ], # Yet only system is supported
        "libpng": ["qt", "system" ], # Yet only system is supported
        "xcb": ["qt", "system" ], # Yet only system is supported
        "xkbcommon": ["qt", "system" ], # Yet only system is supported
        "freetype": ["qt", "system" ], # Yet only system is supported
        "pcre": ["qt", "system" ], # Yet only system is supported
        "harfbuzz": ["qt", "system" ] # Yet only system is supported
    }
    default_options = \
        "shared=True", \
        "activeqt=False", \
        "canvas3d=False", \
        "connectivity=False", \
        "gamepad=False", \
        "graphicaleffects=False", \
        "imageformats=False", \
        "location=False", \
        "serialport=False", \
        "svg=False", \
        "tools=False", \
        "translations=False", \
        "webengine=False", \
        "websockets=False", \
        "xmlpatterns=False", \
        "opengl=desktop", \
        "openssl=linked", \
        "zlib=qt", \
        "libjpeg=qt", \
        "libpng=qt", \
        "xcb=qt", \
        "xkbcommon=qt", \
        "freetype=qt", \
        "pcre=qt", \
        "harfbuzz=qt", 
    url = "http://github.com/kwallner/conan-qt"
    license = "http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True
    

    def config_options(self):
        #if self.settings.os != "Windows":
        #    del self.options.opengl
        #    del self.options.openssl
        pass

    def requirements(self):
        self.output.info("Option for openssl is %s" % self.options.openssl)
        if self.options.openssl == "linked":
            self.requires("OpenSSL/1.0.2m@conan/stable")

    def source(self):
        submodules = ["qtbase"]

        if self.options.activeqt:
            submodules.append("qtactiveqt")
        if self.options.canvas3d:
            submodules.append("qtcanvas3d")
        if self.options.connectivity:
            submodules.append("qtconnectivity")
        if self.options.gamepad:
            submodules.append("qtgamepad")
        if self.options.graphicaleffects:
            submodules.append("qtgraphicaleffects")
        if self.options.imageformats:
            submodules.append("qtimageformats")
        if self.options.location:
            submodules.append("qtlocation")
        if self.options.serialport:
            submodules.append("qtserialport")
        if self.options.svg:
            submodules.append("qtsvg")
        if self.options.tools:
            submodules.append("qttools")
        if self.options.translations:
            submodules.append("qttranslations")
        if self.options.webengine:
            submodules.append("qtwebengine")
        if self.options.websockets:
            submodules.append("qtwebsockets")
        if self.options.xmlpatterns:
            submodules.append("qtxmlpatterns")

        self.run("git clone https://code.qt.io/qt/qt5.git")
        self.run("cd %s && git checkout v%s" % (self.source_dir, self.version))
        self.run("cd %s && git submodule update --init %s" % (self.source_dir, " ".join(submodules)))

        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                for subdir in os.listdir(self.source_dir):
                    if os.path.isfile("%s/%s/configure" % (self.source_dir, subdir)):
                        os.rename("%s/%s/configure" % (self.source_dir, subdir), "%s/%s/configure_orig" % (self.source_dir, subdir))
                os.rename("%s/configure" % self.source_dir, "%s/configure_orig" % self.source_dir)
        else:
            self.run("chmod +x ./%s/configure" % self.source_dir)
            
    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        
        # some useful arguments
        args = [
                "-opensource", 
                "-confirm-license", 
                "-nomake examples", 
                "-nomake tests",
                "-prefix %s" % self.package_folder
                ]
        # static/sharedq
        if self.options.shared:
            args.append("-shared")
        else:
            args.append("-static")
            
        # Debug/Release
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")

        # Add options from requirements
        for include_dir in self.deps_cpp_info.include_paths:
            args += ["-I" + include_dir ]
        for lib_dir in self.deps_cpp_info.lib_paths:
            args += ["-L" + lib_dir ]
        for some_define in self.deps_cpp_info.defines:
            args += ["-D" + some_define ]

        # Partial build options
        
        # zlib
        args += ["-%s-zlib" % self.options.zlib ]
        
        # libjpeg
        args += ["-%s-libjpeg" % self.options.libjpeg ]

        # libpng
        args += ["-%s-zlib" % self.options.libpng ]

        # freetype
        args += ["-%s-zlib" % self.options.freetype ]

        # pcre
        args += ["-%s-zlib" % self.options.pcre ]

        # platform specific
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self._build_msvc(args)
            else:
                self._build_mingw(args)
        else:
            self._build_unix(args)

    def _build_msvc(self, args):
        build_command = find_executable("jom.exe")
        if build_command:
            build_args = ["-j", str(cpu_count())]
        else:
            build_command = "nmake.exe"
            build_args = []
        self.output.info("Using '%s %s' to build" % (build_command, " ".join(build_args)))

        env = {}
        env.update({'PATH': ['%s/qtbase/bin' % self.conanfile_directory,
                             '%s/gnuwin32/bin' % self.conanfile_directory,
                             '%s/qtrepotools/bin' % self.conanfile_directory]})
        # it seems not enough to set the vcvars for older versions
        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.version == "14":
                env.update({'QMAKESPEC': 'win32-msvc2015'})
                args += ["-platform win32-msvc2015"]
            elif self.settings.compiler.version == "12":
                env.update({'QMAKESPEC': 'win32-msvc2013'})
                args += ["-platform win32-msvc2013"]
            elif self.settings.compiler.version == "11":
                env.update({'QMAKESPEC': 'win32-msvc2012'})
                args += ["-platform win32-msvc2012"]
            elif self.settings.compiler.version == "10":
                env.update({'QMAKESPEC': 'win32-msvc2010'})
                args += ["-platform win32-msvc2010"]
            else:
                self.output.error("Unsuppoted plattform")
        
         
        # Unset SHELL variable
        env.update({'SHELL': ''})
        env.update({'QMAKESPEC': ''})

        env_build = VisualStudioBuildEnvironment(self)
        env.update(env_build.vars)

        # Workaround for conan-io/conan#1408
        for name, value in env.items():
            if not value:
                del env[name]
        with tools.environment_append(env):
            vcvars = tools.vcvars_command(self.settings)

            args += ["-opengl %s" % self.options.opengl]
            
            if self.options.openssl == "no":
                args += ["-no-openssl"]
            elif self.options.openssl == "runtime":
                args += ["-openssl-runtime"]
            else:
                args += ["-openssl-linked"]

            self.run("cd %s && %s && set" % (self.source_dir, vcvars))
            #self.output.info("WILL: cd %s && %s && cmd /C configure.bat %s"
            #         % (self.source_dir, vcvars, " ".join(args)))
            #os.system("start cmd /c cmd")                     
            self.run("cd %s && %s && configure %s"
                     % (self.source_dir, vcvars, " ".join(args)))
            self.run("cd %s && %s && %s %s"
                     % (self.source_dir, vcvars, build_command, " ".join(build_args)))
            self.run("cd %s && %s && %s install" % (self.source_dir, vcvars, build_command))

    def _build_mingw(self, args):
        env_build = AutoToolsBuildEnvironment(self)
        env = {'PATH': ['%s/bin' % self.conanfile_directory,
                        '%s/qtbase/bin' % self.conanfile_directory,
                        '%s/gnuwin32/bin' % self.conanfile_directory,
                        '%s/qtrepotools/bin' % self.conanfile_directory],
               'QMAKESPEC': 'win32-g++'}
        env.update(env_build.vars)
        with tools.environment_append(env):
            # Workaround for configure using clang first if in the path
            new_path = []
            for item in os.environ['PATH'].split(';'):
                if item != 'C:\\Program Files\\LLVM\\bin':
                    new_path.append(item)
            os.environ['PATH'] = ';'.join(new_path)
            # end workaround
            args += ["-opengl %s" % self.options.opengl,
                     "-platform win32-g++"]
            
            if self.options.openssl == "no":
                args += ["-no-openssl"]
            elif self.options.openssl == "runtime":
                args += ["-openssl-runtime"]
            else:
                args += ["-openssl-linked"]

            self.output.info("Using '%s' threads" % str(cpu_count()))
            self.run("cd %s && configure.bat %s"
                     % (self.source_dir, " ".join(args)))
            self.run("cd %s && mingw32-make -j %s"
                     % (self.source_dir, str(cpu_count())))
            self.run("cd %s && mingw32-make install" % (self.source_dir))

    def _build_unix(self, args):
        # platform
        if self.settings.os == "Linux":
            if self.settings.compiler == "gcc":
                if self.settings.arch == "x86":
                    args += ["-platform linux-g++-32"]
                else:
                    args += ["-platform linux-g++"]
            else:
                args += ["-platform linux-clang"]
        else:
            args += ["-no-framework"]
            if self.settings.arch == "x86":
                args += ["-platform macx-clang-32"]
          
        # openssl
        if self.options.openssl == "no":
            args += ["-no-openssl"]
        else:
            if self.options.openssl == "runtime":
                args += ["-openssl-runtime"]
            else:
                args += ["-openssl-linked"]
            ssl_libs= []
            ssl_libs.append("-lssl")
            ssl_libs.append("-lcrypto")
            ssl_libs.append("-ldl")
            os.environ['OPENSSL_LIBS'] = " ".join(ssl_libs) 
            
        # xcb
        args += ["-%s-zlib" % self.options.xcb ]

        # xkbcommon
        args += ["-%s-zlib" % self.options.xkbcommon ]

        # harfbuzz
        args += ["-%s-zlib" % self.options.harfbuzz ]
                       
        self.output.info("Using '%s' threads" % str(cpu_count()))
        self.run("cd %s && ./configure %s" % (self.source_dir, " ".join(args)))
        self.run("cd %s && make -j %s" % (self.source_dir, str(cpu_count())))
        self.run("cd %s && make install" % (self.source_dir))

    def package_info(self):
        libs = ['Concurrent', 'Core', 'DBus',
                'Gui', 'Network', 'OpenGL',
                'Sql', 'Test', 'Widgets', 'Xml']

        self.cpp_info.libs = []
        self.cpp_info.includedirs = ["include"]
        for lib in libs:
            if self.settings.os == "Windows" and self.settings.build_type == "Debug":
                suffix = "d"
            elif self.settings.os == "Macos" and self.settings.build_type == "Debug":
                suffix = "_debug"
            else:
                suffix = ""
            self.cpp_info.libs += ["Qt5%s%s" % (lib, suffix)]
            self.cpp_info.includedirs += ["include/Qt%s" % lib]

        if self.settings.os == "Windows":
            # Some missing shared libs inside QML and others, but for the test it works
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
