import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)

# image = preprocess(Image.open("server/data/CLIP.png")).unsqueeze(0).to(device)
# text = clip.tokenize(["a diagram", "a diagram of neural network", "a cat"]).to(device)


def encode_text(text):
    text = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
    return text_features


def encode_image(img_path):
    with torch.no_grad():
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
        image_features = model.encode_image(image)

    return image_features


