import os
import gdown

def check_ckpt_exist(root, ckpt_name, url_id, force):
    _root = os.path.expanduser(root)
    if not os.path.exists(_root):
            os.makedirs(_root)
            
    dir_path = os.path.join(_root, ckpt_name)
    if force:
        print('download_path :', dir_path)
        download_file(save_path = dir_path, url_id = url_id)
        return dir_path
        
    elif os.path.exists(dir_path):
        return dir_path
    
    else:
        print('download_path :', dir_path)
        download_file(save_path = dir_path, url_id = url_id)
        return dir_path

def download_file(save_path, url_id):
    """
    https://github.com/wkentaro/gdown
    """
    url = 'https://drive.google.com/u/0/uc?id=' + url_id + '&export=download'
    gdown.download(url, save_path, quiet=False)
        