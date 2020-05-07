'''Generate key.log camera pose matrix file for give a set of clustered images
from the trajectory.log file of the original dataset.
Also filter out the relevant depth images from the original dataset for the
clustered set of images.'''

import open3d as o3d
import os, sys
sys.path.append("Utility")
import numpy as np

from file import *

origin_path = os.path.realpath("../Data/burgers/burgers-full") #path orignal set of images
clustered_path = os.path.realpath("../Data/burgers/burgers-k345") #path for clustered images

#depth_image_path = get_file_list(os.path.join(path, "depth/"), extension=".png")
clustered_image_list = get_file_list(os.path.join(clustered_path, "image/"),extension=".png")

clustered_img_indexes = []
for img in clustered_image_list:
    clustered_img_indexes.append(int(img.split('.')[0].split('/')[-1].strip("0")))

#clustered_img_indexes = np.array(clustered_img_indexes)
print(clustered_img_indexes)
camera = o3d.io.read_pinhole_camera_trajectory(os.path.join(origin_path, "scene/key.log"))


extrinsic_mat_list=[]
for index in clustered_img_indexes:
    extrinsic_mat_list.append(camera.parameters[index].extrinsic)

f = open(os.path.join(clustered_path, "scene/key.log"), "w")
for i in range(0,len(extrinsic_mat_list)):
    f.writelines(str(i)+" "+str(i)+" "+str((i+1))+'\n')
    for j in range(0,4):
        for k in range(0, 4):
            f.writelines(str(round(extrinsic_mat_list[i][j][k],10))+" ")
        f.writelines('\n')

f.close()


