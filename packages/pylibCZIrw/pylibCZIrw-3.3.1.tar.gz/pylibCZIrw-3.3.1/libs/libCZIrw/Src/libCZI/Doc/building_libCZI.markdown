Building libCZI                 {#buildinglibCZI}
===============

libCZI aims to be portable and should build readily using any decent C++ compiler. This repository is leveraging the [CMake](https://cmake.org/) system for building.

Here are some instructions for building on Windows and on Linux.

Building on Windows with Visual Studio
--------------------------------------

Visual Studio has [built-in support](https://docs.microsoft.com/en-us/cpp/build/cmake-projects-in-visual-studio?view=msvc-160) for CMake projects. Executing File->Open Folder... and pointing to the folder where the libCZI-repo is located should give something like this:
![libCZI solution](Images/VisualStudio_cmake1.png "libCZI solution")
@image latex VisualStudio_cmake1.png "libCZI solution"
The project should compile and build without further ado.

For building on the command-line, it is recommended to do an out-of-source build. Executing those commands will execute all steps - go to the folder where the libCZI-repo is located:

    mkdir build
    cd build
    cmake ..
    cmake --build .

Building on Linux
-----------------

When building on Linux, the packages zlib and libpng must be available. If necessary, they can be installed like this (assuming a Debian based distro):

    sudo apt-get install zlib1g-dev
    sudo apt-get install libpng-dev

The same steps as above will build the code - go into the folder where the libCZI-repo is located, and run

    mkdir build
    cd build
    cmake ..
    cmake --build .


Building the documentation
--------------------------

Executing <tt>doxygen</tt> will produce the HTML documentation in the folder ../Src/Build folder.

