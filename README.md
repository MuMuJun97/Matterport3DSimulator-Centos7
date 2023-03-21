# Matterport3D Simulator for CentOS Linux 7 
- for non-root or non-administrator users in centos 7 server; 
- ref [Matterport3DSimulator](https://github.com/peteanderson80/Matterport3DSimulator)

## Environments
```shell
gcc (GCC) 5.4.0
python 3.8
```

## Installation

### 1. env setting
```shell
git clone https://github.com/MuMuJun97/Matterport3DSimulator-Centos7.git
cd Matterport3DSimulator-Centos7_DIF/
export MPDIR=$(pwd)

# change pkg-config files
python extra/env.py

export PKG_CONFIG_EXECUTABLE=$MPDIR/extra/pkgconfig/bin/pkg-config:$PKG_CONFIG_EXECUTABLE
export PATH=$MPDIR/extra/pkgconfig/bin:$PATH
export PKG_CONFIG_PATH=$MPDIR/extra:$PKG_CONFIG_PATH
```

### 2. build
```shell
mkdir build && cd build
cmake ..
make -j 10

# test 1
python $MPDIR/demo.py 
>>> TEST MatterSim SUCCESS # build OK

# test 2
cd $MPDIR/build
$ python
>>> import MatterSim
>>> print(MatterSim.__file__) # print OK
```
