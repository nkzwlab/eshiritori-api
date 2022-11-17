import torch
import torch.optim as optim
from dataset import QuickDrawDataset, get_loader
from train import train_loop
from distillation import distill_loop
from eval import eval_loop
from model import Net
import torch.nn as nn
from tqdm import tqdm
import wandb
from wandb import AlertLevel


if __name__ == '__main__':
    teacher_name = "resnet152"
    which_teacher = "resnet152"
    student_name = "resnet50_from_resnet152"
    which_student = "resnet50"

    data_dir = './data'
    max_examples_per_class = 1000#15000
    train_val_split_pct = .1
    lr = 0.01
    num_epochs = 50
    batch_size = 128
    shuffle = True
    num_workers = 0
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)

    ds = QuickDrawDataset(
        root=data_dir,
        max_items_per_class=max_examples_per_class,
        class_limit=None,
        is_download=False,
    )
    
    train_ds, val_ds = ds.split(train_val_split_pct)
    
    train_loader = get_loader(train_ds, batch_size, shuffle, num_workers)
    val_loader = get_loader(val_ds, batch_size, shuffle, num_workers)
    

    teacher = Net(rn = which_teacher).to(device)
    teacher.load_state_dict(torch.load(f"weights/{teacher_name}_latest.pth"))
    student = Net(rn = which_student).to(device)


    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(student.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs, last_epoch=-1)
    
    wandb_config = dict(
        project="orf_eshiritori",
        group="distill",
        name="RN50D152 | 15000 per class | 50epochs"
    )

    with wandb.init(job_type="train",**wandb_config):

        print("starting training...")
        best_val_acc = 0

        for epoch in tqdm(range(1, num_epochs)):

            loss,ce_loss,kd_loss = distill_loop(teacher, student, train_loader, device, criterion, optimizer)
            acc = eval_loop(student, val_loader, device, criterion)

            print(f"Epoch: {epoch}, Loss: {loss}, CE_Loss:{ce_loss}, KD_Loss:{kd_loss} , Accuracy: {acc}")
            wandb.log({"epoch":epoch,"loss":loss,"acc":acc,"ce_loss":ce_loss,"kd_loss":kd_loss})

            if acc > best_val_acc:
                best_val_acc = acc
                print("saving model...")
                torch.save(student.state_dict(), f"weights/{student_name}_best.pth")
                print("done.")
            
            scheduler.step()

        print("done.")

        print("saving model...")
        # save the model
        torch.save(student.state_dict(), f"weights/{student_name}.pth")
        print("done.")

    wandb.alert(
    title="ORF 絵しりとり",
    text="<@U013HNPE0GG> 学習終了しました",
    level=AlertLevel.INFO
    )