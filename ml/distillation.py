import torch
import torch.nn as nn
import torch.nn.functional as F
from dataset import QuickDrawDataset, get_loader
from tqdm import tqdm

def distill_loop(
    teacher,
    student,
    data_loader,
    device,
    criterion,
    optimizer,
    T=2,
    lambda_=0.9
):

    student.train()
    teacher.eval()

    accum_loss = 0
    
    for i, (images, labels) in enumerate(data_loader):
        # print(labels)
        optimizer.zero_grad()

        images, labels = images.to(device), labels.to(device)

        outputs = student.forward(images)
        teacher_outputs = teacher.forward(images)
        
        ce_loss = criterion(outputs, labels)
        kd_loss = nn.KLDivLoss()(F.log_softmax(outputs/T, dim=1),F.softmax(teacher_outputs/T, dim=1)) * (T * T)

        loss = lambda_ * ce_loss + (1 - lambda_) * kd_loss

        accum_loss += loss.item()
        # print(loss)
        
        loss.backward()
        optimizer.step()

        loss = accum_loss / len(data_loader)

    return loss, ce_loss, kd_loss