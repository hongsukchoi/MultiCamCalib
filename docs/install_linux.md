# Ceres installation - Linux 

The most secure way of the installation is following the [official guide](http://ceres-solver.org/installation.html).
The below steps are just for reference, which are tested on Ubuntu 20.04.5 LTS on 09/29/2023.

## 1. Install all the dependencies.
    # CMake
    sudo apt-get install cmake

    # google-glog + gflags
    sudo apt-get install libgoogle-glog-dev libgflags-dev

    # BLAS & LAPACK
    sudo apt-get install libatlas-base-dev

    # Eigen3
    sudo apt-get install libeigen3-dev

    # SuiteSparse and CXSparse (optional)
    sudo apt-get install libsuitesparse-dev

## 2. Download ceres 

    wget http://ceres-solver.org/ceres-solver-2.1.0.tar.gz

## 3. Install ceres 
    
    tar zxf ceres-solver-2.1.0.tar.gz
    mkdir ceres-bin
    cd ceres-bin
    cmake ../ceres-solver-2.1.0
    make -j3
    make test
    # Optionally install Ceres, it can also be exported using CMake which
    # allows Ceres to be used without requiring installation, see the documentation
    # for the EXPORT_BUILD_DIR option for more information.
    make install
