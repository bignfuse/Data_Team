import numpy as np
import imutils
import cv2
import os

orb = cv2.xfeatures2d.SIFT_create()
bf = cv2.BFMatcher()

def alignImages(img_path, template_path, file_id=None,validate_form=False):
    # print(f"PATH OF THE IMAGE: {img_path}")
    # print(f"Current path: {os.listdir()}")
    print("---------------------Aligning Image---------------------")
    img1_color = cv2.imread(img_path)
    img1_gray = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
    img_template = cv2.imread(template_path)
    template = cv2.cvtColor(img_template, cv2.COLOR_BGR2GRAY)
    # orb = cv2.xfeatures2d.SIFT_create()
    kp1, dec1 = orb.detectAndCompute(template, None)
    kp2, dec2 = orb.detectAndCompute(img1_gray, None)

    # bf = cv2.BFMatcher()

    matches = bf.knnMatch(dec1,dec2, k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append([m])

    ref_matched_kpts = np.float32([kp1[m[0].queryIdx].pt for m in good])
    sensed_matched_kpts = np.float32([kp2[m[0].trainIdx].pt for m in good])


    H, status = cv2.findHomography(sensed_matched_kpts, ref_matched_kpts, cv2.RANSAC,5.0)

    warped_image = cv2.warpPerspective(img1_gray, H, (template.shape[1], template.shape[0]), borderMode=3)
    
    if validate_form:
        if not match_template(warped_image, template):
            warped_image = None
            return warped_image
    
    return warped_image



# if __name__ == '__main__':
#     img = cv2.imread('/mnt/fuse-extract-v3/data/nmb/annotation-data/NMB_annotated/CASA-0000164594-process.jpg')
#     reference_img = cv2.imread('/mnt/fuse-extract-v3/data/nmb/annotation-data/NMB-Bank_standard.jpg')

#     # aligned_image = align_images(img, reference_img)
#     # cv2.imwrite('align.jpg', aligned_image)
#     print(reference_img.shape)