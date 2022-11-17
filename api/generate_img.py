import replicate

def generate_img(word: str):
    model = replicate.models.get("stability-ai/stable-diffusion")
    output_url = model.predict(prompt="a ball-point pen art of a {}, award-winning".format(word))[0]
    return output_url
