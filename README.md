# ResNet32 on CIFAR-10: Baseline and Mixup Experiments

基于 [akamaster/pytorch_resnet_cifar10](https://github.com/akamaster/pytorch_resnet_cifar10)，建立固定训练／验证划分下的 ResNet32 baseline，并比较固定 Mixup α=0.5 在三个训练随机种子上的表现。

## 实验协议

- 数据划分：CIFAR-10 官方训练集划分为 45,000 张训练图片和 5,000 张验证图片，每类验证图片 500 张。
- 固定划分种子：`split_seed=42`，所有实验使用相同划分。
- 训练随机种子：`0、1、2`。
- 模型选择：仅根据验证准确率保存最佳模型。
- 最终评测：使用验证集选出的最佳模型，在官方 10,000 张测试图片上独立评测。
- 训练设置：ResNet32，200 epochs，batch size 128，SGD，初始学习率 0.1，momentum 0.9，weight decay 1e-4。
- 学习率调度：第 100、150 轮后衰减，衰减系数 0.1。
- 数据增强：随机水平翻转、带 4 像素填充的随机裁剪；验证与测试不使用随机增强。
- 归一化：mean=(0.485, 0.456, 0.406)，std=(0.229, 0.224, 0.225)。
- 对照设置：Baseline 关闭 Mixup；Mixup 使用固定 α=0.5，其余上述设置一致。

运行环境：Python 3.10.18、PyTorch 2.3.1+cu118，CUDA 可用。

## 实验结果

以下准确率单位均为 %；最佳轮数从 1 开始计数。

| 方法 | Seed | 最佳验证准确率 | 最佳轮数 | 最后一轮验证准确率 | 测试准确率 |
|---|---:|---:|---:|---:|---:|
| Baseline | 0 | 92.38 | 140 | 92.12 | 91.44 |
| Baseline | 1 | 93.08 | 173 | 92.88 | 92.09 |
| Baseline | 2 | 92.80 | 197 | 92.66 | 91.96 |
| Mixup α=0.5 | 0 | 93.28 | 182 | 92.80 | 92.72 |
| Mixup α=0.5 | 1 | 93.58 | 186 | 93.24 | 93.13 |
| Mixup α=0.5 | 2 | 93.78 | 187 | 93.46 | 93.24 |

| 方法 | 最佳验证准确率：均值 ± 标准差 | 测试准确率：均值 ± 标准差 |
|---|---:|---:|
| Baseline | 92.75 ± 0.35 | 91.83 ± 0.34 |
| Mixup α=0.5 | 93.55 ± 0.25 | 93.03 ± 0.27 |

标准差采用三个训练种子的样本标准差（ddof=1）。在本次固定数据划分和训练配置下，Mixup 的平均测试准确率提高 1.20 个百分点，三个对应种子均有提升。实验仅覆盖三个训练种子，尚未验证其他数据划分下的表现。

此前使用不同数据协议的结果，以及下方上游提供的成绩，不与本表直接混合比较。

## 复现方法

以下命令在 Linux 项目根目录运行，需要可用的 PyTorch CUDA 环境。

首次准备 CIFAR-10 数据时，可在训练命令中添加 `--download`；数据已放在 `./data` 时无需添加。

### Baseline：seed=0

```bash
python trainer.py \
  --arch resnet32 --workers 0 --epochs 200 \
  --batch-size 128 --lr 0.1 --momentum 0.9 \
  --weight-decay 1e-4 --seed 0 \
  --mixup-alpha 0 --mixup-schedule fixed \
  --data-root ./data --val-size 5000 --split-seed 42 \
  --save-dir experiments/reproduce_baseline_seed0/checkpoints
```

### Mixup：seed=0

```bash
python trainer.py \
  --arch resnet32 --workers 0 --epochs 200 \
  --batch-size 128 --lr 0.1 --momentum 0.9 \
  --weight-decay 1e-4 --seed 0 \
  --mixup-alpha 0.5 --mixup-schedule fixed \
  --data-root ./data --val-size 5000 --split-seed 42 \
  --save-dir experiments/reproduce_mixup05_seed0/checkpoints
```

复现其他训练种子时，同时修改 `--seed` 和输出目录，避免覆盖已有实验。

### 独立测试

```bash
python trainer.py \
  --arch resnet32 --workers 0 \
  --evaluate --eval-split test \
  --data-root ./data \
  --resume experiments/reproduce_baseline_seed0/checkpoints/model_best.pth
```

## 实验记录与检查点

`experiments/` 中保留六次正式训练的 `train.log`、`run_config.json` 和 `split_indices.json`，以及六个最佳模型的独立测试日志。

- Baseline 训练目录：`baseline_split_seed0_20261012`、`baseline_split_seed1_20261014`、`baseline_split_seed2_20261014`。
- Mixup 训练目录：`mixup05_split_seed0_20261013`、`mixup05_split_seed1_20261014`、`mixup05_split_seed2_20261014`。
- Baseline seed=0 测试日志：`experiments/test_eval_baseline_seed0_20261015/test.log`。
- 其余五次测试日志：`experiments/test_eval_20261015/<训练目录名>/test.log`。

训练时，每轮保存 `checkpoint_last.pth`；验证准确率提高时更新 `model_best.pth`。检查点包含模型、优化器、学习率调度器和数据协议信息。数据集与模型权重未纳入 Git。

固定随机种子便于重复实验，但当前设置不保证逐位确定性；检查点未保存随机数生成器状态，恢复训练也不保证与不中断训练完全一致。

## 本分支完成的工作

- 建立固定、类别均衡且独立于训练种子的训练／验证划分，并保存配置与划分索引。
- 将验证集模型选择与官方测试集评测分离。
- 修复最佳模型被覆盖、恢复路径缺失时未及时报错，以及单卡／DataParallel 权重加载不兼容的问题。
- 完成 Baseline 与固定 Mixup α=0.5 的三种子实验，保存训练和测试记录并汇总结果。

ResNet 网络实现来自上游项目；Mixup 为已有方法，本项目贡献主要是实验协议、训练流程修复、对照实验与结果整理。

---

## 上游项目原始说明

以下保留上游项目介绍、预训练模型链接及引用信息。其中的训练协议与成绩属于上游说明；本分支正式实验以本文前述协议为准。

# Proper ResNet Implementation for CIFAR10/CIFAR100 in Pytorch
[Torchvision model zoo](https://github.com/pytorch/vision/tree/master/torchvision/models) provides number of implementations of various state-of-the-art architectures, however, most of them are defined and implemented for ImageNet.
Usually it is straightforward to use the provided models on other datasets, but some cases require manual setup.

For instance, very few pytorch repositories with ResNets on CIFAR10 provides the implementation as described in the [original paper](https://arxiv.org/abs/1512.03385). If you just use the torchvision's models on CIFAR10 you'll get the model **that differs in number of layers and parameters**. This is unacceptable if you want to directly compare ResNet-s on CIFAR10 with the original paper.
The purpose of this repo is to provide a valid pytorch implementation of ResNet-s for CIFAR10 as described in the original paper. The following models are provided:

| Name      | # layers | # params| Test err(paper) | Test err(this impl.)|
|-----------|---------:|--------:|:-----------------:|:---------------------:|
|[ResNet20](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet20-12fca82f.th)   |    20    | 0.27M   | 8.75%| **8.27%**|
|[ResNet32](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet32-d509ac18.th)  |    32    | 0.46M   | 7.51%| **7.37%**|
|[ResNet44](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet44-014dd654.th)   |    44    | 0.66M   | 7.17%| **6.90%**|
|[ResNet56](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet56-4bfd9763.th)   |    56    | 0.85M   | 6.97%| **6.61%**|
|[ResNet110](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet110-1d1ed7c2.th)  |   110    |  1.7M   | 6.43%| **6.32%**|
|[ResNet1202](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet1202-f3b1deed.th) |  1202    | 19.4M   | 7.93%| **6.18%**|

This implementation matches description of the original paper, with comparable or better test error.

## How to run?
```bash
git clone https://github.com/akamaster/pytorch_resnet_cifar10
cd pytorch_resnet_cifar10
chmod +x run.sh && ./run.sh
```

## Details of training
Our implementation follows the paper in straightforward manner with some caveats: **First**, the training in the paper uses 45k/5k train/validation split on the train data, and selects the best performing model based on the performance on the validation set. We *do not perform* validation testing; if you need to compare your results on ResNet head-to-head to the orginal paper keep this in mind. **Second**, if you want to train ResNet1202 keep in mind that you need 16GB memory on GPU.

## Pretrained models for download
1. [ResNet20, 8.27% err](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet20.th)
2. [ResNet32, 7.37% err](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet32.th)
3. [ResNet44, 6.90% err](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet44.th)
4. [ResNet56, 6.61% err](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet56.th)
5. [ResNet110, 6.32% err](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet110.th)
6. [ResNet1202, 6.18% err](https://github.com/akamaster/pytorch_resnet_cifar10/raw/master/pretrained_models/resnet1202.th)

If you find this implementation useful and want to cite/mention this page, here is a bibtex citation:

```bibtex
@misc{Idelbayev18a,
  author       = "Yerlan Idelbayev",
  title        = "Proper {ResNet} Implementation for {CIFAR10/CIFAR100} in {PyTorch}",
  howpublished = "\url{https://github.com/akamaster/pytorch_resnet_cifar10}",
  note         = "Accessed: 20xx-xx-xx"
}

```