
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms

from .model import BiSeNet
from .utils import arrange_mask, get_one_hot
from ..utils import check_ckpt_exist, convert_image_type

# index = [
# 1 'skin', 2 'l_brow', 3 'r_brow', 4 'l_eye', 5 'r_eye', 6 'eye_g', 
# 7 'l_ear', 8 'r_ear', 9 'ear_r', 10 'nose', 
# 11 'mouth', 12 'u_lip', 13 'l_lip', 
# 14 'neck', 15 'neck_l', 16 'cloth', 17 'hair', 18 'hat']

class FaceParser(nn.Module):
    def __init__(self, root='~/.invz_packages/face_parser', ckpt_name = 'faceparser.pth', url_id = '1h5CG5VftFVtvS59fyZQzetlK_Nmyrjhj', force=False):
        super(FaceParser, self).__init__()
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.parsing_net = BiSeNet(n_classes=19).to(device)
        
        ckpt_path = check_ckpt_exist(root, ckpt_name = ckpt_name, url_id = url_id, force = force)
        ckpt = torch.load(ckpt_path, map_location=device)
        
        self.parsing_net.load_state_dict(ckpt)
        for param in self.parsing_net.parameters():
            param.requires_grad = False
        self.parsing_net.eval()
        del ckpt

        self.GaussianBlur = transforms.GaussianBlur(kernel_size=5, sigma=(0.1, 5))
        self.kernel = torch.ones((1,1,5,5), device="cuda")
        
        self.transform = transforms.Compose([
            transforms.Resize((512,512)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def data_preprocess(self, input):
        pil_img = convert_image_type(input)
        tensor_img = self.transform(pil_img).unsqueeze(0).cuda()
        return tensor_img
        
    def data_postprocess(self, tensor_label):
        cv2_label = tensor_label.squeeze().cpu().numpy()
        return cv2_label
    
    def get_label(self, tensor_img, size=512):
        label = self.parsing_net(tensor_img)
        _label = F.interpolate(label, (size,size), mode='bilinear').max(1)[1]
        _label = arrange_mask(_label, size)
        return _label
    
    def get_onehot(self, tensor_img, size=512):
        label = self.get_label(tensor_img, size)
        onehot = get_one_hot(label)
        return onehot