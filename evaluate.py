import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import resnet

# =====================
# 参数
# =====================
model_path = "experiments/resnet32_baseline/checkpoints/model_best.pth"
arch = "resnet32"

# =====================
# GPU
# =====================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================
# 数据
# =====================

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        (0.4914, 0.4822, 0.4465),
        (0.2023, 0.1994, 0.2010)
    ),
])

testset = torchvision.datasets.CIFAR10(
    root="./data",
    train=False,
    download=True,
    transform=transform_test
)

testloader = torch.utils.data.DataLoader(
    testset,
    batch_size=128,
    shuffle=False,
    num_workers=0
)

# =====================
# 模型
# =====================

model = resnet.__dict__[arch]()
checkpoint = torch.load(
    model_path,
    map_location=device
)

model.load_state_dict(
    checkpoint["state_dict"]
)
model.to(device)
model.eval()

# =====================
# 测试
# =====================
correct = 0
total = 0
with torch.no_grad():
    for images, labels in testloader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
acc = 100. * correct / total
print(
    "Best Model Accuracy: {:.2f}%".format(acc)
)