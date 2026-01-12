# REAMDE

+ RTX 3080
+ VS2022 17.14.19
+ cuda 12.5



## 配置流程

```bash
git clone https://github.com/banbao990/ReSTIR_PT.git
```

+ 运行 `prepare.bat` 初始化
+ 下载：NVAPI
  + 下载完成后放到目录 `Source/Externals/.packman/nvapi`
  + 我用的[版本](https://github.com/NVIDIA/nvapi/commit/832a3673d66a0fdf6d6e522468821d5cbd925f23)
+ 打开 `Falcor.sln` 编译【VS2022】
+ 有效版本
  + ReleaseD3D12



## python 环境

+ 目前我的电脑用的是 cuda
+ 使用 pacman 获取的 python 环境【python310】
+ 需要在这个环境下安装 python 包
+ 进入目录 `Source\Externals\.packman\python`
+ 创建一个新环境

```bash
python -m FRadius
```

+ 激活的 `activate.bat` 在目录 `Source\Externals\.packman\python\FRadius\Scripts` 下
+ 接下来只需要在这个虚拟环境中操作就 ok 了
+ **<span style="color:red">先激活环境</span>**
+ 安装 pytorch

```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

+ 目前运行如下指令，能够看到输出了 torch 的版本

```bash
Bin\x64\Release\Mogwai.exe --script=Source\Mogwai\Data\minimal_example.py
# Torch version: 2.9.1+cu126
```



# 其他

## Falcor Test Fail

+ 在我的电脑上，`FalcorTest` 中，如下 test 过不了
  + `IntersectionHelpersTests.cpp`：光线和 sphere 求交点【别用这个】



## Falcor with Pytorch

+ 参考 [cross-denoiser](https://github.com/CGLab-GIST/cross-denoiser/tree/falcor) 这个库，可以使用 Torch cpp 版本
+ 目前我的实现是 cpp 调用 python
  + python 调 cpp，主循环在 python 端会阻塞 UI 运行