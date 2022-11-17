from PIL import Image
import base64
import io
import numpy as np
import torch
from matplotlib import pyplot as plt
import torchvision.transforms as T


def decode_base64(base64_string,resize = 224):

    transform_size = T.Resize(resize)

    base64_decoded = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(base64_decoded))
    image = image.convert('L')
    image = transform_size(image)
    image_tensor = torch.tensor(np.array(image)).float()
    return image_tensor

def plot_image_tensor(image_tensor):
    image_np = image_tensor.numpy()
    plt.imshow(image_np, interpolation='nearest')
    plt.show()
    plt.savefig('test.png')
    
