#读取深度图片
import cv2
import numpy as np

# 读取深度图像
depth_image = cv2.imread('C:/Users/A/Desktop/2.png', cv2.IMREAD_UNCHANGED)  # 使用IMREAD_UNCHANGED以确保图像是以16位深度读取

#确认通道值
print(depth_image.shape)


if depth_image is None:
    print("图像读取失败，请检查路径或文件格式")
else:
    print("图像读取成功")

# 转换为灰度图像
depth_image = cv2.cvtColor(depth_image, cv2.COLOR_BGR2GRAY)
print("转换为单通道深度图像。")

#获取指定像素的深度值
# 假设我们想获取图像中心点的深度值
height, width = depth_image.shape
center_x, center_y = width // 2, height // 2

# 获取中心点的深度值
depth_value = depth_image[center_y, center_x]
print(f"中心点的深度值为: {depth_value} (单位可能是毫米或其他，取决于保存时的单位)")


