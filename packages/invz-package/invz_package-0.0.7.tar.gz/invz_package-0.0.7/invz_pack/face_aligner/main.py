import numpy as np

from .utils import align_face
from ..lmk_detector import LmkDetector
from ..utils import convert_image_type

import warnings; warnings.filterwarnings('ignore')

class FaceAligner:
    def __init__(self, size=1024):
        self.LD = LmkDetector()
        self.size = size

    def data_preprocess(self, input):
        pil_img = convert_image_type(input, target='pillow')
        _pil_img = np.array(pil_img)
        return _pil_img

    def data_postprocess(self, inputs):
        results = []
        for input in inputs:
            results.append(input[:,:,::-1])
        return results

    def get_align_face(self, image, lmk=None):
        if lmk is None:
            faces_count, faces_lmks, faces_bool = self.LD.get_landmark(image, get_5pts=True)
            if faces_count == 0:
                raise RuntimeError("There isn't exist any face in image!!")
            
            else:
                alinged_faces, trans_invs = [], []
                for idx in range(faces_count):
                    face_lmks = faces_lmks[idx]
                    aligned_face, trans_inv= align_face(image, face_lmks, self.size)
                    alinged_faces.append(aligned_face)
                    trans_invs.append(trans_inv)
                    
                return alinged_faces, trans_invs
            
        elif len(lmk) ==  5:
            aligned_face, trans_inv= align_face(image, lmk, self.size)
            
            return [aligned_face], [trans_inv]
            
        elif len(lmk) == 106:
            lmk = np.array([lmk[38], lmk[88], lmk[86], lmk[52], lmk[61]])
            aligned_face, trans_inv= align_face(image, lmk, self.size)
            
            return [aligned_face], [trans_inv]
