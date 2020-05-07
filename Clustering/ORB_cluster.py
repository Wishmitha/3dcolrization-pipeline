###########################################
'''
Command: 
  python ORB_cluster.py \
  --input_dir data/cactusgarden/color \
  --input_depth_dir data/cactusgarden/depth  \
  --output_dir = data/cactusgarden/ORB_0.45_filtered_500_color
  --output_depth_dir data/cactusgarden/ORB_0.45_filtered_500_depth  \
  --filter_blur 1
  --similar_threshold 0.45
  --blur_threshold 500.0

 python ORB_cluster.py --input_dir data/cactusgarden/color  --input_depth_dir data/cactusgarden/depth  --output_dir data/cactusgarden/ORB_0.45_filtered_500_color --output_depth_dir data/cactusgarden/ORB_0.45_filtered_500_depth 
 python ORB_cluster.py --input_dir data/stonewall/color  --input_depth_dir data/stonewall/depth  --output_dir data/stonewall/ORB_0.4_filtered_100_color --output_depth_dir data/stonewall/ORB_0.4_filtered_100_depth --similar_threshold 0.4 --blur_threshold 100.0
 python ORB_cluster.py --input_dir data/totempole/color  --input_depth_dir data/totempole/depth  --output_dir data/totempole/ORB_0.35_filtered_900_color --output_depth_dir data/totempole/ORB_0.35_filtered_900_depth --similar_threshold 0.35 --blur_threshold 900.0
 python ORB_cluster.py --input_dir data/burghers/color  --input_depth_dir data/burghers/depth  --output_dir data/burghers/ORB_0.4_filtered_400_color --output_depth_dir data/burghers/ORB_0.4_filtered_400_depth --similar_threshold 0.4 --blur_threshold 400.0
 python ORB_cluster.py --input_dir data/burghers/color  --input_depth_dir data/burghers/depth  --output_dir data/burghers/ORB_0.45_filtered_350_color --output_depth_dir data/burghers/ORB_0.45_filtered_350_depth --similar_threshold 0.45 --blur_threshold 350.0
'''
#######################################

import cv2
import os
import sys
import glob
import argparse
import time
import random
import shutil

## filter blurry images
def filter_blurriness(a):
    input_dir = a.input_dir
    # input_dir = "data\\cactusgarden\\color"
    threshold = a.blur_threshold
    # threshold = 500.0
    if not os.path.exists(input_dir):
        raise Exception("input_dir does not exist")
    input_paths = []
    input_paths = glob.glob(os.path.join(input_dir, "*.png"))
    if len(input_paths) == 0:
        input_paths = glob.glob(os.path.join(input_dir, "*.jpg"))
    if len(input_paths) == 0:
        raise Exception("input_dir contains no image files")

    clear_img_list = []
    for i in range(len(input_paths)):  
        img = cv2.imread(input_paths[i], cv2.IMREAD_GRAYSCALE)
        imageVar = cv2.Laplacian(img, cv2.CV_64F).var()

        if not imageVar < threshold:
            clear_img_list.append(i)

    return clear_img_list


def get_name(path):
    name, _ = os.path.splitext(os.path.basename(path))
    return name

## use ORB to calcualte two images' similarity
def img_similarity(img1,img2):
    """
    :param img1: gray image 1
    :param img2: gray image 2
    :return: image similarity
    """
    try:
        # initialize ORB detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # extract and calcualte feature points
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        # knn filter results
        matches = bf.knnMatch(des1, trainDescriptors=des2, k=2)

        # check max matches
        good = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
#         print(len(good))
#         print(len(matches))
        similary = len(good) / len(matches)
#         print("Similarity:%s" % similary)
        return similary

    except:
        print('Cannot compute similarity between these tow images')
        return '0'
    
def save_image(output_dir, input_path):
    if not os.path.exists(output_dir):
        try:
        # Create target Directory
            os.mkdir(output_dir)
            print("Directory " , output_dir ,  " Created ") 
        except FileExistsError:
            print("Directory " , output_dir ,  " already exists")

  
    img = cv2.imread(input_path)
    cv2.imwrite(os.path.join(output_dir, get_name(input_path) + ".png"), img)


