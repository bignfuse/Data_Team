import cv2
import os
import json
import argparse
import sys
from time import time
import multiprocessing as mp

# from .configs import CROP_CROPPED_SAVEDIR, CROP_SAVEDIR

def read_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    
    return data


def crop(image, data,key_json_data,img_name,saveDir):
    pad=5
    image=image[(data[0][1]-pad):(data[2][1]+pad),(data[0][0]-pad):(data[1][0]+pad)]
    key = key_json_data[data["id"]]
    if key and ('None' not in key):
        if cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
            save_name = img_name + '_' + str(key) + '.jpg'

            file_list = os.listdir(saveDir)
            save_file = os.path.join(saveDir, save_name)
            cv2.imwrite(save_file, cropped_image)

    return 


def save_cropped_image(image,img_path,std_json_path,key_json_path,form_type):
    # saveDir = 'cropped'
    print("---------------------Cropping image ---------------------")
    save_path_name=img_path.split('/')[-2]
    img_name = img_path.split('/')[-1].split('.jpg')[0]

    if form_type != "old":
        saveDir = f"new_cropped/{save_path_name}"
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
    else: 
        saveDir = f"old_cropped/{save_path_name}"
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        
    
   
    
    std_json_data = read_json(std_json_path+f"standard_{img_name}.json")
    std_data=std_json_data["fieldBBs"]
    key_json_data = read_json(key_json_path+f"mapping_dict_{img_name}.json")
    pool=mp.Pool(mp.cpu_count())
    for data in std_data:
        pool.apply_async(crop,args=(image, data['poly_points'],key_json_data,img_name,saveDir))
        
    