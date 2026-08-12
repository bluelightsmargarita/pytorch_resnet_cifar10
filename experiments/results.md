# ResNet32 CIFAR10 Experiments


## Baseline

Model:
ResNet32

Optimizer:
SGD

Scheduler:
MultiStepLR

Epoch:
200

Accuracy:
92.31%



## Experiment 1

Model:
ResNet32

Optimizer:
SGD

Scheduler:
CosineAnnealingLR

T_max:
200

Epoch:
200

Accuracy:
92.11%

Observation:
CosineAnnealingLR produced comparable performance,
but did not outperform the classical MultiStepLR schedule.

## Experiment 2: ResNet32 + Cutout


### Configuration

Model:
ResNet32

Dataset:
CIFAR10

Optimizer:
SGD

Learning rate:
0.1

Momentum:
0.9

Weight decay:
1e-4

Scheduler:
MultiStepLR

Milestones:
[100, 150]

Gamma:
0.1

Epochs:
200

Batch size:
128


### Data Augmentation

Baseline:

- RandomHorizontalFlip
- RandomCrop


Experiment:

- RandomHorizontalFlip
- RandomCrop
- Cutout


Cutout parameters:

n_holes = 1

length = 16


### Result

Best Accuracy:

92.98%


### Observation

Compared with baseline (92.31%),
Cutout improves test accuracy by approximately 0.67%.

Although training accuracy decreases,
the model achieves better generalization ability,
indicating that Cutout provides effective regularization.

## Experiment3: Mixup

Model:
ResNet32

Augmentation:
RandomCrop + RandomHorizontalFlip + Mixup(alpha=1.0)

Best Accuracy:
93.09%