from torch import nn
import torchvision.models as models

class Net(nn.Module):
    def __init__(self, num_classes=345, pretrained=False, rn="resnet50"):
        super(Net, self).__init__()   
        if rn == "resnet18":
            model = models.resnet18(pretrained=pretrained)
        elif rn == "resnet34":
            model = models.resnet34(pretrained=pretrained)     
        elif rn == "resnet50":
            model = models.resnet50(pretrained=pretrained)
        elif rn == "resnet101":
            model = models.resnet101(pretrained=pretrained)
        elif rn == "resnet152":
            model = models.resnet152(pretrained=pretrained)        
        else:
            raise ValueError("rn must be one of resnet18, resnet34, resnet50, resnet152, resnet101")

        model.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=64,
            kernel_size=model.conv1.kernel_size, #7,7,
            stride=model.conv1.stride,
            padding=model.conv1.padding, #3,3,
            bias=False
        )
        
        # model.conv1 = nn.Conv2d(
        #     in_channels=1,
        #     out_channels=64,
        #     kernel_size=3,#model.conv1.kernel_size 7,7,
        #     stride=1,#model.conv1.stride,
        #     padding=2,#model.conv1.padding 3,3,
        #     bias=False
        # )
        
        model.fc = nn.Linear(
            in_features=model.fc.in_features,
            out_features=num_classes
        )
        
        self.resnet = model
        
    def forward(self, images):
        return self.resnet(images)

if __name__ == '__main__':
    net = Net()
    print(net)
    print(net.resnet.conv1.kernel_size)
    print(net.resnet.conv1.stride)
    print(net.resnet.conv1.padding)