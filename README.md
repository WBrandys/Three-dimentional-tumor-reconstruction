# Three-dimentional-tumor-reconstruction

This project focuses on the three-dimensional reconstruction of mice pancreatic tumors (PDAC) from 2D ultrasound images.
The aim was to calculate tumor volume based on segmented masks and compare algorithmic results with volumes obtained using physical caliper measurements and the VevoLab software.

# Files structure
- folder `images/` - Series of ultrasound image slices organized per mouse (1-5) and imaging plane (axial, menas transversal and coronal)
- folder `plots/` - R scripts used for data visualization and statistical analysis of tumor volumes
- file `reconstruction.py` - Python script for 3D tumor volume reconstruction using binary masks and Marching Cubes algorithm

# Requirements

Python (version 3.10+)
Libraries can be installed with:
```
pip install numpy matplotlib opencv-python scikit-image pyvista
```
R (version 4.4.0+)
Packages can be installed with:
```
install.packages(c("ggplot2", "dplyr", "tidyr", "readr"))
```

# Running the Reconstruction
To run the `reconstruction.py` script on a specific imaging series (axial (transverse) or coronal plane for a particular mouse), update the input path in the script. Edit the line:
```
with open('images/name_of_the_series/_annotations.coco.json', 'r') as file:
    data = json.load(file)
```
Replace `name_of_the_series` with the appropriate folder name (for egzample mysz_1_axial or mysz_1_coronal) corresponding to chosen dataset.
The script will load the annotations file, generate binary masks than perform linear interpolation and the 3D volume reconstruction using the Marching Cubes algorithm and PyVista visualization.

To perform linear interpolation I modified the script from: [https://github.com/bnsreenu/python_for_microscopists/blob/master/Tips_and_Tricks_50_interpolate_images_in_a_stack.ipynb]



