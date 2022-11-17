import replicate
import webbrowser

model = replicate.models.get("stability-ai/stable-diffusion")
output_url = model.predict(prompt="a ball-point pen art of a dog, award-winning")[0]
print(output_url)
webbrowser.open(output_url)