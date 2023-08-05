import torch.nn.functional as F
import numpy as np
import warnings; warnings.filterwarnings('ignore')
from insightface.app import FaceAnalysis # pip install -U insightface

from ..utils import convert_image_type

class LmkDetector:
    def __init__(self,):
        self.app = FaceAnalysis(providers=['CUDAExecutionProvider'], allowed_modules=['detection', 'landmark_2d_106'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def data_preprocess(self, input):
        pil_img = convert_image_type(input, target='pillow')
        return np.array(pil_img)

    def data_postprocess(self, inputs):
        results = []
        for input in inputs:
            results.append(input[:,:,::-1])
        return results

    def get_landmark(self, image, get_5pts=True):
        W, H = image.shape[:2]
        faces = self.app.get(np.pad(image, ((W//4, W//4), (H//4, H//4), (0, 0))))
        
        faces_count = len(faces)
        faces_lmks, faces_bool = [], []
        if len(faces):
            for idx in range(faces_count):
                lmk = faces[idx].landmark_2d_106 - [[H//4, W//4]]
            
                if get_5pts:
                    lmk = np.array([lmk[38], lmk[88], lmk[86], lmk[52], lmk[61]])
                    
                faces_bool.append(True)
                faces_lmks.append(lmk)
                
            return faces_count, faces_lmks, faces_bool
        
        elif not len(faces):
            return 0, None, None