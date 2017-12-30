Conan package for Qt
--------------------------------------------

[![Build Status](https://travis-ci.org/kwallner/conan-qt.svg?branch=testing/5.8.0)](https://travis-ci.org/kwallner/conan-qt)

[![Build status](https://ci.appveyor.com/api/projects/status/gboj3x82d42eoasw/branch/testing/5.8.0?svg=true)](https://ci.appveyor.com/project/kwallner/conan-qt)

[ ![Download](https://api.bintray.com/packages/kwallner/Conan/Qt%3Akwallner/images/download.svg?version=5.8.0%3Atesting) ](https://bintray.com/kwallner/Conan/Qt%3Akwallner/5.8.0%3Atesting/link)

[Conan.io](https://conan.io) package for [Qt](https://www.qt.io) library. This package includes by default the Qt Base module (Core, Gui, Widgets, Network, ...). Others modules can be added using options.

The packages generated with this **conanfile** can be found in [bintray.com](https://bintray.com/kwallner/Conan).

## Reuse the package

### Basic setup

```
$ conan install Qt/5.9.3@kwallner/testing
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

```
    [requires]
    Qt/5.8.0@kwallner/testing

    [options]
    Qt:shared=true # false
    # On Windows, you can choose the opengl mode, default is 'desktop'
    Qt:opengl=desktop # dynamic
    # If you need specific Qt modules, you can add them as follow:
    Qt:websockets=true
    Qt:xmlpatterns=true

    [generators]
    txt
    cmake
```

Complete the installation of requirements for your project running:

```
    conan install .
```

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

## Develop the package

### Required dependencies (Linux)

For Ubuntu:
apt-get install libgl1-mesa-dev libxcb1 libxcb1-dev \
    libx11-xcb1 libx11-xcb-dev libxcb-keysyms1 \
    libxcb-keysyms1-dev libxcb-image0 libxcb-image0-dev \
    libxcb-shm0 libxcb-shm0-dev libxcb-icccm4 \
    libxcb-icccm4-dev libxcb-sync1 libxcb-sync-dev \
    libxcb-xfixes0-dev libxrender-dev libxcb-shape0-dev \
    libxcb-randr0-dev libxcb-render-util0 libxcb-render-util0-dev \
    libxcb-glx0-dev libxcb-xinerama0 libxcb-xinerama0-dev

### Build packages

    $ pip install conan_package_tools
    $ python build.py

### Upload packages to server

    $ conan upload Qt/5.8.0@kwallner/testing --all
