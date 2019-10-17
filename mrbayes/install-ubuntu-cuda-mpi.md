# Guide to install [MrBayes](https://github.com/NBISweden/MrBayes) with Cuda, OpenCL and MPI on Ubuntu
# Requeriments
You need and Ubuntu 18.04 installation with an Nvidia CUDA compatible cards or any Card OpenCL compatible.

Be in mind, this install are tested to Nvidia card and are expect to work as OpenCL compatible card too.

I don't have a AMD card. When I get one in hand I will make the install adjustments to work with.

# Installation Steps
## 1. Install basic libaries
```sh
sudo apt-get install -y libtool autoconf make g+ git libread line-dev build-essential doxygen git
sudo apt-get install -y default-jdk
sudo apt-get install -y ocl-icd-opencl-dev pocl-opencl-icd opencl-headers
sudo apt-get install -y openmpi-bin openmpi-doc libopenmpi-dev 
sudo apt-get install -y libmpich-mpd1.0-dev libmpich-shmem1.0-dev libmpich1.0-dev libblacs-mpi-dev
```
### 2. Install CUDA
```sh
cd ~/Downloads
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.1.168-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804_10.1.168-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo apt-get update
sudo apt-get install -y cuda
```
### 3. Install latest NVIDIA Drivers
This step are necessary even if already has NVIDIA driver installed, to check if you has the latest Nvidia Driver installed. You need to select the latest and greatest version. And Reboot to take effect.
```sh
pkexec driver-manager
sudo reboot
``` 
Now you can check if Nvidia driver and CUDA installation are Ok. By
```sh
nvidia-smi
```
### 4. Install BEAGLE from git
```sh
git clone --depth=1 https://github.com/beagle-dev/beagle-lib.git
cd beagle-lib
./autogen.sh
./configure --prefix=/usr/local
make
sudo make install
cd ..
```
#### 4.1 Update Library path and make it global
```sh
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
sudo echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> /etc/bash.bashrc
sudo echo "export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH" >> /etc/bash.bashrc
```
#### 4.2 Verify if BEAGLE install is Ok
```sh
make check
```
### 5 Install MrBayes from git
```sh
git clone --depth=1 https://github.com/NBISweden/MrBayes.git
cd MrBayes
./configure --with-mpi
make
sudo make install
cd ..
```

