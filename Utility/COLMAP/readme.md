## depth\_bin\_to\_png.py ##
This script transfers binary depth maps to png images.

Example command:

    python depth_bin_to_png.py -d ./dep_geometric_map -o ./dep_geometric_img --min_depth_percentile 5 --max_depth_percentile 95

Folder of depth binary maps (e.g. folder dep_geometric_map) should contain *bin* files generated from COLMAP **dense reconstruction**.

We use geometric binary files in 
`dense > stereo > depth_maps > image.jpg.geometric.bin` .

Reference: [https://colmap.github.io/format.html#depth-and-normal-maps](https://colmap.github.io/format.html#depth-and-normal-maps)
 