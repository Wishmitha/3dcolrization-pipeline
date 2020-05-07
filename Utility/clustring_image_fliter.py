'''Generate key.log camera pose matrix file for give a set of clustered images
from the trajectory.log file of the original dataset.
Also filter out the relevant depth images from the original dataset for the
clustered set of images.'''

import open3d as o3d
import os, sys
sys.path.append("Utility")

from file import *

#origin_path = os.path.realpath("Data/fountain/fountain_small") #path orignal set of images
clustered_path = os.path.realpath("Data/fountain/fountain_small") #path for clustered images

depth_image_path = get_file_list(os.path.join(path, "depth/"),
                                     extension=".png")
color_image_path = get_file_list(os.path.join(path, "image/"),
                                     extension=".jpg")

origin = o3d.io.read_image(os.path.join(origin_path))
clutered = o3d.io.read_image(os.path.join(clustered_path))


def generate_key_log():
    pass

def filter_depth_images():
    pass


