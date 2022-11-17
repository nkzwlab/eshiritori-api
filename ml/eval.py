import torch
import torch.nn as nn
import torch.nn.functional as F
import json
from model import Net
from decode_base64 import decode_base64,plot_image_tensor
from words import get_label_name, get_most_similar_word
# import torchvision.models as models
import torch
import torch.optim as optim
from dataset import QuickDrawDataset, get_loader
from train import train_loop
from distillation import distill_loop
from model import Net
import torch.nn as nn
from tqdm import tqdm
import wandb
from wandb import AlertLevel

# from torchmetrics import ConfusionMatrix

def eval_loop(
    net,
    data_loader,
    device,
    criterion,
):
    # print('***************************')
    # print('start eval')
    # print('***************************')
    net.eval()

    correct = 0
    total = 0
    confmat = ConfusionMatrix(num_classes=345)

    for i, (images, labels) in enumerate(data_loader):
        images, labels = images.to(device), labels.to(device)
        outputs = net.forward(images)
        
        loss = criterion(outputs, labels)

        _, predicted = torch.max(outputs.data, 1)

        # print(predicted.dtype,labels.dtype)
        # confmat = confmat(predicted, labels)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    acc = 100 * correct / total

    print(loss)
    print(f'Accuracy of the network on the test images: {acc:.2f}%')
    return acc #,confmat


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    net= Net(rn="resnet50").to(device)
    net.load_state_dict(torch.load("./weights/RN50_ver2_|_100_per_class_|_50_epochs.pth"))
    data_dir = './data'
    max_examples_per_class = 1000
    train_val_split_pct = .1
    batch_size = 128    
    shuffle = True
    num_workers = 0

    ds = QuickDrawDataset(
        root=data_dir,
        max_items_per_class=max_examples_per_class,
        class_limit=None,
        is_download=False,
    )
    train_ds, val_ds = ds.split(train_val_split_pct)
    val_loader = get_loader(val_ds, batch_size, shuffle, num_workers)
    
    criterion = nn.CrossEntropyLoss()

    acc = eval_loop(net,
    val_loader,
    device,
    criterion)

    print(acc)
    # plot_image_tensor(cm)