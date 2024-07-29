import cv2
import numpy as np
import os
import random
from tqdm import trange

def extract_vessel_skeleton(image_shape):

    vessel_skeleton = np.zeros(image_shape, dtype=np.uint8)
    num_branches = np.random.randint(3, 6)
    for _ in range(num_branches):
        start_point = (np.random.randint(50, image_shape[1] - 50), np.random.randint(50, image_shape[0] - 50))
        branch_length = np.random.randint(100, 400)
        branch_angle = np.random.uniform(0, np.pi * 2)  
        for step in range(branch_length):
            start_point = (int(start_point[0] + np.cos(branch_angle)), int(start_point[1] + np.sin(branch_angle)))
            radius = int(1 + (branch_length - step) / branch_length * 3)  
            cv2.circle(vessel_skeleton, start_point, radius, (255,), -1)
            branch_angle += np.random.uniform(-np.pi / 6, np.pi / 6)

    return vessel_skeleton


def generate_adaptive_bezier_curve_mask(skeleton_image, curve_length):

    # print(type(skeleton_image))
    skeleton_pixels = np.where(skeleton_image > 0)
    

    curve_mask = np.zeros_like(skeleton_image)
    for y, x in zip(skeleton_pixels[0], skeleton_pixels[1]):
        
        neighborhood_size = 8
        y1 = max(0, y - neighborhood_size)
        y2 = min(skeleton_image.shape[0] - 1, y + neighborhood_size)
        x1 = max(0, x - neighborhood_size)
        x2 = min(skeleton_image.shape[1] - 1, x + neighborhood_size)
        local_region = skeleton_image[y1:y2, x1:x2]
        angle = calculate_orientation(local_region)

        
        curve_points = calculate_bezier_curve_points((x, y), curve_length, angle)
        curve_points = np.int32(curve_points)
        cv2.polylines(curve_mask, [curve_points], isClosed=False, color=(255, 255, 255), thickness=2)

    return curve_mask

def calculate_orientation(region):

    sobelx = cv2.Sobel(region, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(region, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)
    gradient_angle = np.arctan2(sobely, sobelx)

    orientation = np.mean(gradient_angle)

    orientation_degrees = np.degrees(orientation)

    return orientation_degrees

def calculate_bezier_curve_points(center, length, angle):
   
    angle_rad = np.radians(angle)
    x1 = center[0] + length * np.cos(angle_rad)
    y1 = center[1] + length * np.sin(angle_rad)
    x2 = center[0] - length * np.cos(angle_rad)
    y2 = center[1] - length * np.sin(angle_rad)
    return [(center[0], center[1]), (int(x1), int(y1)), (int(x2), int(y2))]




if __name__=='__main__':
    
    # input_folder = '/home/****/Desktop/projects/medical/RPCA-UNet-master/Data_test/rawData_test/vessel'
    output_folder = '/home/****/Desktop/projects/medical/SAVDA_mm24/datasets/ssv/trainF'
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in trange(0, 1621):
        
        # Generate vessel skeleton and save as an image
        image_shape = (512,512)
        vessel_skeleton = extract_vessel_skeleton(image_shape)
        # cv2.imwrite("synthetic_vessel_skeleton.png", vessel_skeleton)
        # print("Synthetic vessel skeleton generated and saved.")

        adaptive_bezier_curve_mask = generate_adaptive_bezier_curve_mask(vessel_skeleton, curve_length=2)
        
        output_filename = 'trainA{:05d}.png'.format(i)
        output_path = os.path.join(output_folder, output_filename)
        cv2.imwrite(output_path, adaptive_bezier_curve_mask)

    print("--------------done-----------------")
