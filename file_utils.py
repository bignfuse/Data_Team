import os
from pdf2image import convert_from_path
from mtcnn.mtcnn import MTCNN
import cv2

def remove_files(directory_):
    if not os.path.exists(directory_):
        os.mkdir(directory_)
    for i in os.listdir(directory_):
        path_ = os.path.join(directory_, i)
        os.remove(path_)

def is_new_form(img):
    page3_img=cv2.imread(img)
    detector = MTCNN()
    faces = detector.detect_faces(page3_img)
    if len(faces)>0:
        return True
    else:
        return False

def split_and_save_pdf_images(pdf_path):
    print("---------------------Splitting Pdf---------------------")
    save_directory="saved_pdf_images/"+pdf_path.split("/")[-1].split(".")[0]+"/"
    print(save_directory)
    if not os.path.exists(save_directory):
            os.makedirs(save_directory)
    print(pdf_path)
    images = convert_from_path(pdf_path)
    for i in range(len(images)):
        if i<=3:
            file_name=str(i+1) +'.jpg'
            file_path=os.path.join(save_directory,file_name)
            images[i].save(file_path, 'JPEG') 
            print(f"-------------Image saved at:: {file_path}")

        else:
            break
    return save_directory

     