def cluster_images(a, clear_img_list):
    input_dir = a.input_dir
    output_dir = a.output_dir
    threshold = a.similar_threshold
    # input_dir = "data\\cactusgarden\\color"
    # output_dir = "data\\cactusgarden\\ORB_0.45_filtered_500_color"
    # threshold = 0.45

    if not os.path.exists(input_dir):
        raise Exception("input_dir does not exist")
    
            
    input_paths = []
    input_paths = glob.glob(os.path.join(input_dir, "*.png"))
    if len(input_paths) == 0:
        input_paths = glob.glob(os.path.join(input_dir, "*.jpg"))
    if len(input_paths) == 0:
        raise Exception("input_dir contains no image files")
    
    if clear_img_list is None:
        clear_img_list = [i for i in range(len(input_paths))]
    #  calculate similarity between images    
#     N = len(input_paths)
    N = len(clear_img_list)
    k = 0
    img1_path = input_paths[clear_img_list[0]]
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    start = time.time()
    n_cluster = 0
    for i in range(1,N):   
        
        # read images
        img2_path = input_paths[clear_img_list[i]]
        img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
        score = img_similarity(img1, img2)
        
        end = time.time()
#         print("Image ", clear_img_list[i-1],"vs. Image", clear_img_list[i], " Similarity: ", score)
        
        if score < threshold or i == N-1:       
            end = time.time()
#             print("Save new image for a cluster -> Time: ", end-start, " sec")
            start = time.time()
            # save_image(output_dir, input_paths[clear_img_list[random.randint(k, i-1)]]) #save image
            save_image(output_dir, input_paths[clear_img_list[(k + i-1)//2]]) #save image
            n_cluster += 1
            k = i
        
        img1 = img2
    return n_cluster
        



def copy_dep_images(a):
    output_dir = a.output_dir
    input_depth_dir = a.input_depth_dir
    output_depth_dir = a.output_depth_dir
    # output_dir = "data\\cactusgarden\\ORB_0.45_filtered_500_color"
    # input_depth_dir = "data\\cactusgarden\\depth"
    # output_depth_dir = "data\\cactusgarden\\ORB_0.45_filtered_500_dep"
    if not os.path.exists(input_depth_dir):
        raise Exception("input_depth_dir does not exist")

    if not os.path.exists(output_depth_dir):
        try:
        # Create target Directory
            os.mkdir(output_depth_dir)
            print("Directory " , output_depth_dir ,  " Created ") 
        except FileExistsError:
            print("Directory " , output_depth_dir ,  " already exists")


    output_paths = []
    output_paths = glob.glob(os.path.join(output_dir, "*.png"))
    if len(output_paths) == 0:
        output_paths = glob.glob(os.path.join(output_dir, "*.jpg"))
    if len(output_paths) == 0:
        raise Exception("input_dep_dir contains no image files")

    for path in output_paths:
        name = get_name(path)
        source = os.path.join(input_depth_dir,(name + ".png"))
        dest = os.path.join(output_depth_dir,(name + ".png"))
        shutil.copyfile(source, dest) 



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", help="path to folder containing input images")
    parser.add_argument("--output_dir", help="path to folder containing output images")
    parser.add_argument("--input_depth_dir", help="path to folder containing input depth images")
    parser.add_argument("--output_depth_dir", help="path to folder containing output depth images")
    parser.add_argument("--similar_threshold", type=float, default= 0.45, help="similarity threshold, range(0,1)") # smaller, sample fewer
    parser.add_argument("--filter_blur", type=int, default=1, help="to filter blurry images (0 to disable)") 
    parser.add_argument("--blur_threshold", type=float, default=500, help="blurriness filtering threshold, range(0,2000)") #larger, filter more
    a = parser.parse_args()
    
    clear_img_list = []
    if a.filter_blur:
        f_start = time.time()
        clear_img_list = filter_blurriness(a)
        f_end = time.time()
        print("Remained #images: ",len(clear_img_list))
        print("Filtering, Time elapsed: %4f secs" % (f_end-f_start))

    else:
        clear_img_list = None

    start = time.time()
    n_cluster = cluster_images(a, clear_img_list)
    end = time.time()
    print("Filter + Cluster %d clusters, Time elapsed: %4f secs" % (n_cluster, end-start))

    copy_dep_images(a)
