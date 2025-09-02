import torch
import cv2
import numpy as np
from PIL import Image
import sys
import os
# Add the U-2-Net directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'U-2-Net'))
try:
    from u2net import U2NETP  # Try the direct import
except ImportError:
    print("Failed to import U2NETP from u2net.py. Checking alternative path...")
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'U-2-Net', 'model'))  # Try model subfolder if needed
    from u2net import U2NETP  # Retry import

# Load pre-trained U2-Net model
model = U2NETP(3, 1)
model.load_state_dict(torch.load("saved_models/u2netp.pth", map_location=torch.device('cpu')))
model.eval()

def detect_clothing(image_path, output_path):
    # Load and preprocess image
    img = Image.open(image_path).convert("RGB")
    img = img.resize((320, 320), Image.BILINEAR)  # Resize for efficiency
    img = np.array(img) / 255.0
    img = torch.from_numpy(img.transpose((2, 0, 1))).float().unsqueeze(0)
    
    # Run inference
    with torch.no_grad():
        mask = model(img)
        if isinstance(mask, tuple):  # Check if output is a tuple
            mask = mask[0]  # Take the first element (saliency map)
        mask = mask.squeeze(0).cpu().numpy()[0]  # Process the saliency map
    
    # Post-process mask
    mask = (mask * 255).astype(np.uint8)
    _, mask_binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    
    # Resize mask back to original image size
    original = cv2.imread(image_path)
    mask_binary = cv2.resize(mask_binary, (original.shape[1], original.shape[0]), interpolation=cv2.INTER_NEAREST)
    
    # Save mask and processed image
    cv2.imwrite(output_path, mask_binary)
    return mask_binary

if __name__ == "__main__":
    detect_clothing("static/uploads/cloth_0.jpg", "static/uploads/cloth_0_clothing.jpg")