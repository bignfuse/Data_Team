# from crop import save_cropped_image
from crop_test import save_cropped_image
from file_utils import split_and_save_pdf_images,is_new_form
import os
from align import alignImages
from glob import glob
import pandas as pd
import argparse
import time


def Crop_map(file_path):
    pdf_path=file_path
    label=open("label.txt","w")
    for p in glob(pdf_path+"/*.pdf"):
        saved_pdf=split_and_save_pdf_images(p)
        page_3_img_path = os.path.join(saved_pdf,"3.jpg")
        form_type= is_new_form(page_3_img_path)
        if form_type== True:
            form_type="new"
            std_json_path=f"{form_type}/standard_json_files/"
            key_json_path=f"{form_type}/key_value_mapping_json_files/"
        elif form_type==False:
            form_type="old"
            std_json_path=f"{form_type}/standard_json_files/"
            key_json_path=f"{form_type}/key_value_mapping_json_files/"
        print("form type: ",form_type)
        for n,c in enumerate(os.listdir(saved_pdf)):
            if n>2:
                break
            pdf_image_path=os.path.join(saved_pdf,c)
            aligned_img=alignImages(pdf_image_path,f"{form_type}/template_image/template_{c.split('.')[0]}.jpg")
            save_cropped_image(aligned_img,pdf_image_path,std_json_path,key_json_path,form_type)
        data=pd.read_csv(f"{file_path}/data_{'_'.join(p.split('/')[-1].split('.')[0].split('_')[:-1])}.csv",names=["key","values"])
        if data.index.name != "key":
            data=data.set_index("key")
        crop_dir=f"{form_type}_cropped/{p.split('/')[-1].split('.')[0]}"
        print(f"---------------------Crop and Label Mapping for File {p} ---------------------")
        for crop in os.listdir(crop_dir):
            key_name=crop.split("_")
            if len(key_name)>2:
                key_name=' '.join(key_name[1:len(key_name)]).split(".")[0]
            else:
                key_name= key_name[-1].split(".")[0]
            if(key_name in list(data.index.values)):
                values=data.loc[key_name,"values"]
                label.write(f"{crop_dir}/{crop} {values}\n")
            else:
                label.write(f"{crop_dir}/{crop} check\n")

    label.close()  
def csv_split(xls_path,file_path):
    print("---------------------csv split---------------------")
    df = pd.read_excel(xls_path, sheet_name=None)  
    for key,values in df.items():
        print(f'{file_path}/data_{key}.csv')
        df[key].to_csv(f'{file_path}/data_{key}.csv')    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, required=True)
    parser.add_argument('--xls_path',type=str, required=False)
    args = parser.parse_args()
    t1=time.time()
    if args.xls_path is not None:
        csv_split(args.xls_path,args.file_path)
    Crop_map(args.file_path)
    print("Total time taken:",time.time()-t1)
