# Traffic — CS50 AI

Neural network for classifying German traffic signs (GTSRB dataset, 43 categories) using TensorFlow/Keras.

## Experimentation

To understand how architectural choices affect performance, three model variants were trained and compared on the same data split (60% train / 40% test, 10 epochs, Adam optimizer, `categorical_crossentropy` loss).

---

### Architecture 1 — No convolution (weak baseline)

A pure dense network applied to flattened raw pixels. Used as a sanity baseline to measure how much value the convolutional layers actually add.

```
Flatten()                          → (2700,)
Dense(128, ReLU)                   → (128,)
Dense(43, softmax)                 → (43,)
```

**Hypothesis:** dense layers treat every pixel position as an independent feature, so the network has no built-in notion of spatial locality or translation invariance. It should still learn something — there are strong color and position cues in centered traffic-sign photos — but it should plateau well below a CNN.

**Results:**
- Training accuracy (final epoch): 85.04%
- Test accuracy: 84.12%
- Test loss: 0.6255
- Time per epoch: ~2 seconds

**Observations:** Surprisingly competitive considering there are zero convolutional layers. The accuracy is decent because GTSRB images are pre-cropped and centered, so position-specific dense weights can still latch onto consistent color and shape patterns at fixed coordinates. Two things stand out:
1. Train (85%) and test (84%) are almost identical — no overfitting at all, which means the model doesn't have enough capacity to memorize training data, let alone generalize beyond it.
2. The loss is still steadily decreasing at epoch 10 (0.86 → 0.61 in the last 5 epochs), so the network has not converged — more epochs would help, but only marginally. The architecture is the real bottleneck.

---

### Architecture 2 — Standard CNN (baseline)

Two convolutional blocks followed by a dense classifier with dropout. This is the textbook starting point for small-image classification.

```
Conv2D(32, 3x3, ReLU)              → (28, 28, 32)
MaxPooling2D(2x2)                  → (14, 14, 32)

Conv2D(64, 3x3, ReLU)              → (12, 12, 64)
MaxPooling2D(2x2)                  → (6, 6, 64)

Flatten()                          → (2304,)
Dense(128, ReLU)                   → (128,)
Dropout(0.5)                       → (128,)
Dense(43, softmax)                 → (43,)
```

**Hypothesis:** convolutional filters share weights across spatial positions, so the same "red octagon edge" or "white arrow" pattern is detected anywhere in the frame. Pooling halves the spatial dimensions and gives some shift tolerance. Dropout 0.5 before the output discourages over-reliance on any single feature.

**Results:**
- Training accuracy (final epoch): 93.50%
- Test accuracy: 98.43%
- Test loss: 0.0680
- Time per epoch: ~4 seconds

**Observations:** Massive jump over Architecture 1: +14 points in test accuracy (84% → 98%) and the test loss drops by an order of magnitude (0.62 → 0.07). This confirms that the spatial inductive bias of convolutions (weight sharing + locality) is doing the heavy lifting, not just raw model capacity. Notable detail: test accuracy (98.4%) ends up higher than training accuracy (93.5%). This is not a bug — it is the expected effect of dropout. During training, 50% of the dense layer's activations are zeroed out, artificially handicapping the reported training accuracy; during evaluation dropout is disabled and the full network is active. Combined with the fact that training accuracy is averaged over an epoch where the model is still improving, the gap is healthy and indicates no overfitting.

---

### Architecture 3 — Deeper CNN with Batch Normalization (strong)

Three convolutional blocks, batch normalization between layers, and a slightly larger dense head with two dropout layers.

```
Conv2D(32, 3x3, ReLU) + BatchNorm  → (28, 28, 32)
Conv2D(32, 3x3, ReLU) + BatchNorm  → (26, 26, 32)
MaxPooling2D(2x2)                  → (13, 13, 32)

Conv2D(64, 3x3, ReLU) + BatchNorm  → (11, 11, 64)
MaxPooling2D(2x2)                  → (5, 5, 64)

Conv2D(128, 3x3, ReLU) + BatchNorm → (3, 3, 128)

Flatten()                          → (1152,)
Dense(256, ReLU)                   → (256,)
Dropout(0.5)                       → (256,)
Dense(128, ReLU)                   → (128,)
Dropout(0.3)                       → (128,)
Dense(43, softmax)                 → (43,)
```

**Hypothesis:** stacking two 3x3 convolutions before pooling gives an effective 5x5 receptive field with fewer parameters and an extra non-linearity. A third conv block (128 filters) lets the network learn higher-level combinations of mid-level features. BatchNormalization stabilizes training and tends to allow faster convergence and slightly higher final accuracy. The deeper dense head with two dropout layers should provide additional regularization to fight overfitting from the increased capacity.

