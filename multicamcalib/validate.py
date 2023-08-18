import os.path as osp
import glob
import json
import open3d as o3d
import cv2
import numpy as np
from collections import defaultdict

mapper = {
    0: 0,
    3: 1,
    4: 2,
    1: 3,
    6: 4,
    2: 5,
    5: 6
}



if __name__ == '__main__':
    data_dir = "../data/validation"
    calibration_path = "../data/handnerf_intrinsics/output/cam_params/cam_params_final.json"

    # read calibration data
    with open(calibration_path, 'r') as f:
        calibratoin_data = json.load(f)

    # read images
    rgb_paths = defaultdict(list)
    depth_paths = defaultdict(list)
    num_cams = 6
    num_data = 1

    for cam_idx in range(0,num_cams):
        rgb_paths[cam_idx] = sorted(
            glob.glob(osp.join(data_dir, f'cam_{cam_idx}', '*.jpg'))
        ) # for rgb
        depth_paths[cam_idx ] = sorted(
            glob.glob(osp.join(data_dir, f'cam_{cam_idx}', '*.png'))
        )  # for depth



    cam_pairs = []
    for i in range(0, num_cams):
        for j in range(i+1, num_cams):
            # if i in [0,2] or j in [0,2]:
            #     continue
            cam_pairs.append((i,j))

    for data_idx in range(num_data):
        print("Scene ", data_idx)
        

        for pair in cam_pairs:
            print("Pair ", pair)
            pointcloud_list = []
            for cam_idx in pair:
                # make open3d RGBD image
                rgb_path = rgb_paths[cam_idx][data_idx]
                depth_path = depth_paths[cam_idx][data_idx]

                color_raw = o3d.io.read_image(rgb_path)
                depth_raw = o3d.io.read_image(depth_path)
                rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)

                # prepare intrinsics and extrinsics for open3d
                calib = calibratoin_data[str(cam_idx)]
                # intrinsics
                intrinsics = o3d.camera.PinholeCameraIntrinsic()
                width, height = 1280, 720
                if cam_idx in [0,2]:
                    x_scale = 640 / 1280
                    y_scale = 480 / 720 

                    intrinsics.set_intrinsics(
                        int(width * x_scale), int(height * y_scale),
                          calib['fx'] * x_scale, calib['fy'] * y_scale, calib['cx'] * x_scale, calib['cy'] * y_scale)
                else:
                    intrinsics.set_intrinsics(width, height, calib['fx'], calib['fy'], calib['cx'], calib['cy'])

                # extrinsics
                rvec, tvec = calib['rvec'], calib['tvec'] # (3,) (3,)
                R, _ = cv2.Rodrigues(np.float32(rvec))
                t = np.float32(tvec).reshape(3, 1) / 1000.
                extrinsics = np.eye(4)
                extrinsics[:3, :3] = R
                extrinsics[:3, 3:] = t

                pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,
                                                                    intrinsics,
                                                                    extrinsics)
                # pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
                pointcloud_list.append(pcd)

            o3d.visualization.draw_geometries(pointcloud_list)
        # import pdb
        # pdb.set_trace()
