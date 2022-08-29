import cv2
import os
import json
import argparse
import sys
from time import time
import multiprocessing as mp
from multiprocessing import pool
 
from multiprocessing.dummy import Pool as ThreadPool



def read_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    
    return data


# def crop(image,img_name,saveDir,data,key_json_data):
def crop(data):
    pad=5
    points=data['poly_points']
    cropped_image=img[(points[0][1]-pad):(points[2][1]+pad),(points[0][0]-pad):(points[1][0]+pad)]
    key = key_json_data[data["id"]]
    if key and ('None' not in key):
        if cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                save_name = img_name + '_' + str(key) + '.jpg'
                file_list = os.listdir(saveDir)
                save_file = os.path.join(saveDir, save_name)
                cv2.imwrite(save_file, cropped_image)
    


def save_cropped_image(image,img_path,std_json_path,key_json_path,form_type):
    # saveDir = 'cropped'
    print("---------------------Cropping image ---------------------")
    save_path_name=img_path.split('/')[-2]
    global img_name  
    img_name = img_path.split('/')[-1].split('.jpg')[0]
    global saveDir
    if form_type != "old":
         
        saveDir = f"new_cropped/{save_path_name}"
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
    else:  
        saveDir = f"old_cropped/{save_path_name}"
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        
    
   
    global img
    img=image
    std_json_data = read_json(std_json_path+f"standard_{img_name}.json")
    std_data=std_json_data["fieldBBs"]
    
    global key_json_data 
    key_json_data = read_json(key_json_path+f"mapping_dict_{img_name}.json")
    # pool=mp.Pool(mp.cpu_count())
    # print(mp.cpu_count())
    pool = ThreadPool(4)
    pool.map(crop,std_data)
    # for data in std_data:
    #     # cropped_image = crop(image,img_name,saveDir,data,key_json_data)
    #     pool.apply_async(crop,args=(image,img_name,saveDir,data,key_json_data))
    # pool.close()
    # pool.join()
       

    