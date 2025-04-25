# import OS module
import os
# Get the list of all files and directories
path = "C://Users//xd//Documents//GitHub//RefactoredAudio//wheels"
dir_list = os.listdir(path)
print("Files and directories in '", path, "' :")
# prints all files
for f in dir_list:
    if f.endswith(".whl"):
        print(f'"./wheels/{f}",')

# for f in dir_list:
#     if "cp312" in f:
#         print(f)
import subprocess
import sys
import pip
# List of wheel files (either file paths or URLs)
wheel_files = [
    "allosaurus-1.0.2-py3-none-any.whl",
    "editdistance-0.8.1-cp310-cp310-macosx_10_9_x86_64.whl",
    "editdistance-0.8.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "editdistance-0.8.1-cp311-cp311-win_amd64.whl",
    "filelock-3.16.0-py3-none-any.whl",
    "fsspec-2024.9.0-py3-none-any.whl",
    "jinja2-3.1.4-py3-none-any.whl",
    "llvmlite-0.43.0-cp310-cp310-macosx_10_9_x86_64.whl",
    "llvmlite-0.43.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "llvmlite-0.43.0-cp311-cp311-win_amd64.whl",
    "MarkupSafe-2.1.5-cp310-cp310-macosx_10_9_x86_64.whl",
    "MarkupSafe-2.1.5-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "MarkupSafe-2.1.5-cp311-cp311-win_amd64.whl",
    "mpmath-1.3.0-py3-none-any.whl",
    "munkres-1.1.4-py2.py3-none-any.whl",
    "networkx-3.3-py3-none-any.whl",
    "numba-0.60.0-cp310-cp310-macosx_10_9_x86_64.whl",
    "numba-0.60.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl",
    "numba-0.60.0-cp311-cp311-win_amd64.whl",
    "numpy-2.0.2-cp310-cp310-macosx_10_9_x86_64.whl",
    "numpy-2.0.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "numpy-2.0.2-cp311-cp311-win_amd64.whl",
    "nvidia_cublas_cu12-12.1.3.1-py3-none-manylinux1_x86_64.whl",
    "nvidia_cuda_cupti_cu12-12.1.105-py3-none-manylinux1_x86_64.whl",
    "nvidia_cuda_nvrtc_cu12-12.1.105-py3-none-manylinux1_x86_64.whl",
    "nvidia_cuda_runtime_cu12-12.1.105-py3-none-manylinux1_x86_64.whl",
    "nvidia_cudnn_cu12-9.1.0.70-py3-none-manylinux2014_x86_64.whl",
    "nvidia_cufft_cu12-11.0.2.54-py3-none-manylinux1_x86_64.whl",
    "nvidia_curand_cu12-10.3.2.106-py3-none-manylinux1_x86_64.whl",
    "nvidia_cusolver_cu12-11.4.5.107-py3-none-manylinux1_x86_64.whl",
    "nvidia_cusparse_cu12-12.1.0.106-py3-none-manylinux1_x86_64.whl",
    "nvidia_nccl_cu12-2.20.5-py3-none-manylinux2014_x86_64.whl",
    "nvidia_nvjitlink_cu12-12.6.68-py3-none-manylinux2014_x86_64.whl",
    "nvidia_nvtx_cu12-12.1.105-py3-none-manylinux1_x86_64.whl",
    "panphon-0.21.2-py2.py3-none-any.whl",
    "pip-24.2-py3-none-any.whl",
    "PyYAML-6.0.2-cp310-cp310-macosx_10_9_x86_64.whl",
    "PyYAML-6.0.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "PyYAML-6.0.2-cp311-cp311-win_amd64.whl",
    "regex-2024.9.11-cp310-cp310-macosx_10_9_x86_64.whl",
    "regex-2024.9.11-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "regex-2024.9.11-cp311-cp311-win_amd64.whl",
    "resampy-0.4.3-py3-none-any.whl",
    "scipy-1.14.1-cp310-cp310-macosx_10_13_x86_64.whl",
    "scipy-1.14.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "scipy-1.14.1-cp311-cp311-win_amd64.whl",
    "setuptools-74.1.2-py3-none-any.whl",
    "setuptools-75.1.0-py3-none-any.whl",
    "sympy-1.13.2-py3-none-any.whl",
    "torch-2.2.2-cp310-none-macosx_10_9_x86_64.whl",
    "torch-2.4.1-cp310-cp310-manylinux1_x86_64.whl",
    "torch-2.4.1-cp311-cp311-win_amd64.whl",
    "triton-3.0.0-1-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl",
    "typing_extensions-4.12.2-py3-none-any.whl",
    "unicodecsv-0.14.1-py3-none-any.whl",
    "wheel-0.44.0-py3-none-any.whl"
]

# # Function to install the wheel files using pip
# def install_wheel(wheel_file):
#     try:
#         iii = 0
#         wheel_verison = ""
#         wheel_name = ""
#         for i, char in enumerate(wheel_file):
#             #print(f"Index {i}: {char}")
#             if iii ==0:
#                 wheel_name = wheel_name + char
#             if iii ==1:
#                 wheel_verison = wheel_verison + char
#             if char == "-":
#                 iii+=1
#             if iii ==2:
#                 #print(f"wheel name: {wheel_name}, wheel verison {wheel_verison}")
#                 break
        
#         #print(f"Installing {wheel_name[:-1], '==',wheel_verison[:-1]}...")
#         #subprocess.check_call([ sys.executable, 'pip', 'download', '--d .', '--only-binary=:all:',' --python-version=3.11.9',  ])
#         print(f'"{wheel_name[:-1]}=={wheel_verison[:-1]}",')
#         #pip.main(['download', wheel_name[:-1] , '--dest ./temp','--only-binary=:all:','--python-version=3.11.9' ])
#         #pip. download
#         #print(f"{wheel_file} installed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error installing {wheel_file}: {e}")

# # Loop through each wheel file and install it
# for wheel in wheel_files:
#     install_wheel(wheel)
