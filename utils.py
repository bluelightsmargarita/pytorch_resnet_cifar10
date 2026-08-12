import numpy as np
import torch


class Cutout(object):
    def __init__(self, n_holes, length):
        self.n_holes = n_holes
        self.length = length

    def __call__(self, img):

        h = img.size(1)
        w = img.size(2)

        mask = np.ones((h, w), np.float32)

        for _ in range(self.n_holes):

            y = np.random.randint(h)
            x = np.random.randint(w)

            y1 = np.clip(y - self.length // 2, 0, h)
            y2 = np.clip(y + self.length // 2, 0, h)

            x1 = np.clip(x - self.length // 2, 0, w)
            x2 = np.clip(x + self.length // 2, 0, w)

            mask[y1:y2, x1:x2] = 0.

        mask = torch.from_numpy(mask)

        mask = mask.expand_as(img)

        img = img * mask

        return img

def mixup_data(x, y, alpha=1.0):
    """
    Mixup data augmentation

    x: input images
    y: labels
    alpha: beta distribution parameter
    """

    if alpha > 0:
        lam = np.random.beta(alpha, alpha)
    else:
        lam = 1


    batch_size = x.size()[0]

    index = torch.randperm(batch_size).to(x.device)


    mixed_x = lam * x + (1 - lam) * x[index, :]

    y_a, y_b = y, y[index]


    return mixed_x, y_a, y_b, lam

def mixup_criterion(criterion, pred, y_a, y_b, lam):
    """
    Mixup loss calculation
    """

    return (
        lam * criterion(pred, y_a)
        +
        (1 - lam) * criterion(pred, y_b)
    )