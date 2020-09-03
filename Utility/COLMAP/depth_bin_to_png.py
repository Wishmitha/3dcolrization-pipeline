'''
# This script transfer binary depth maps to png images
#
### Based on COLMAP's python script: scripts/read_dense.py
### Changes:
####    1) read folder instead of one file
####    2) save as images rather than show them
# Author: Yingshu CHEN
#
# Example command: 
#### python depth_bin_to_png.py -d ./dep_geometric_map -o ./dep_geometric_img --min_depth_percentile 5 --max_depth_percentile 95
# Binary depth maps generated from COLMAP in folder "dep_geometric_map" will be transfered in to png images in folder "dep_geometric_img"
'''

import glob
import argparse
import numpy as np
import os
import cv2
import pylab as plt


def read_array(path):
    with open(path, "rb") as fid:
        width, height, channels = np.genfromtxt(fid, delimiter="&", max_rows=1,
                                                usecols=(0, 1, 2), dtype=int)
        # print("width: {}, height: {}, channels: {}".format(width, height, channels))
        fid.seek(0)
        num_delimiter = 0
        byte = fid.read(1)
        while True:
            if byte == b"&":
                num_delimiter += 1
                if num_delimiter >= 3:
                    break
            byte = fid.read(1)
        array = np.fromfile(fid, np.float32)
    array = array.reshape((width, height, channels), order="F")
    return np.transpose(array, (1, 0, 2)).squeeze()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--depth_dir",
                        help="path to depth map", type=str, required=True)
    # parser.add_argument("-n", "--normal_map",
    #                     help="path to normal map", type=str, required=True)
    parser.add_argument("--min_depth_percentile",
                        help="minimum visualization depth percentile",
                        type=float, default=5) # [0,100]
    parser.add_argument("--max_depth_percentile",
                        help="maximum visualization depth percentile",
                        type=float, default=95) # [0,100]
    parser.add_argument("-o", "--output_dir",
                        help="path to save depth / normal images", default="./", type=str)
    args = parser.parse_args()
    return args


# Can feel free to define different naming format 
def get_name(path):
    name, _ = os.path.splitext(os.path.basename(path))
    # print("Transferring " + name)
    # return name
    return name.split('.')[0]

def transfer(depth_bin_path, min_depth_percentile, max_depth_percentile, output_dir):
    depth_map = read_array(depth_bin_path)

    min_depth, max_depth = np.percentile(
        depth_map, [min_depth_percentile, max_depth_percentile])
    depth_map[depth_map < min_depth] = min_depth
    depth_map[depth_map > max_depth] = max_depth

    # Visualize the depth map.
    # plt.figure()
    # plt.imshow(depth_map)
    # plt.title('depth map')
    # plt.show()

    # Save depth map
    cv2.imwrite(os.path.join(output_dir, get_name(depth_bin_path) + ".png"), depth_map)

def main():
    args = parse_args()

    if args.min_depth_percentile > args.max_depth_percentile:
        raise ValueError("min_depth_percentile should be less than or equal "
                         "to the max_depth_perceintile.")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    else:
        raise Exception("Output directory exists.")


    # Read depth maps
    if not os.path.exists(args.depth_dir):
        raise FileNotFoundError("Depth file not found: {}".format(args.depth_dir))

    input_paths = glob.glob(os.path.join(args.depth_dir, "*.bin"))


    for depth_bin_path in input_paths:
        transfer(depth_bin_path, args.min_depth_percentile, args.max_depth_percentile, args.output_dir)


if __name__ == "__main__":
    main()
