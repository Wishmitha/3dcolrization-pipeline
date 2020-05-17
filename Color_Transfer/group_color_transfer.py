'''
Color style transfer for a folder of images

Reference:
Color Transfer between Images by Reinhard et al, 2001. [https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf]
https://github.com/jrosebr1/color_transfer

## Command USAGE:
## python group_color_transfer.py --input_dir inputs/folder_containing_images --style_image style/style_image.jpg --output_dir results/image_style_folder_name
# e.g., python group_color_transfer.py --input_dir inputs/fountain_all --style_image style/fountain/night2.jpg --output_dir results/fountain_all_night2

'''


# import the necessary packages
from color_transfer import color_transfer
import numpy as np
import argparse
import cv2
import os
import glob

def get_name(path):
    name, _ = os.path.splitext(os.path.basename(path))
    return name

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':

	# construct the argument parser and parse the arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--style_image", required = True, help = "Path to style image")
	parser.add_argument("-i", "--input_dir", required = True, help = "Path to input folder containing target images")
	parser.add_argument("-o", "--output_dir", required = True, default="results", help = "Path to output folder saving results")
	parser.add_argument("-c", "--clip", type = str2bool, default = 't',
		help = "Should np.clip scale L*a*b* values before final conversion to BGR? "
			   "Approptiate min-max scaling used if False.")
	parser.add_argument("-p", "--preservePaper", type = str2bool, default = 't',
		help = "Should color transfer strictly follow methodology layed out in original paper?")
	args = parser.parse_args()
	
	# get color style image
	try:
		style_image = cv2.imread(args.style_image)
	except:
		raise Exception("style image does not exist")

	# get paths of all target images 
	input_dir = args.input_dir
	output_dir = args.output_dir
	if not os.path.exists(input_dir):
		raise Exception("input_dir does not exist")

	if not os.path.exists(output_dir):
		try: # Create target Directory
			os.mkdir(output_dir)
			print("Directory " , output_dir ,  " Created ") 
		except FileExistsError:
			print("Directory " , output_dir ,  " already exists")


	input_paths = glob.glob(os.path.join(input_dir, "*.png"))
	if len(input_paths) == 0:
		input_paths = glob.glob(os.path.join(input_dir, "*.jpg"))
	if len(input_paths) == 0:
		raise Exception("input_dir contains no image files")
	
	# handle all images
	for img_path in input_paths:
		# load the image
		target_image = cv2.imread(img_path)
		transfer_image = color_transfer(style_image, target_image, clip=args.clip, preserve_paper=args.preservePaper)
		cv2.imwrite(os.path.join(output_dir, get_name(img_path) + ".png"), transfer_image)

