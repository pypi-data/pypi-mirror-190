import os
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

import warnings; warnings.filterwarnings('ignore')

from .nets import Backbone
from ..utils import check_ckpt_exist, convert_image_type

class IdExtractor(nn.Module):
    def __init__(self, x=32, y=32, w=192, h=192 , root='~/.invz_packages/id_extractor', ckpt_name = 'currface.pth', url_id = '15xnMCs8udpODpSGwbePuhJqDoDeE0SA7', force=False):
        """
        Methods
        --------
        forward(tesnor_img : tensor) -> id_vector : tensor
        
        data_preprocess(img_path : str) -> tensor_img : tensor
        
        compare_similarity(id_vector_1 : tensor, id_vector_2 : tensor) -> score : float
        """
        super(IdExtractor, self).__init__()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.id_extractor = Backbone().to(device).eval()
        
        ckpt_path = check_ckpt_exist(root, ckpt_name = ckpt_name, url_id = url_id, force = force)
        ckpt = torch.load(ckpt_path, map_location=device)

        self.id_extractor.load_state_dict(ckpt)
        for param in self.id_extractor.parameters():
            param.requires_grad = False
        del ckpt

        self.x, self.y, self.w, self.h = x, y, w, h

        self.transform = transforms.Compose([
            transforms.Resize((256, 256), interpolation=Image.BILINEAR),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
    def data_preprocess(self, input):
        """
        
        """
        pil_img = convert_image_type(input)
        tensor_img = self.transform(pil_img).unsqueeze(0).cuda()
        return tensor_img
        
    def forward(self, tensor_img):
        """
        
        """
        tensor_img = F.interpolate(tensor_img[..., self.y:self.y+self.h, self.x:self.x+self.w], (112, 112), mode='bilinear')
        id_vector = self.id_extractor(tensor_img)
        return id_vector
    
    def compare_similarity(self, id1, id2):
        """
        
        """
        score = torch.cosine_similarity(id1, id2, dim=1).mean().item()
        return score
    
