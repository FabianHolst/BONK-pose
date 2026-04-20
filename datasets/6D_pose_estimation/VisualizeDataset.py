import os
import numpy as np
import json
import cv2
import matplotlib.pyplot as plt
from typing import Dict
from PIL import Image
import matplotlib.patches as patches


# !!! Set dataset path to where you've unzipped the dataset.
pathOf6Ddataset = '.'
labels_path = os.path.join(pathOf6Ddataset, "label")
calib_path = os.path.join(pathOf6Ddataset, "calib")
image_path = os.path.join(pathOf6Ddataset, "image")


def load_camera_intrinsics(calib_file: str) -> np.ndarray:
    return np.loadtxt(calib_file)

def project_point_to_image(point_3d: np.ndarray, camera_matrix: np.ndarray) -> np.ndarray:
    image_point = np.matmul(camera_matrix, point_3d)
    point_2d = image_point[:2] / image_point[2]
    return point_2d

def project_points_to_image(points_3d: np.ndarray, camera_matrix: np.ndarray) -> np.ndarray:
    points_2d = []
    for point in points_3d:
        points_2d.append(project_point_to_image(point,camera_matrix))
    return np.array(points_2d)

def visualize_annotations(image_file: str, annotations: Dict, camera_matrix: np.ndarray):    
    # setup
    image = Image.open(image_file) 
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8,5), dpi=256)
    plt.tight_layout()
    axes.imshow(image)
    axes.axis('off')
    
    if len(annotations["objects"]) == 0:
        return
    
    #3D bounding boxes
    for object6d in annotations["objects"]:
        position = object6d["position"]
        rotationMatrix=cv2.Rodrigues(np.array(object6d["position"]["eulerAngles"]))[0]
        forward, port, up = rotationMatrix[:,0], rotationMatrix[:,1], rotationMatrix[:,2]
        centroid = position["centroid"]
        w, h, l = object6d["width"] / 2, object6d["height"] / 2, object6d["length"] / 2

        # center
        centroidInImage = project_point_to_image(centroid,camera_matrix)
        axes.scatter(*centroidInImage,s=10)     

        # 3D bounding box corners and edges
        corners3D = np.array([
            centroid-forward*l-port*w-up*h,
            centroid+forward*l-port*w-up*h,
            centroid+forward*l+port*w-up*h,
            centroid-forward*l+port*w-up*h,
            centroid-forward*l-port*w+up*h,
            centroid+forward*l-port*w+up*h,
            centroid+forward*l+port*w+up*h,
            centroid-forward*l+port*w+up*h,
        ])        
        bbCornersInImage = project_points_to_image(corners3D,camera_matrix)
        
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom square
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top square
            (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical edges
        ]
        for start, end in edges:
            x_values = [bbCornersInImage[start][0], bbCornersInImage[end][0]]
            y_values = [bbCornersInImage[start][1], bbCornersInImage[end][1]]
            axes.plot(x_values, y_values,linestyle='dotted', color='blue', alpha=0.8, linewidth=1)
            
        # Object coordinate system
        rightHandedObjCoordSystemEndPoints = np.array([
            centroid+forward*l,
            centroid+port*w,
            centroid+up*h
        ])
        coordinateSystemEnpointsInImageSpace = project_points_to_image(rightHandedObjCoordSystemEndPoints,camera_matrix)

        x_points = coordinateSystemEnpointsInImageSpace[:,0]  
        y_points = coordinateSystemEnpointsInImageSpace[:,1]
        x_center, y_center = centroidInImage 
        axes.scatter(x_points,y_points,s=10)
        
        for x, y in zip(x_points, y_points):
            axes.arrow(x_center, y_center, x - x_center, y - y_center, 
             head_width=0.2, head_length=0.2, fc='black', ec='black')
            
    #2D bounding boxes
    if annotations["2d_annotation_gt"]:
        for twoDObject in annotations["2d_annotation_gt"]:
            gt_bbox = twoDObject["bbox"]
            gt_label=str(twoDObject["category_id"])
            edgecolor='red'

            x_min, y_min, w, h = gt_bbox
            gt_bbox_converted = [x_min, y_min, x_min + w, y_min + h]
            x_min, y_min, x_max, y_max = gt_bbox_converted
            rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=2, edgecolor=edgecolor, facecolor='none')
            axes.add_patch(rect)
            axes.text(x_min, y_max-24, gt_label, color=edgecolor, fontsize='8', verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5, edgecolor=edgecolor,pad=1))
            
    plt.show()
    plt.close(fig) 

# Load and visualize data
for filename in os.listdir(labels_path)[:5]:  # Limit to 5 files for example
    if filename.endswith(".json"):
        print(filename)
        label_file = os.path.join(labels_path, filename)
        
        with open(label_file, "r") as file:
            annotations = json.load(file)
        
        base_name = os.path.splitext(filename)[0]
        calib_file = os.path.join(calib_path, f"{base_name}.txt")
        image_file = os.path.join(image_path, f"{base_name}.jpg")
        
        camera_matrix = load_camera_intrinsics(calib_file)
        
        visualize_annotations(image_file, annotations, camera_matrix)