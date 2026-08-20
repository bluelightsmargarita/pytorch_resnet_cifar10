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

# Experiment 9: Alpha-Budget-Matched Mixup Warmup

## Motivation

The previous Dynamic Mixup experiment compared:

* Fixed Mixup: alpha = 0.5
* Linear Warmup: alpha = 0 -> 0.5

However, these two settings differ not only in the temporal schedule of Mixup strength, but also in their average alpha over training.

For Fixed Mixup:

```text
Average alpha ≈ 0.5
```

For Linear Warmup:

```text
Average alpha ≈ 0.25
```

Therefore, the previous experiment contains a confounding factor:

```text
Temporal scheduling effect
+
Overall Mixup strength
```

To partially separate these two factors, an alpha-budget-matched warmup experiment was designed.

---

## Configuration

Model:

```text
ResNet32
```

Dataset:

```text
CIFAR-10
```

Optimizer:

```text
SGD
```

Learning Rate:

```text
0.1
```

Momentum:

```text
0.9
```

Weight Decay:

```text
5e-4
```

Epochs:

```text
200
```

Cutout:

```text
OFF
```

Label Smoothing:

```text
OFF
```

Seed:

```text
0
```

---

## Alpha-Budget-Matched Warmup

The warmup base alpha was increased from:

```text
0.5
```

to:

```text
1.0
```

producing an approximately linear schedule:

```text
0 -> 1.0
```

The average alpha over training is therefore approximately:

```text
0.5
```

which matches the alpha budget of:

```text
Fixed alpha = 0.5
```

---

## Result

| Method                      | Alpha Schedule | Approx. Average Alpha | Seed | Best Accuracy |
| --------------------------- | -------------- | --------------------: | ---: | ------------: |
| Fixed                       | 0.5 -> 0.5     |                  0.50 |    0 |        93.50% |
| Original Warmup             | 0 -> 0.5       |                  0.25 |    0 |        93.63% |
| Alpha-Budget-Matched Warmup | 0 -> 1.0       |                  0.50 |    0 |        93.14% |

Compared with Fixed alpha=0.5:

```text
93.14% - 93.50% = -0.36 pp
```

Compared with the original Warmup:

```text
93.14% - 93.63% = -0.49 pp
```

---

## Observation

Matching the average alpha budget did not improve the performance of Linear Warmup.

Instead, the alpha-budget-matched schedule achieved:

```text
93.14%
```

which was lower than both Fixed alpha=0.5 and the original Warmup schedule in seed 0.

This suggests that the behavior of Dynamic Mixup cannot be explained only by the arithmetic mean of alpha.

---

## Limitation

The Mixup coefficient is sampled from:

```text
lambda ~ Beta(alpha, alpha)
```

Therefore, alpha is not linearly equivalent to the actual degree of image mixing.

Although:

```text
Warmup 0 -> 1.0
```

and:

```text
Fixed alpha = 0.5
```

have approximately the same average alpha, they do not necessarily have the same effective Mixup regularization strength.

Thus, this experiment should be interpreted as an:

```text
alpha-budget-matched control
```

rather than a perfectly matched effective-regularization experiment.

---

# Experiment 10: Fixed Alpha 0.25 Control Experiment

## Motivation

The original Linear Warmup schedule:

```text
0 -> 0.5
```

has an average alpha of approximately:

```text
0.25
```

Therefore, another control experiment was introduced:

```text
Fixed alpha = 0.25
```

This allows a more direct comparison between:

```text
Fixed alpha = 0.25
```

and:

```text
Warmup 0 -> 0.5
```

while keeping their average alpha approximately matched.

The main research question is:

> When the average alpha budget is approximately matched, does the temporal allocation of Mixup strength still affect final model performance?

---

## Configuration

All training configurations were kept identical to the previous Mixup experiments except for the Mixup schedule.

Fixed control:

```text
Mixup alpha = 0.25
Mixup schedule = fixed
```

Warmup:

```text
Base Mixup alpha = 0.5
Mixup schedule = warmup
```

Three matched random seeds were evaluated:

```text
0, 1, 2
```

---

## Multi-Seed Results

| Seed | Fixed alpha=0.25 | Warmup 0->0.5 | Delta (Warmup - Fixed) |
| ---: | ---------------: | ------------: | ---------------------: |
|    0 |           93.43% |        93.63% |               +0.20 pp |
|    1 |           92.64% |        93.87% |               +1.23 pp |
|    2 |           93.46% |        93.76% |               +0.30 pp |

Using sample standard deviation:

```text
Fixed alpha=0.25 = 93.18% ± 0.47%
Warmup 0->0.5   = 93.75% ± 0.12%
```

Mean paired difference:

```text
+0.58 percentage points
```

All three paired differences were positive:

```text
Seed 0: +0.20 pp
Seed 1: +1.23 pp
Seed 2: +0.30 pp
```

---

## Observation

The original hypothesis that Warmup performs well only because it has a lower average alpha is not sufficient to explain the observed results.

When comparing two configurations with approximately matched average alpha:

```text
Fixed alpha=0.25
vs
Warmup 0->0.5
```

the Warmup schedule achieved higher Best Accuracy for all three tested seeds.

The average improvement was:

```text
+0.58 pp
```

This provides preliminary evidence that the temporal allocation of Mixup strength may influence model performance independently of the simple average alpha value.

---

## Discussion

One possible interpretation is that Linear Mixup Warmup behaves as a form of curriculum regularization.

During early training:

```text
Lower Mixup strength
```

may allow the model to learn basic discriminative features with less regularization.

During later training:

```text
Higher Mixup strength
```

may progressively increase regularization and encourage smoother decision boundaries.

However, this mechanism has not yet been directly verified.

Another important observation is the relatively high cross-seed variation of the Fixed alpha=0.25 condition:

```text
Fixed alpha=0.25 std ≈ 0.47
```

compared with:

```text
Warmup std ≈ 0.12
```

In particular, the seed 1 result for Fixed alpha=0.25 was substantially lower than the other two seeds.

Therefore, part of the observed mean improvement is influenced by this low-performing seed.

---

## Current Conclusion

The current experiments suggest that:

> The behavior of Mixup Warmup cannot be explained solely by its lower average alpha.

Across three matched seeds, Linear Warmup from 0 to 0.5 consistently outperformed Fixed alpha=0.25, with an average paired improvement of approximately 0.58 percentage points.

This provides preliminary evidence that the temporal scheduling of Mixup strength may itself affect optimization or regularization behavior.

However, because only three random seeds were evaluated, the current evidence is not sufficient for a strong statistical claim.

---

## Limitations

Current limitations include:

1. Only three random seeds were evaluated.
2. Mean alpha is only an approximate proxy for effective Mixup strength.
3. Training dynamics across early, middle, and late stages were not explicitly analyzed.
4. No statistical significance test is reported due to the very small sample size.
5. Only a linear Warmup schedule was investigated in the current control experiment.

---

## Future Work

Possible future extensions include:

* Increasing the number of random seeds.
* Measuring effective mixing strength instead of only average alpha.
* Analyzing training and validation dynamics across different training stages.
* Comparing nonlinear or stage-wise Mixup schedules.
* Investigating whether Dynamic Mixup behaves as a form of curriculum regularization.

These extensions are left for future work.
