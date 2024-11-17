## Install GCC11.2 Mannually on Ubuntu20

In the case of bad internet connectivity, this is for manually install gcc11.2 on ubuntu20. 

### Prerequisite

```
sudo apt install build-essential manpages-dev software-properties-common gcc g++ make bison binutils gcc-multilib flex
```

### gnu package

```
http://ftp.tsukuba.wide.ad.jp/software/gcc/releases/gcc-11.2.0/gcc-11.2.0.tar.gz
http://ftp.tsukuba.wide.ad.jp/software/gcc/infrastructure/gmp-6.1.0.tar.bz2
http://ftp.tsukuba.wide.ad.jp/software/gcc/infrastructure/isl-0.18.tar.bz2
http://ftp.tsukuba.wide.ad.jp/software/gcc/infrastructure/mpc-1.0.3.tar.gz
http://ftp.tsukuba.wide.ad.jp/software/gcc/infrastructure/mpfr-3.1.6.tar.bz2
```
need 4 packages, 
```
gmp-6.1.0
isl-0.18
mpc-1.0.3
mpfr-3.1.6
```
These are prepared in the gcc-11.2.7z, use the following steps to install

```
mv gcc-11.2.0-tar.gz ~
cd ~
tar xf gcc-11.2.0.tar.gz
cd gcc-11.2.0/
```
Copy the 4 packages(don't extract) under gcc-11.2.0/, and run the script
```
./contrib/download_prerequisites
```
configure the build
```
mkdir build
cd build
../configure configure -v --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu --prefix=/usr/local/gcc-11.2 --enable-checking=release --enable-languages=c,c++ --disable-multilib --program-suffix=-11.2
```
This time, we install the gcc11 into /usr/local/gcc-11.2. Then, we make and make install

```
make -j$(nproc)
```
Make step takes up to 1 hour.

```
sudo make install
```

### Add PATH and LD_LIBRARY_PATH

In ~/.bashrc, add

```
export PATH=/usr/local/gcc-11.2/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/gcc-11.2/lib64:$LD_LIBRARY_PATH
```


### Update Priority

```
sudo update-alternatives --install /usr/bin/gcc gcc /usr/local/gcc-11.2/bin/gcc-11.2 40

sudo update-alternatives --install /usr/bin/g++ g++ /usr/local/gcc-11.2/bin/g++-11.2 40
```

The default priority is 20, so we can set 40 for gcc11



### Install ccache

In vortex, ccache is required, use 

```
sudo apt install ccache
```

add 

```
export PATH="/usr/lib/ccache:$PATH"
```
to the ~/.bashrc


### Softlink and Dynamic Library

Updating the priority has the same effect as updating the softlink, so updating the softlink is optional.

```
sudo ln -sf /usr/local/gcc-11.2/bin/gcc-11.2 /usr/bin/gcc
sudo ln -sf /usr/local/gcc-11.2/bin/g++-11.2 /usr/bin/g++
```

Dynamic library(if not, vortex build step would complain about glibc):

```
sudo ln -sf /usr/local/gcc-11.2/lib64/libstdc++.so.6.0.29 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
```









