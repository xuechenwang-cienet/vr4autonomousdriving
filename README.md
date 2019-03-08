# vr4autonomousdriving

## Setup env

Ubuntu18.04.2, GeForce RTX 2070

### nvidia-driver and CUDA

nvidia-driver-410 and CUDA10

Linux-x86_64-Ubuntu-18.04-deb(local)

https://developer.nvidia.com/cuda-10.0-download-archive?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=deblocal

### venv

```bash
$ python3.6 -m venv venv
$ source venv/bin/activate
(venv) $
```

### CARLA Python API

Download carla v0.9.3
https://github.com/carla-simulator/carla/releases/tag/0.9.3

```bash
(venv) $ easy_install CARLA_0.9.3/PythonAPI/carla-0.9.3-py3.5-linux-x86_64.egg
```

### facebookresearch/maskrcnn-benchmark

Here is a prebuilt wheel

```bash
(venv) $ pip install maskrcnn_benchmark-0.1-cp36-cp36m-linux_x86_64.whl
```

### PyTorch 1.0

PyTorch 1.0, https://pytorch.org/

Stable(1.0)-Linux-Pip-Python3.6-CUDA10.0

```bash
(venv) $ pip3 install https://download.pytorch.org/whl/cu100/torch-1.0.1.post2-cp36-cp36m-linux_x86_64.whl
(venv) $ pip3 install torchvision
```

### Install other dependent packages

```bash
(venv) $ pip install -r requirements.txt
```

## Start this DEMO

### CARLA

```bash
$ cd CARLA_0.9.3
CARLA_0.9.3 $ ./CarlaUE4.sh
```

### VRSERVER

```bash
(venv) $ env "FLASK_APP=vrserver" "PYTHONIOENCODING=UTF-8" python -m flask run
```
