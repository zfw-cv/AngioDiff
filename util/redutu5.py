import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def read_and_generate_heatmap(folder1, folder2, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Get image filenames from both folders
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)
    
    # Create a map to match image filenames in folder2
    files2_map = {file_name.split('_rec_B.png')[0]: file_name for file_name in files2 if file_name.endswith('_rec_B.png')}
    
    for file_name1 in files1:
        # Remove file extension to facilitate matching
        base_name = os.path.splitext(file_name1)[0]
        if base_name in files2_map:
            # Read matching files
            file_name2 = files2_map[base_name]
            img_path1 = os.path.join(folder1, file_name1)
            img_path2 = os.path.join(folder2, file_name2)
            
            image1 = Image.open(img_path1).convert('L')
            image2 = Image.open(img_path2).convert('L')
            
            # Convert images to arrays of gray values
            data1 = np.array(image1, dtype=float)
            data2 = np.array(image2, dtype=float)
            
            # Compute the absolute difference between the two images
            data_diff = np.abs(data2 - data1)
            
            # Create a heatmap
            plt.figure()
            heatmap = plt.imshow(data_diff, cmap='jet', interpolation='nearest', vmin=0, vmax=40)
            plt.colorbar(heatmap)
            plt.title('')
            
            # Save the heatmap
            output_path = os.path.join(output_folder, 'change_heatmap_' + base_name + '.png')
            plt.savefig(output_path)
            plt.close()

# Example usage:
# read_and_generate_heatmap('path/to/folder1', 'path/to/folder2', 'path/to/output_folder')
path_1 = '/home/****/Desktop/projects/medical/SAVDA_mm24/datasets/ssv/testB/'
# path_1 = '/home/****/Desktop/projects/medical/SAVDA_mm24/results/check_base/test_25/images/'
path_2 = '/home/****/Desktop/projects/medical/SAVDA_mm24/results/check_base/test_195/images/'
out_path = '/home/****/Desktop/projects/medical/SAVDA_mm24/results/check_base/4base_195/'


read_and_generate_heatmap(path_1,path_2,out_path)
print("--done---")