import torch
import torch.nn as nn
import torch.nn.functional as F
import json
from ml.model import Net
from ml.decode_base64 import decode_base64
from ml.words import get_label_name, get_most_similar_word
# import torchvision.models as models

def infer(model,image,top_n=5):
    model.eval()
    with torch.no_grad():
        output = model(image)
        # output = F.softmax(output,dim=1)
        values, indices = torch.topk(output, top_n)
        # _, pred = torch.max(output, 1)
        return values, indices
    
def predict_with_first_letter(
    base64_encoded_img, 
    first_letter,
    resnet_model,
    word2vec_model,
):
    image_tensor = decode_base64(base64_encoded_img)

    print("running inference...")
    values, indices = infer(resnet_model, image_tensor.unsqueeze(0).unsqueeze(0), top_n=5)
    print("done.")

    for value, index in zip(values[0], indices[0]):
        print(f"{get_label_name(index.item())}: {value.item()}")

    top_indice = indices[0]
    top_word = get_label_name(top_indice[0].item())
    
    print("")
    print(f"top word: {top_word}")
    print("")

    print("getting most similar word...")
    print("")
    if top_word[0] == first_letter:
        most_similar_word = top_word
        print(f"most similar word is: {most_similar_word}")
        return most_similar_word
    else:
        most_similar_word = get_most_similar_word(first_letter,top_word, model=word2vec_model ,nearest_n=15)
        print(f"most similar word is: {most_similar_word}")
        return most_similar_word

if __name__ == '__main__':

    # print(models.resnet18())
    # print( Net(rn="resnet18"))
    first_letter = "ね"

    net = Net(rn="resnet50")

    print("")
    print("loading model...")
    # net.load_state_dict(torch.load("./weights/RN50_ver2_|_100_per_class_|_50_epochs.pth"))
    net.load_state_dict(torch.load("./weights/resnet50_best.pth"))
    print("done.")
    

    base64_string = json.load(open("./src/base64.json"))["cat"]#["base64_text"]

    image_tensor = decode_base64(base64_string)

    # print(net.resnet.conv1)
    # print(list(net.parameters())[0].dtype)
    # print(image_tensor.dtype)

    print("")
    print("running inference...")
    values, indices = infer(net, image_tensor.unsqueeze(0).unsqueeze(0), top_n=5)
    print("done.")

    for value, index in zip(values[0], indices[0]):
        print(f"{get_label_name(index.item())}: {value.item()}")

    top_indice = indices[0]
    top_word = get_label_name(top_indice[0].item())
    
    print("")
    print(f"top word: {top_word}")
    print("")

    print("getting most similar word...")
    print("")
    if top_word[0] == first_letter:
        most_similar_word = top_word
        print(f"most similar word is: {most_similar_word}")
    else:
        most_similar_word = get_most_similar_word(first_letter,top_word,nearest_n=15)
        print(f"most similar word is: {most_similar_word}")
