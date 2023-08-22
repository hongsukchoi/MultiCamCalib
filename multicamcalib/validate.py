import os.path as osp
import glob
import json
import open3d as o3d
import cv2
import numpy as np
from collections import defaultdict
from PIL import Image



if __name__ == '__main__':
    data_dir = "../data/handnerf_0818/validation"
    calibration_path = "../data/handnerf_0818/output/cam_params/cam_params_final.json"

    # read calibration data
    with open(calibration_path, 'r') as f:
        calibratoin_data = json.load(f)

    # read images
    rgb_paths = defaultdict(list)
    depth_paths = defaultdict(list)
    start_cam, end_cam = 1, 5
    num_data = 1

    for cam_idx in range(start_cam,end_cam+1):
        rgb_paths[cam_idx] = sorted(
            glob.glob(osp.join(data_dir, f'cam_{cam_idx}', '*.jpg'))
        ) # for rgb
        depth_paths[cam_idx ] = sorted(
            glob.glob(osp.join(data_dir, f'cam_{cam_idx}', '*.png'))
        )  # for depth



    # cam_pairs = []
    # for i in range(start_cam, end_cam+1):
    #     for j in range(i+1, end_cam+1):
    #         # if i in [0,2] or j in [0,2]:
    #         #     continue
    #         cam_pairs.append((i,j))

    for data_idx in range(num_data):
        print("Scene ", data_idx)
        

        # for pair in cam_pairs:
        #     print("Pair ", pair)
       
        pointcloud_list = []
        for cam_idx in [1,2,3,4,5]:
            print("Cam idx: ", cam_idx)
            # make open3d RGBD image
            rgb_path = rgb_paths[cam_idx][data_idx]
            depth_path = depth_paths[cam_idx][data_idx]
            print(rgb_path, depth_path)
            color_raw = o3d.io.read_image(rgb_path)
            depth_raw = o3d.io.read_image(depth_path)
            rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)
            # depth_image = np.asarray(Image.open(depth_path)).astype(np.uint16)
            # o3d_depth = o3d.geometry.Image(depth_image)

            # prepare intrinsics and extrinsics for open3d
            calib = calibratoin_data[str(cam_idx)]
            # intrinsics
            intrinsics = o3d.camera.PinholeCameraIntrinsic()
            width, height = 1280, 720
            if cam_idx == 0:
                import pdb; pdb.set_trace()
            intrinsics.set_intrinsics(width, height, calib['fx'], calib['fy'], calib['cx'], calib['cy'])

            # extrinsics
            rvec, tvec = calib['rvec'], calib['tvec'] # (3,) (3,)
            R, _ = cv2.Rodrigues(np.float32(rvec))
            t = np.float32(tvec).reshape(3, 1) / 1000.
            extrinsics = np.eye(4)
            extrinsics[:3, :3] = R
            extrinsics[:3, 3:] = t

            color = np.asarray(Image.open(rgb_path)).astype('float').reshape(-1, 3) 
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,   intrinsics, extrinsics)
            # pcd_new = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.asarray(pcd.points)))
            # pcd_new.colors = o3d.utility.Vector3dVector(color)
            # pcd = o3d.geometry.PointCloud.create_from_depth_image(
            #     o3d_depth, intrinsic=intrinsics, extrinsic=extrinsics, depth_scale=1000.0, depth_trunc=2.5)
            # pcd.colors = o3d.utility.Vector3dVector(np.asarray(color_raw).astype(float).reshape(-1,3) / 255)
            # pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
            pointcloud_list.append(pcd)
        o3d.visualization.draw_geometries(pointcloud_list)

        # import pdb
        # pdb.set_trace()
