import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import cv2


#保存为.txt文件
def save_depth_txt(file_path):
    # 配置深度流
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    # 开启流
    pipeline.start(config)
    
    # 得到深度传感器实例
    profile = pipeline.get_active_profile()
    depth_sensor = profile.get_device().first_depth_sensor()
    
    # 设置深度传感器参数
    depth_scale = depth_sensor.get_depth_scale()
    clipping_distance = 1.0
    
    # 创建一个numpy数组来存储深度图像数据
    depth_image = np.zeros((480, 640), dtype=np.float32)
    
    try:
        # 循环采集深度图像
        while True:
            # 等待下一帧
            frames = pipeline.wait_for_frames()
            
            # 取得深度帧
            depth_frame = frames.get_depth_frame()
            
            # 将深度帧转换为numpy数组
            depth_data = np.asarray(depth_frame.get_data(), dtype=np.uint16)
            
            # 将深度数据进行单位转换和裁剪
            depth_image = depth_data * depth_scale
            depth_image[depth_image > clipping_distance] = 0
            
            # 保存深度图像为.txt文件
            np.savetxt(file_path, depth_image, fmt='%.4f', delimiter='\t')
            
            # 按下'q'键退出循环
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
    
    finally:
        # 关闭流和窗口
        pipeline.stop()


#保存为点云数据.pcd
def save_depth_pcd(file_path):
    # 配置深度流
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    # 开启流
    pipeline.start(config)
    
    # 得到深度传感器实例
    profile = pipeline.get_active_profile()
    depth_sensor = profile.get_device().first_depth_sensor()
    
    # 设置深度传感器参数
    depth_scale = depth_sensor.get_depth_scale()
    clipping_distance = 1.0
    
    # 创建一个PointCloud对象
    pcd = o3d.geometry.PointCloud()
    
    try:
        # 循环采集深度图像
        while True:
            # 等待下一帧
            frames = pipeline.wait_for_frames()
            
            # 取得深度帧
            depth_frame = frames.get_depth_frame()
            
            # 将深度帧转换为numpy数组
            depth_data = np.asarray(depth_frame.get_data(), dtype=np.uint16)
            
            # 将深度数据进行单位转换和裁剪
            depth_image = depth_data * depth_scale
            depth_image[depth_image > clipping_distance] = 0
            
            # 将深度图像转换为点云
            points = rs.pointcloud.calculate(depth_frame)
            vertices = np.asarray(points.get_vertices(), dtype=np.float32)
            pcd.points = o3d.utility.Vector3dVector(vertices)
            
            # 保存点云为.pcd文件
            o3d.io.write_point_cloud(file_path, pcd)
            
            # 按下'q'键退出循环
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
    
    finally:
        # 关闭流和窗口
        pipeline.stop()



# 保存为.txt文件
save_depth_txt('depth_image.txt')

# 保存为.pcd文件
save_depth_pcd('depth_cloud.pcd')



