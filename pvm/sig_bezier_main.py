import cv2
import numpy as np
import os
from tqdm import trange

def extract_vessel_skeleton(mask_image):
    median_filtered = cv2.medianBlur(mask_image, 5)

    skel = np.zeros_like(median_filtered)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False
    while not done:
        eroded = cv2.erode(median_filtered, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(median_filtered, temp)
        skel = cv2.bitwise_or(skel, temp)
        median_filtered = eroded.copy()
        zeros = len(np.unique(median_filtered))
        if zeros == 1:
            done = True

    return skel

def generate_adaptive_bezier_curve_mask(skeleton_image, curve_length):
    print(type(skeleton_image))
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
    # output_folder = '/home/****/Desktop/projects/medical/RPCA-UNet-master/Data_test/rawData_test/vessel_bezier'

    input_folder = '/home/****/Desktop/projects/medical/SAVDA_mm24/datasets/ssv/base_test/testA'
    output_folder = '/home/****/Desktop/projects/medical/SAVDA_mm24/datasets/ssv/base_test/testA_bezier3'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):

        if filename.endswith('.png'):
            print("-------processing file-----------:", filename)
            vessel_mask = cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_GRAYSCALE)
            vessel_skeleton = extract_vessel_skeleton(vessel_mask)
            adaptive_bezier_curve_mask = generate_adaptive_bezier_curve_mask(vessel_skeleton, curve_length=3)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, adaptive_bezier_curve_mask)

    print("--------------done-----------------")
