# ResNet32 CIFAR10 Baseline


## 1. Experiment Information

Date:
2026-08-09

Model:
ResNet32

Dataset:
CIFAR10


## 2. Training Configuration

Optimizer:
SGD

Learning rate:
0.1

Momentum:
0.9

Weight decay:
0.0001

Scheduler:
MultiStepLR

Milestones:
100,150

Epoch:
200


## 3. Result

Best Accuracy:

Final Accuracy:


## 4. Notes

- Successfully reproduced baseline
- Checkpoint resume verified
- Scheduler resume verified

# ResNet32 CIFAR10 Baseline Experiment


## Environment

Framework:
PyTorch

Dataset:
CIFAR10


## Model

Architecture:
ResNet32


## Training Settings

Epoch:
200

Optimizer:
SGD

Learning rate:
0.1

Momentum:
0.9

Weight decay:
1e-4


## Scheduler

MultiStepLR

milestones:
100,150

gamma:
0.1


## Result

Best Test Accuracy:

92.82%


## Checkpoint

checkpoint_last.pth

model_best.pth


# ResNet32 CIFAR10 Baseline Experiment


## 1. Experiment Goal

Reproduce ResNet32 on CIFAR10 dataset
and establish a baseline for future improvements.


## 2. Environment

Framework:
PyTorch

Dataset:
CIFAR10


## 3. Model

Architecture:
ResNet32


## 4. Training Configuration

Epochs:
200

Batch size:
128


Optimizer:
SGD

Learning rate:
0.1

Momentum:
0.9

Weight decay:
1e-4


## 5. Learning Rate Scheduler

Scheduler:
MultiStepLR

Milestones:
100,150

Gamma:
0.1


## 6. Checkpoint Strategy

Save:
checkpoint_last.pth

model_best.pth


Resume training:
Supported


## 7. Result

Best Test Accuracy:

92.31%


## 8. Conclusion

The baseline model was successfully reproduced.
Checkpoint recovery and learning rate scheduling were verified.

This experiment provides a reference for future model improvements.
