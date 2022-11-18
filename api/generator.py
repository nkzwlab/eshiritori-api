import replicate
import os
import requests
import base64
from PIL import Image
from io import BytesIO
import json
import random

def generate_img(word: str):
    # TODO: tokenをリセットするロジックが必要かも
    
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("8abccf52e7cba9f6e82317253f4a3549082e966db5584e92c808ece132037776")
    output_url = version.predict(prompt='a ball-point pen art of a {}'.format(word))
    
    response = requests.get(output_url[0])
    img = Image.open(BytesIO(response.content))
    img = img.resize((500, 500))
    img = img.convert(mode="1")
    
    return pil_to_base64(img)
    
def pil_to_base64(img, format='png'):
    buffer = BytesIO()
    img.save(buffer, format)
    
    return base64.b64encode(buffer.getvalue())

def generate_next_word(first_letter: str):
    with open("api/generatable_word.json") as f:
        jsn = json.load(f)
        
    word_dict = random.choice(jsn[first_letter])
    ja = list(word_dict.keys())[0]
    en = list(word_dict.values())[0]
    
    return ja, en
    
if __name__ == '__main__':
    # img = generate_img('dog')
    
    print(generate_next_word('あ'))