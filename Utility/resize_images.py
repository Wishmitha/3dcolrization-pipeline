'''
Script used to resize all images in a folder with same new resolution (resize_width x resize_height)
By Yingshu CHEN

command example:
python resize_images.py --input_dir ./images --output_dir ./ -rw 1536 -rh 1024
python resize_images.py ./ -rw 1536 -rh 1024
## All images in folder './images' will be resized and saved in new folder './images_1536x1024'

python resize_images.py --input_dir ./person-hall/images --output_dir ./person-hall -rw 1536 -rh 1024 -type JPG
## All '*.JPG' images in folder './person-hall/images' will be resized and saved in new folder './person-hall/images_1536x1024'
## Not change file channels
## Not change the files name or file type

'''
import cv2
import glob
import argparse
import os


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_dir", default='./images', help="path to folder containing images to be resized") 
	parser.add_argument("--output_dir", default='./', help="where to put output resized files") 
	parser.add_argument("--resize_width", '-rw', type=int, required=True, help="width of resized image") 
	parser.add_argument("--resize_height", '-rh', type=int, required=True, help="height of resized image")
	parser.add_argument("--image_type", '-type', default='all', help="image type to be resized, default support all types including jpg/JPG, jpge/JPGE, png/PNG" )
	a = parser.parse_args()

	width = a.resize_width
	height = a.resize_height
    ############### Open image files ####################
	if a.input_dir is None or not os.path.exists(a.input_dir):
		raise Exception("input_dir does not exist")

	input_paths = []
	if a.image_type == 'all':
		input_paths = glob.glob(os.path.join(a.input_dir, "*.jpg"))
		input_paths = input_paths + glob.glob(os.path.join(a.input_dir, "*.JPG"))
		input_paths = input_paths + glob.glob(os.path.join(a.input_dir, "*.jpge"))
		input_paths = input_paths + glob.glob(os.path.join(a.input_dir, "*.JPGE"))
		input_paths = input_paths + glob.glob(os.path.join(a.input_dir, "*.png"))
		input_paths = input_paths + glob.glob(os.path.join(a.input_dir, "*.PNG"))
	else:
		input_paths = glob.glob(os.path.join(a.input_dir, "*"+a.image_type))

	if len(input_paths) == 0:
		raise Exception("input_dir contains no image files")
	else:
		print('{} images will be resized with new resolution {}x{}.'.format(len(input_paths), width, height))
	image_dir = os.path.join(a.output_dir, "images_{}x{}".format(width, height))
	os.makedirs(image_dir, exist_ok=True)

	########### Resize images ##############

	for path in input_paths:
		image = cv2.imread(path)
		resized = cv2.resize(image, (width, height))
		name, postfix = os.path.splitext(os.path.basename(path))
		print('Resizing '+name+postfix)
		cv2.imwrite(os.path.join(image_dir, name+postfix), resized)

	print('DONE.')
