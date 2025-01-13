import torch
import torch.nn
import cv2
import sys
import torchvision.transforms as transforms
import numpy as np
import torch.nn.functional as F

from model import Encoder
from imagecleaner import StraightenImage, resize, Load_image


class StraightenTransform(object):
    def __call__(self, x):
        image = np.array(x)
        image = StraightenImage(image)
        #print(image.shape)
        if image is None or image.shape[0] < 50 or image.shape[1] < 50:
            return x
        else:
            return image


def get_face_tensor(imgfile, device):
    image = Load_image(imgfile)

    transform = transforms.Compose([
    StraightenTransform(),
    transforms.ToTensor(),
    transforms.Pad(3), # adds 6 to both the height and width to make it 256,256
    transforms.Resize((128,128))
])

    tensorface = transform(image)
    return tensorface








def compareImages(face1, face):
    device = torch.device('cpu')
    emb10 = get_face_tensor(face1, device).to(device)
    emb20 = get_face_tensor(face, device).to(device)
    
    

    features = 18
    # embedding2 = RunModel(face)
    
    img_size = emb10.shape
    model = Encoder(features, img_size).to(device)
    model.load_state_dict(torch.load("Saved_model.pth", map_location=torch.device('cpu'))) # ensures that the model can be ran on the cpu 
    model.eval()
    emb1 = model(emb10.unsqueeze(0))
    emb2 = model(emb20.unsqueeze(0))

    is_same_prediction = model.isSame(emb10.unsqueeze(0), emb20.unsqueeze(0))

    # emb1 = F.normalize(emb1, p=2, dim=1)
    # emb2 = F.normalize(emb2, p=2, dim=1)
    # similarity = torch.sum(emb1*emb2, dim=1)
    # #print(similarity)
    # is_same = similarity > 0.7
    return is_same_prediction



