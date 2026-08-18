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
92.21%

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

## Experiment3: Mixup+cutout

Model:
ResNet32

Augmentation:
RandomCrop + RandomHorizontalFlip + Mixup(alpha=1.0)

Best Accuracy:
93.09%

## Experiment 4: Label Smoothing

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

- RandomHorizontalFlip
- RandomCrop


### Label Smoothing

label_smoothing = 0.1


### Result

Best Accuracy:

92.69%


### Observation

Compared with baseline (92.31%),
Label Smoothing improves test accuracy by approximately 0.38%.

The improvement is smaller than Cutout and Mixup,
but it still provides a positive regularization effect.

## Experiment 5: Mixup Alpha Sensitivity

| Alpha | Best Accuracy |
|------:|--------------:|
| 0.2 | 93.39% |
| 1.0 | 93.09% |

Current best:

Mixup(alpha=0.2) = 93.39%


| Alpha | Best Accuracy |
|-------:|--------------:|
| 0.2   | 93.39%        |
| 0.5   | 93.81%        |
| 1.0   | 93.09%        |
| 2.0   | Pending       |

Current Best:

Mixup(alpha=0.5) = 93.81%


| Alpha | Best Accuracy |
|-------:|--------------:|
| 0.2   | 93.39%        |
| 0.5   | 93.81%        |
| 1.0   | 93.09%        |
| 2.0   | 92.82%        |

Current Best:

Mixup(alpha=0.5) = 93.81%

## Experiment 6: Multi-Seed Evaluation for Mixup(alpha=0.5)

To evaluate the stability of the best Mixup configuration, the experiment was repeated with three different random seeds while keeping all other settings unchanged.

| Seed | Best Accuracy |
|-----:|--------------:|
| 0    | 93.05%        |
| 1    | 93.56%        |
| 2    | 93.51%        |

Mean Accuracy: 93.37%

Standard Deviation: 0.28%

Final Result:

Mixup(alpha=0.5) = 93.37% ± 0.28%

## Experiment 7: Weight Decay Sensitivity

### Configuration

Model:
ResNet32

Dataset:
CIFAR-10

Optimizer:
SGD

Learning Rate:
0.1

Momentum:
0.9

Scheduler:
MultiStepLR

Epochs:
200

Mixup Alpha:
0.5

Cutout:
OFF

Label Smoothing:
OFF

Loss:
CrossEntropyLoss

Seed:
0

### Weight Decay Sensitivity Results

| Weight Decay | Best Accuracy |
|---|---:|
| 0 | 90.76% |
| 1e-5 | 89.66% |
| 5e-5 | 92.89% |
| 1e-4 | 92.58% |
| 2.5e-4 | 93.42% |
| 5e-4 | 93.50% |
| 7.5e-4 | 93.09% |
| 1e-3 | 92.64% |

### Observation

Weight decay showed a clear non-monotonic effect on model performance.

Very small weight decay values, including 0 and 1e-5, resulted in relatively poor generalization performance.

Performance improved substantially when weight decay increased to the range of approximately 2.5e-4 to 5e-4.

Among the tested values, 5e-4 achieved the highest single-seed accuracy of 93.50%.

Increasing weight decay further to 7.5e-4 and 1e-3 caused performance to decrease, indicating that excessive regularization can reduce model accuracy.

These results suggest that an appropriate balance between Mixup regularization and weight decay is important for ResNet32 on CIFAR-10.


### Multi-seed Evaluation for Weight Decay = 5e-4

Fixed configuration:

- Mixup alpha = 0.5
- Weight decay = 5e-4
- Epochs = 200
- Cutout = OFF
- Label Smoothing = OFF

| Seed | Best Accuracy |
|---:|---:|
| 0 | 93.50% |
| 1 | 93.70% |
| 2 | 93.96% |

Mean Accuracy:

93.72%

Standard Deviation:

0.23%

Final result:

ResNet32 + Mixup(alpha=0.5) + Weight Decay(5e-4)

= 93.72% ± 0.23%


### Comparison with Previous Mixup Configuration

Previous result:

ResNet32 + Mixup(alpha=0.5) + Weight Decay(1e-4)

= 93.37% ± 0.28%

Optimized weight decay result:

ResNet32 + Mixup(alpha=0.5) + Weight Decay(5e-4)

= 93.72% ± 0.23%

Mean accuracy improvement:

+0.35 percentage points

The optimized weight decay produced higher accuracy for all three tested random seeds, suggesting that the improvement is relatively stable across these runs.

## Experiment 8: Dynamic Mixup Schedule

### Motivation

Previous experiments showed that Mixup with alpha=0.5 and weight decay=5e-4 achieved strong performance.

This experiment investigates whether the Mixup strength should remain fixed throughout training, or change dynamically with training progress.

The following schedules were compared:

- Fixed: alpha remains 0.5
- Decay: alpha linearly decreases from 0.5 toward 0
- Warmup: alpha linearly increases from 0 toward 0.5

All other settings were kept unchanged.

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
5e-4

Mixup base alpha:
0.5

Epochs:
200

Cutout:
OFF

Label Smoothing:
OFF

### Single-seed comparison

| Schedule | Seed | Best Accuracy |
|----------|------|---------------|
| Fixed | 0 | 93.50% |
| Decay | 0 | 93.18% |
| Warmup | 0 | 93.63% |

Compared with the fixed schedule:

- Decay: -0.32 percentage points
- Warmup: +0.13 percentage points

The decay schedule did not improve performance.

Warmup showed a small positive result on seed 0, so it was further evaluated with multiple random seeds.

### Warmup Multi-seed Evaluation

| Seed | Fixed | Warmup | Difference |
|------|-------|--------|------------|
| 0 | 93.50% | 93.63% | +0.13 |
| 1 | 93.70% | 93.87% | +0.17 |
| 2 | 93.96% | 93.76% | -0.20 |

Fixed:

93.72% ± 0.23%

Warmup:

93.75% ± 0.10%

Mean improvement:

+0.03 percentage points

### Observation

Linear Mixup warmup did not produce a clear improvement in average accuracy compared with fixed alpha=0.5.

Although warmup improved performance for seeds 0 and 1, it decreased performance for seed 2.

Therefore, the current results do not support the conclusion that linear Mixup warmup consistently improves model accuracy.

Warmup showed lower variation across the three tested seeds, but only three seeds were evaluated, so no strong conclusion about improved training stability is made.

The decay schedule performed worse than the fixed schedule in the single-seed experiment.

### Discussion

The dynamic schedules also change the average Mixup strength over the whole training process.

For example, a linear schedule between 0 and 0.5 has an average alpha of approximately 0.25, whereas the fixed schedule keeps alpha=0.5 throughout training.

Therefore, differences between fixed and dynamic schedules may reflect both:

1. the temporal distribution of Mixup strength
2. the total amount of Mixup regularization

A future experiment could control for average Mixup strength to separate these two effects.