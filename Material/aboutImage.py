import torch
from torchvision import models, transforms
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import urllib.request

# Load pretrained ResNet model
model_resnet = models.resnet50(weights="IMAGENET1K_V1")
model_resnet.eval()

# Load BLIP model for image captioning
processor_blip = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model_blip = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Image preprocessing for ResNet
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load and preprocess image
image_path = "tt.jpg"  # Replace with your image path
img = Image.open(image_path)
img_t = preprocess(img).unsqueeze(0)

# Predict class label using ResNet
with torch.no_grad():
    output = model_resnet(img_t)
    _, predicted_class_idx = output[0].max(0)

# Download ImageNet class labels
url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
filename, _ = urllib.request.urlretrieve(url)
with open(filename, "r") as f:
    categories = [line.strip() for line in f.readlines()]

predicted_label = categories[predicted_class_idx.item()]

# Generate image caption using BLIP
inputs = processor_blip(images=img, return_tensors="pt")
out = model_blip.generate(**inputs)
caption = processor_blip.decode(out[0], skip_special_tokens=True)

# Display results
print(f"Predicted label: {predicted_label}")
print(f"Generated caption: {caption}")
