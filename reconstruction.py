import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator
from skimage import measure
import pyvista as pv
import matplotlib.pyplot as plt
from scipy.ndimage import binary_dilation

#Load annotation file in COCO format which includes segmentation data
with open('images/mysz_3_axial/_annotations.coco.json', 'r') as file:
    data = json.load(file)
  
#Helper functions to get with, height and id of images  
def get_img(id):
    return next((item for item in data["images"] if item["id"] == id), None)

def get_img_id(id):
    image_id= get_img(id)
    return image_id["id"]

def get_img_height(id):
    img_height = get_img(id)
    return img_height["height"]

def get_img_width(id):
    img_width = get_img(id)
    return img_width["width"]

#Function which creates empty binary mask (filled with 0) with image dimentions
def mask_filled_with_0(id):
    height = get_img_height(id)
    width = get_img_width(id)
    mask = np.zeros((height,width), dtype=np.uint8)
    return mask

#Function which gets all the annotations for particular image (id)
def get_annotations_for_img_id (id):
    return [annotation for annotation in data["annotations"] if annotation["id"] == id]

#Function which extract segmentation points for particular image (id)
def get_img_segmentations(id):
    annotations = get_annotations_for_img_id(id)
    segmentations = []
    
    for value in annotations:
        segmentations.append(value["segmentation"][0])
    return segmentations

#Function which creates binary mask depending on segmentation points (1-object, 0-background)
def binary_mask(id):
    mask = mask_filled_with_0(id)
    segmentations = get_img_segmentations(id)
    
    for value in segmentations:
        contur = np.array(value).reshape(-1,2).astype(np.int32)
        cv2.fillPoly(mask, [contur], color=1)
        
    return mask

#Function which extract slice number from the image name
def number_of_slice(name):
    return int(name[-7:-4])

#Sort images based on slice number
all_ids=[item["id"] for item in data["images"]]
sorted_img = sorted(
    all_ids,
        key=lambda id: number_of_slice(get_img(id)["extra"]["name"])
) 

#Stack all images into one 3d volume
masks_stack=[binary_mask(slice) for slice in sorted_img]
volume_3d = np.stack(masks_stack, axis=0).astype(float)
print(volume_3d.shape)

#Linear interpolation

# Original voxel dimensions
pixelsize_old_x = 0.0274815
pixelsize_old_y =  0.0274815
slice_thickness_old = 0.1016

pixelsize_new_x = 0.0274815
pixelsize_new_y= 0.0274815
slice_thickness_new = slice_thickness_old/4 #increase slices in Z-axis 4 times

x_old = np.linspace(0,(volume_3d.shape[1]-1)*pixelsize_old_x, volume_3d.shape[1])
y_old = np.linspace(0,(volume_3d.shape[2]-1)*pixelsize_old_y, volume_3d.shape[2])
z_old = np.linspace(0, (volume_3d.shape[0])*slice_thickness_old, volume_3d.shape[0])

method = "linear"
interpolating_function = RegularGridInterpolator((z_old,x_old, y_old), volume_3d, method=method, bounds_error=False)

#Shape of new interpolated grid
x_new = np.round(volume_3d.shape[1]*pixelsize_old_x/pixelsize_new_x).astype(np.int32)
y_new = np.round(volume_3d.shape[2]*pixelsize_old_y/pixelsize_new_y).astype(np.int32)
z_new = np.arange(0, z_old[-1], slice_thickness_new)

#3D grid points for interpolation
pts = np.indices((len(z_new), x_new, y_new)).transpose((1, 2, 3, 0))
pts = pts.reshape(1, len(z_new)*x_new*y_new, 1, 3).reshape(len(z_new)*x_new*y_new, 3)
pts = np.array(pts, dtype=float)
pts[:, 1] = pts[:, 1] * pixelsize_new_x        # X-axis
pts[:, 2] = pts[:, 2] * pixelsize_new_y        # Y-axis
pts[:, 0] = pts[:, 0] *slice_thickness_new

#Interpolate in batches
batch_size = 500000 
results = []
for i in range(0, len(pts), batch_size):
    batch = pts[i:i+batch_size]
    result = interpolating_function(batch)
    results.append(result)

#Concate interpolated values into 3D volume
interpolated_data = np.concatenate(results)
interpolated_data = interpolated_data.reshape(len(z_new), x_new, y_new)

#Convert interpolated data to binary
interpolated_data_binary = (interpolated_data > 0.1).astype(np.uint8)

#3D mask expansion voxels on edges
interpolated_data_eadges = binary_dilation(interpolated_data_binary, structure=np.ones((3, 3, 3))).astype(np.uint8)

#Repeat several times
for _ in range(8): 
    interpolated_data_eadges = binary_dilation(interpolated_data_eadges, structure=np.ones((3,3,3)))

#3D mesh reconstruction with marching cubes
vertices, faces, normals, values = measure.marching_cubes(interpolated_data_eadges, 0.01, spacing=(slice_thickness_new, pixelsize_new_x, pixelsize_new_y))

#Convert into PyVista format
faces_pv = np.hstack([[3, *face] for face in faces])
surf = pv.PolyData(vertices, faces_pv)

#Fill holes in the mesh surface
size=500
surf_filled = surf.fill_holes(hole_size=size)

#Visualise the mesh
plotter = pv.Plotter()
plotter.add_mesh(surf_filled, color="lightgray", opacity=0.7, show_edges=True)
plotter.add_blurring()
plotter.add_axes()
plotter.show()

#Calculate volume based on voxels number
voxel_volume = pixelsize_new_x * pixelsize_new_y * slice_thickness_new
voxels_number = np.count_nonzero(interpolated_data_eadges)
volume_mm3 = voxels_number * voxel_volume
print("Volume:", round(volume_mm3, 2), "mm³")