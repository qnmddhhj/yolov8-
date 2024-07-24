import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import cv2

# 从Bag文件中读取数据并保存深度数据为.txt和.pcd文件
def process_depth_data_from_bag(bag_file_path, txt_file_path, pcd_file_path):
    # 设置pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    
    # 指定从Bag文件加载数据
    rs.config.enable_device_from_file(config, bag_file_path)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    # 启动pipeline
    pipeline.start(config)
    
    try:
        # 读取一帧数据
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        
        if not depth_frame:
            raise RuntimeError("No depth frame available.")
        
        # 深度帧处理
        depth_scale = pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        clipping_distance = 1.0 / depth_scale
        
        depth_data = np.asanyarray(depth_frame.get_data())
        depth_image = depth_data * depth_scale
        depth_image[depth_image > clipping_distance] = 0
        
        # 保存深度数据为txt文件
        np.savetxt(txt_file_path, depth_image, fmt='%.4f', delimiter='\t')
        print(f"Saved depth data to {txt_file_path}")
        
        # 转换为点云并保存为PCD文件
        pc = rs.pointcloud()
        points = pc.calculate(depth_frame)
        vtx = np.asanyarray(points.get_vertices())
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(vtx.view('float32').reshape(-1, 3))
        
        o3d.io.write_point_cloud(pcd_file_path, pcd)
        print(f"Saved point cloud to {pcd_file_path}")

    finally:
        pipeline.stop()

# 路径配置
bag_file_path = r'C:/Users/A/Documents/20240715_102449.bag'
txt_file_path = r'C:/Users/A/深度数据'
pcd_file_path = r'C:/Users/A/深度数据'

# 处理函数调用
process_depth_data_from_bag(bag_file_path, txt_file_path, pcd_file_path)
