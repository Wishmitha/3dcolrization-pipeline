import cv2
import os
import numpy as np
import numpngw
import re

def load_pfm(file):
    color = None
    width = None
    height = None
    scale = None
    data_type = None
    header = file.readline().decode('UTF-8').rstrip()

    if header == 'PF':
        color = True
    elif header == 'Pf':
        color = False
    else:
        raise Exception('Not a PFM file.')
    dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline().decode('UTF-8'))
    if dim_match:
        width, height = map(int, dim_match.groups())
    else:
        raise Exception('Malformed PFM header.')
    # scale = float(file.readline().rstrip())
    scale = float((file.readline()).decode('UTF-8').rstrip())
    if scale < 0: # little-endian
        data_type = '<f'
    else:
        data_type = '>f' # big-endian
    data_string = file.read()
    data = np.fromstring(data_string, data_type)
    shape = (height, width, 3) if color else (height, width)
    data = np.reshape(data, shape)
    data = cv2.flip(data, 0)
    return data

import argparse

# parser = argparse.ArgumentParser(description='convert .pfm to .png')
#
# parser.add_argument('--root dir', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
#
# parser.add_argument('--root_dir', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
#
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

rootdir = '/home/wolfpack/Dev/Projects/3dcolrization-pipeline/Data/BlendedMVS/building_1/rendered_depth_maps'
extensions = ('.pfm')

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            #if file.split('_')[-1].split('.')[0] == type:
                img = load_pfm(open(os.path.join(subdir, file),'rb')) #pfm file path goes here
                img = (65535*((img - img.min())/img.ptp())).astype(np.uint16)
                print(img)
                res = cv2.resize(img, dsize=(2048, 1536), interpolation=cv2.INTER_CUBIC)


                dir = subdir+"/"+"16bit_depths"
                if not os.path.exists(dir):
                    os.makedirs(dir)

                numpngw.write_png(os.path.join(dir, file).split('.')[0]+'.png', res)
                #scipy.misc.imsave(os.path.join(dir, file).split('.')[0]+'.png', res)  # output png file path goes here