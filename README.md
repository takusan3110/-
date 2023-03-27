# -
姿勢推定Webサービス「SHISEIDOU」に関するソースコード<br>

実装環境としてはanacondaの仮想環境上に実装しました<br>
openmmlab                /home/saitou/anaconda3/envs/openmmlab<br>
また、インストールしたパッケージは以下のとおりです
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
_tflow_select             2.1.0                       gpu  
absl-py                   1.3.0            py38h06a4308_0  
addict                    2.4.0                    pypi_0    pypi
aiohttp                   3.8.1            py38h7f8727e_1  
aiosignal                 1.2.0              pyhd3eb1b0_0  
aiosmtplib                2.0.1              pyhd8ed1ab_0    conda-forge
astor                     0.8.1            py38h06a4308_0  
astunparse                1.6.3                      py_0  
async-timeout             4.0.2            py38h06a4308_0  
attrs                     22.1.0           py38h06a4308_0  
blas                      1.0                         mkl  
blinker                   1.4              py38h06a4308_0  
brotlipy                  0.7.0           py38h27cfd23_1003  
bzip2                     1.0.8                h7b6447c_0  
c-ares                    1.18.1               h7f8727e_0  
ca-certificates           2022.10.11           h06a4308_0  
cachetools                4.2.2              pyhd3eb1b0_0  
certifi                   2022.12.7        py38h06a4308_0  
cffi                      1.15.1           py38h74dc2b5_0  
chardet                   4.0.0           py38h06a4308_1003  
charset-normalizer        2.0.4              pyhd3eb1b0_0  
chumpy                    0.70                     pypi_0    pypi
click                     8.0.4            py38h06a4308_0  
colorama                  0.4.6                    pypi_0    pypi
commonmark                0.9.1                    pypi_0    pypi
contourpy                 1.0.6                    pypi_0    pypi
cryptography              38.0.1           py38h9ce1e76_0  
cuda                      11.7.1                        0    nvidia
cuda-cccl                 11.7.91                       0    nvidia
cuda-command-line-tools   11.7.1                        0    nvidia
cuda-compiler             11.7.1                        0    nvidia
cuda-cudart               11.7.99                       0    nvidia
cuda-cudart-dev           11.7.99                       0    nvidia
cuda-cuobjdump            11.7.91                       0    nvidia
cuda-cupti                11.7.101                      0    nvidia
cuda-cuxxfilt             11.7.91                       0    nvidia
cuda-demo-suite           11.8.86                       0    nvidia
cuda-documentation        11.8.86                       0    nvidia
cuda-driver-dev           11.7.99                       0    nvidia
cuda-gdb                  11.8.86                       0    nvidia
cuda-libraries            11.7.1                        0    nvidia
cuda-libraries-dev        11.7.1                        0    nvidia
cuda-memcheck             11.8.86                       0    nvidia
cuda-nsight               11.8.86                       0    nvidia
cuda-nsight-compute       11.8.0                        0    nvidia
cuda-nvcc                 11.7.99                       0    nvidia
cuda-nvdisasm             11.8.86                       0    nvidia
cuda-nvml-dev             11.7.91                       0    nvidia
cuda-nvprof               11.8.87                       0    nvidia
cuda-nvprune              11.7.91                       0    nvidia
cuda-nvrtc                11.7.99                       0    nvidia
cuda-nvrtc-dev            11.7.99                       0    nvidia
cuda-nvtx                 11.7.91                       0    nvidia
cuda-nvvp                 11.8.87                       0    nvidia
cuda-runtime              11.7.1                        0    nvidia
cuda-sanitizer-api        11.8.86                       0    nvidia
cuda-toolkit              11.7.1                        0    nvidia
cuda-tools                11.7.1                        0    nvidia
cuda-visual-tools         11.7.1                        0    nvidia
cudatoolkit               10.1.243             h6bb024c_0  
cudnn                     7.6.5                cuda10.1_0  
cupti                     10.1.168                      0  
cycler                    0.11.0                   pypi_0    pypi
cython                    0.29.32                  pypi_0    pypi
dataclasses               0.8                pyh6d0b6a4_7  
ffmpeg                    4.2.2                h20bf706_0  
ffmpeg-python             0.2.0                    pypi_0    pypi
fftw                      3.3.9                h27cfd23_1  
flask                     2.2.2                    pypi_0    pypi
flask-dropzone            1.6.0                    pypi_0    pypi
flask-sqlalchemy          3.0.2                    pypi_0    pypi
fonttools                 4.38.0                   pypi_0    pypi
freetype                  2.12.1               h4a9f257_0  
frozenlist                1.2.0            py38h7f8727e_0  
future                    0.18.2                   pypi_0    pypi
gast                      0.4.0              pyhd3eb1b0_0  
gds-tools                 1.4.0.31                      0    nvidia
giflib                    5.2.1                h7b6447c_0  
gmp                       6.2.1                h295c915_3  
gnutls                    3.6.15               he1e5248_0  
google-auth               2.6.0              pyhd3eb1b0_0  
google-auth-oauthlib      0.4.4              pyhd3eb1b0_0  
google-pasta              0.2.0              pyhd3eb1b0_0  
greenlet                  2.0.1                    pypi_0    pypi
grpcio                    1.42.0           py38hce63b2e_0  
h5py                      2.10.0           py38hd6299e0_1  
hdf5                      1.10.6               h3ffc7dd_1  
idna                      3.4              py38h06a4308_0  
importlib-metadata        4.11.3           py38h06a4308_0  
intel-openmp              2021.4.0          h06a4308_3561  
itsdangerous              2.1.2                    pypi_0    pypi
jinja2                    3.1.2                    pypi_0    pypi
jpeg                      9e                   h7f8727e_0  
json-tricks               3.16.1                   pypi_0    pypi
keras-preprocessing       1.1.2              pyhd3eb1b0_0  
kiwisolver                1.4.4                    pypi_0    pypi
lame                      3.100                h7b6447c_0  
lcms2                     2.12                 h3be6417_0  
ld_impl_linux-64          2.38                 h1181459_1  
lerc                      3.0                  h295c915_0  
libcublas                 11.11.3.6                     0    nvidia
libcublas-dev             11.11.3.6                     0    nvidia
libcufft                  10.9.0.58                     0    nvidia
libcufft-dev              10.9.0.58                     0    nvidia
libcufile                 1.4.0.31                      0    nvidia
libcufile-dev             1.4.0.31                      0    nvidia
libcurand                 10.3.0.86                     0    nvidia
libcurand-dev             10.3.0.86                     0    nvidia
libcusolver               11.4.1.48                     0    nvidia
libcusolver-dev           11.4.1.48                     0    nvidia
libcusparse               11.7.5.86                     0    nvidia
libcusparse-dev           11.7.5.86                     0    nvidia
libdeflate                1.8                  h7f8727e_5  
libffi                    3.4.2                h6a678d5_6  
libgcc-ng                 11.2.0               h1234567_1  
libgfortran-ng            11.2.0               h00389a5_1  
libgfortran5              11.2.0               h1234567_1  
libgomp                   11.2.0               h1234567_1  
libiconv                  1.16                 h7f8727e_2  
libidn2                   2.3.2                h7f8727e_0  
libnpp                    11.8.0.86                     0    nvidia
libnpp-dev                11.8.0.86                     0    nvidia
libnvjpeg                 11.9.0.86                     0    nvidia
libnvjpeg-dev             11.9.0.86                     0    nvidia
libopus                   1.3.1                h7b6447c_0  
libpng                    1.6.37               hbc83047_0  
libprotobuf               3.20.1               h4ff587b_0  
libstdcxx-ng              11.2.0               h1234567_1  
libtasn1                  4.16.0               h27cfd23_0  
libtiff                   4.4.0                hecacb30_2  
libunistring              0.9.10               h27cfd23_0  
libvpx                    1.7.0                h439df22_0  
libwebp                   1.2.4                h11a3e52_0  
libwebp-base              1.2.4                h5eee18b_0  
lz4-c                     1.9.3                h295c915_1  
markdown                  3.3.4            py38h06a4308_0  
markupsafe                2.1.1            py38h7f8727e_0  
matplotlib                3.6.2                    pypi_0    pypi
mkl                       2021.4.0           h06a4308_640  
mkl-service               2.4.0            py38h7f8727e_0  
mkl_fft                   1.3.1            py38hd3c417c_0  
mkl_random                1.2.2            py38h51133e4_0  
mmcv-full                 1.7.0                    pypi_0    pypi
mmdet                     2.26.0                   pypi_0    pypi
mmpose                    0.29.0                   pypi_0    pypi
model-index               0.1.11                   pypi_0    pypi
multidict                 6.0.2            py38h5eee18b_0  
munkres                   1.1.4                    pypi_0    pypi
ncurses                   6.3                  h5eee18b_3  
nettle                    3.7.3                hbbd107a_1  
nsight-compute            2022.3.0.22                   0    nvidia
numpy                     1.23.4           py38h14f4228_0  
numpy-base                1.23.4           py38h31eccc5_0  
oauthlib                  3.2.1            py38h06a4308_0  
opencv-python             4.6.0.66                 pypi_0    pypi
openh264                  2.1.1                h4ff587b_0  
openmim                   0.3.3                    pypi_0    pypi
openssl                   1.1.1s               h7f8727e_0  
opt_einsum                3.3.0              pyhd3eb1b0_1  
ordered-set               4.1.0                    pypi_0    pypi
packaging                 21.3                     pypi_0    pypi
pandas                    1.5.2                    pypi_0    pypi
pillow                    9.2.0            py38hace64e9_1  
pip                       22.2.2           py38h06a4308_0  
protobuf                  3.20.1           py38h295c915_0  
pyasn1                    0.4.8              pyhd3eb1b0_0  
pyasn1-modules            0.2.8                      py_0  
pycocotools               2.0.6                    pypi_0    pypi
pycparser                 2.21               pyhd3eb1b0_0  
pygments                  2.13.0                   pypi_0    pypi
pyjwt                     2.4.0            py38h06a4308_0  
pyopenssl                 22.0.0             pyhd3eb1b0_0  
pyparsing                 3.0.9                    pypi_0    pypi
pysocks                   1.7.1            py38h06a4308_0  
python                    3.8.15               h3fd9d12_0  
python-dateutil           2.8.2                    pypi_0    pypi
python-flatbuffers        2.0                pyhd3eb1b0_0  
pytorch                   1.13.0          py3.8_cuda11.7_cudnn8.5.0_0    pytorch
pytorch-cuda              11.7                 h67b0de4_0    pytorch
pytorch-mutex             1.0                        cuda    pytorch
pytz                      2022.6                   pypi_0    pypi
pyyaml                    6.0                      pypi_0    pypi
readline                  8.2                  h5eee18b_0  
requests                  2.28.1           py38h06a4308_0  
requests-oauthlib         1.3.0                      py_0  
rich                      12.6.0                   pypi_0    pypi
rsa                       4.7.2              pyhd3eb1b0_1  
scipy                     1.9.3            py38h14f4228_0  
setuptools                65.5.0           py38h06a4308_0  
six                       1.16.0             pyhd3eb1b0_1  
sqlalchemy                1.4.44                   pypi_0    pypi
sqlite                    3.40.0               h5082296_0  
tabulate                  0.9.0                    pypi_0    pypi
tensorboard               2.10.0           py38h06a4308_0  
tensorboard-data-server   0.6.0            py38hca6d32c_0  
tensorboard-plugin-wit    1.8.1            py38h06a4308_0  
tensorflow                2.4.1           gpu_py38h8a7d6ce_0  
tensorflow-base           2.4.1           gpu_py38h29c2da4_0  
tensorflow-estimator      2.6.0              pyh7b7c402_0  
tensorflow-gpu            2.4.1                h30adc30_0  
termcolor                 2.1.0            py38h06a4308_0  
terminaltables            3.1.10                   pypi_0    pypi
tk                        8.6.12               h1ccaba5_0  
torchaudio                0.13.0               py38_cu117    pytorch
torchvision               0.14.0               py38_cu117    pytorch
typing_extensions         4.3.0            py38h06a4308_0  
urllib3                   1.26.12          py38h06a4308_0  
werkzeug                  2.2.2            py38h06a4308_0  
wheel                     0.37.1             pyhd3eb1b0_0  
wrapt                     1.14.1           py38h5eee18b_0  
x264                      1!157.20191217       h7b6447c_0  
xtcocotools               1.12                     pypi_0    pypi
xz                        5.2.6                h5eee18b_0  
yapf                      0.32.0                   pypi_0    pypi
yarl                      1.8.1            py38h5eee18b_0  
zipp                      3.8.0            py38h06a4308_0  
zlib                      1.2.13               h5eee18b_0  
zstd                      1.5.2                ha4553b6_0  



<app.pyを正常に動作させるために必要なこと><br><br>
staticsフォルダ下に以下のツールを置いてください

・MMPose<br>
・MMDetection<br>
・ffmpeg<br>

また、sataticsフォルダ下にpthフォルダを作成し、以下の名前のファイルを置いてください<br>

・faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth<br>
・hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth<br>

いずれもMMPoseにインストール時に付随するデータです<br>



