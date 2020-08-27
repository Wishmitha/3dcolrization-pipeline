1. Create Anaconda environment using, "conda env create -f environment.yml"
2. Set the created Anaconda environment as the interpreter for the project
3. Set dataset path in Reconstruction -> config.json
4. Run Reconstruction -> run_system.py to perform 3D reconstruction
5. Run Texturing -> color_map_optimization.py to perform texture mapping
6. Run Utility -> clustring_image_fliter.py to generate key.log for clustered images
7. Run "python realsense_recorder.py --record_imgs" in Utility to capture data: RGBD and camera intrinsic (Note that: your need to have RealSense Python package and OpenCV Python package, use "pip install pyrealsense2" and "pip install opencv-python" to install)
8. Run Clustering -> ORB_cluster.py to do ORB clustering to select optimal number of images
9. Run Utility -> COLMAP -> depth_bin_to_png.py to transfer binary depth maps to png files
10. Speedy color style transfer in folder "Color_Transfer", see more details in "Color_Transfer".
