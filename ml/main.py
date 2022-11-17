import torch
import torch.optim as optim
from dataset import QuickDrawDataset, get_loader
from train import train_loop
from eval import eval_loop
from model import Net
import torch.nn as nn
from tqdm import tqdm
import wandb
from wandb import AlertLevel


if __name__ == '__main__':
    model_name = "RN50_ver1_|_1000_per_class_|_3_epochs"
    which_resnet = "resnet50"
    data_dir = './data'
    max_examples_per_class = 1000#15000 #15000
    train_val_split_pct = .1
    lr = 0.01
    num_epochs = 3
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

    # sample_images, sample_labels = next(iter(train_loader))
    # print(sample_images.shape)
    
    net = Net(rn = which_resnet).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs, last_epoch=-1)
    
    wandb_config = dict(
        project="orf_eshiritori",
        group="test",
        name="RN50 ver1 | 1000 per class | 3 epochs"
    )

    with wandb.init(job_type="train",**wandb_config):

        print("starting training...")
        best_val_acc = 0

        for epoch in tqdm(range(1, num_epochs)):

            loss = train_loop(net, train_loader, device, criterion, optimizer)
            acc = eval_loop(net, val_loader, device, criterion)

            print(f"Epoch: {epoch}, Loss: {loss}, Accuracy: {acc}")
            wandb.log({"epoch":epoch,"loss":loss,"acc":acc,"lr":optimizer.param_groups[0]['lr']})

            if acc > best_val_acc:
                best_val_acc = acc
                print("saving model...")
                torch.save(net.state_dict(), f"weights/{model_name}_best.pth")
                print("done.")

            scheduler.step()

        print("done.")

        print("saving model...")
        # save the model
        torch.save(net.state_dict(), f"weights/{model_name}.pth")
        print("done.")

    wandb.alert(
    title="ORF 絵しりとり",
    text="<@U013HNPE0GG> 学習終了しました",
    level=AlertLevel.INFO
    )