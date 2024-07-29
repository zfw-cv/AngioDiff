import os

# 文件夹列表
folder1='1base_25'
folder2='1base_50'
folder3='1base_90'
folder4='1base_100'
folder5='1base_130'
folder6='1base_160'
folder7='1base_200'


folders = [folder1,folder2,folder3,folder4,folder5,folder6,folder7]
base_dir = '/home/****/Desktop/projects/medical/SAVDA_mm24/results/check_base/'  

images = {}

for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    for file in os.listdir(folder_path):
        if file.endswith('.png'):
            if file not in images:
                images[file] = []
            images[file].append(os.path.join(folder, file))

html = """
<html>
<head>
<title>Image Gallery</title>
</head>
<body>
<h1>Image Gallery</h1>
<table border="1">
"""

for image_name, paths in images.items():
    html += "<tr>"
    html += f"<td>{image_name}</td>"
    for path in paths:
        html += f"<td><img src='{path}' alt='{image_name}' width='100'></td>"
    html += "</tr>\n"

html += """
</table>
</body>
</html>
"""

with open('gallery1.html', 'w') as file:
    file.write(html)

print("HTML file has been created.")
