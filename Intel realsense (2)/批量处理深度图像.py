import cv2
import numpy as np
import os

# 确保路径是正确的，注意不要在路径字符串的末尾加上多余的引号
folder_path = r'D:\Realsense\deepth_photo'  # 使用原始字符串，并确保路径正确

try:
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    for file in files:
        file_path = os.path.join(folder_path, file)
        depth_image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

        if depth_image is None:
            print(f"图像 {file} 读取失败，请检查路径或文件格式")
        else:
            print(f"图像 {file} 读取成功")
            if len(depth_image.shape) == 3:
                depth_image = cv2.cvtColor(depth_image, cv2.COLOR_BGR2GRAY)
            height, width = depth_image.shape
            center_x, center_y = width // 2, height // 2
            depth_value = depth_image[center_y, center_x]
            print(f"图像 {file} 的中心点深度值为: {depth_value}")
except Exception as e:
    print(f"发生错误：{e}")