**Results:**
- Training accuracy (final epoch): 98.86%
- Test accuracy: 98.12%
- Test loss: 0.0649
- Time per epoch: ~13 seconds

**Observations:** The hypothesis was only partially confirmed. BatchNormalization clearly accelerated convergence: epoch 1 already reached 68.7% training accuracy (versus 34.5% for Architecture 2), and by epoch 2 the network was at 93.5% — a level Architecture 2 only reached after 10 full epochs. However, **final test accuracy was actually slightly lower than Architecture 2** (98.12% vs 98.43%), and for the first time training accuracy (98.86%) exceeded test accuracy — the classic signature of mild overfitting. Three takeaways:
1. The dataset has a natural performance ceiling around ~98% with 30x30 inputs and 10 epochs. More capacity stops paying off and starts costing in generalization.
2. The extra parameters were trained ~3x slower per epoch (13s vs 4s) for no accuracy gain.
3. Architecture 2 happened to land in a regularization sweet spot — its capacity matched the dataset's complexity, and a single Dropout(0.5) was sufficient to keep train and test aligned.

---

## Comparison and Conclusions

| Architecture | Test accuracy | Test loss | Time/epoch | Train acc | Notes |
|---|---|---|---|---|---|
| 1 — No conv | 84.12% | 0.6255 | ~2 s | 85.04% | No overfitting, but capacity-limited. |
| 2 — Standard CNN | **98.43%** | **0.0680** | ~4 s | 93.50% | Best test accuracy. Dropout regularizes well. |
| 3 — Deep CNN + BN | 98.12% | 0.0649 | ~13 s | 98.86% | Fastest convergence, but mild overfitting and 3x slower per epoch. |

### What worked

- **Convolutions are the single biggest lever.** Going from no convolutions (Arch 1) to two simple conv blocks (Arch 2) added 14 percentage points of test accuracy and dropped the test loss by an order of magnitude. Weight sharing across spatial positions matters far more than raw parameter count.
- **Dropout 0.5 before the output is a strong default** for this problem. In Architecture 2 it was sufficient to keep test accuracy slightly higher than training accuracy, indicating no overfitting at all.
- **BatchNormalization dramatically speeds up convergence.** Architecture 3 reached ~93% training accuracy by epoch 2; Architecture 2 needed 10 epochs to get there. If you are constrained to few epochs, BN buys you time.

### What did not work as expected

- **More layers did not equal better generalization.** Architecture 3 has roughly twice the parameters of Architecture 2 and a richer feature extractor (3 conv blocks vs 2, plus BN), yet it generalized slightly worse on the held-out test set. This is a clean illustration that adding capacity past what the dataset can support starts to overfit instead of helping.
- **The compute cost of Architecture 3 was not justified by the result.** Training was ~3x slower per epoch with no test-accuracy gain — a bad tradeoff in this setting.

### What I noticed

- Even a pure dense network reached ~84% on this dataset. That is much higher than I initially expected and reflects the fact that GTSRB images are pre-cropped and centered, so absolute pixel positions carry useful signal even without spatial inductive bias.
- The "test accuracy higher than training accuracy" pattern in Architecture 2 was confusing at first, but it turned out to be the expected effect of dropout being active during training (handicapping the live training metric) and disabled during evaluation. It is a sign of healthy regularization, not a bug.
- Diminishing returns set in fast. The jump from Arch 1 to Arch 2 was massive (+14 points). The jump from Arch 2 to Arch 3 was negative. The lesson: once a model is well-matched to the data, the next gains come from better data (augmentation, more samples, higher resolution) rather than deeper architectures.

### What I would try next

If pushing past 98.5% test accuracy were the goal, the productive directions would be:
- **Data augmentation** (random rotation, brightness shifts, small translations) — likely the highest-leverage change.
- **Larger input size** (e.g. 48x48 or 64x64) so finer details survive resizing.
- **Learning rate scheduling** (cosine decay or step decay) to squeeze the last fraction of a percent.
- More epochs with early stopping based on validation loss, rather than a fixed 10.

Adding more layers without addressing data quality is unlikely to help further on this dataset.

## Notes

- Image preprocessing: each `.ppm` file is read with `cv2.imread`, resized to 30x30 with `cv2.resize`, cast to `float32`, and normalized to `[0, 1]` by dividing by 255.
- Path handling uses `os.path.join` for cross-platform compatibility.
- Pixel normalization is performed inside `load_data` so `get_model` only deals with model architecture concerns.
