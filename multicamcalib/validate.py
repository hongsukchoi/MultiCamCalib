import os.path as osp
import glob
import json
import open3d as o3d
import cv2
import numpy as np
from collections import defaultdict


if __name__ == '__main__':
    data_dir = "../data/handnerf_09282023/validation_depth"
    calibration_path = "../data/handnerf_09282023/output/cam_params/cam_params_final.json"

    # read calibration data
    with open(calibration_path, 'r') as f:
        calibratoin_data = json.load(f)

    # read images
    rgb_paths = defaultdict(list)
    depth_paths = defaultdict(list)
    start_cam, end_cam = 1, 6
    num_data = 1

    for cam_idx in range(start_cam,end_cam+1):
        rgb_paths[cam_idx] = sorted(
            glob.glob(osp.join(data_dir, f'cam_{cam_idx}', '*.jpg'))
        ) # for rgb
        depth_paths[cam_idx ] = sorted(
            glob.glob(osp.join(data_dir, f'cam_{cam_idx}', '*.png'))
        )  # for depth


    for data_idx in range(num_data):
        print("Scene ", data_idx)
        
        pointcloud_list = []
        for cam_idx in [1,2,3,4,5, 6]:
            print("Cam idx: ", cam_idx)
            # make open3d RGBD image
            rgb_path = rgb_paths[cam_idx][data_idx]
            depth_path = depth_paths[cam_idx][data_idx]
            print(rgb_path, depth_path)
            color_raw = o3d.io.read_image(rgb_path)
            depth_raw = o3d.io.read_image(depth_path)
            rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw,
                                    depth_scale=1000.0, depth_trunc=3.0, convert_rgb_to_intensity=False)

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

            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,  intrinsics, extrinsics)
            pointcloud_list.append(pcd)

        o3d.visualization.draw_geometries(pointcloud_list)

