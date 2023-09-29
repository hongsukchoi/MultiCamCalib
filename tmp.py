import os
import os.path as osp
import shutil
import glob


if __name__ == '__main__':
    src_dir = osp.abspath('/home/hongsuk.c/Downloads/handnerf_calibration_part_2')
    dst_dir = osp.abspath(
        '/home/hongsuk.c/Projects/MultiCamCalib/data/handnerf_09282023/images')
    src_cam_dir_list = sorted(glob.glob(src_dir + '/*'))
    for scd in src_cam_dir_list:
        img_paths = sorted(glob.glob(scd + '/*'))
        for img_path in img_paths:
            file_name = osp.basename(img_path)
            new_file_name = file_name.split('_')[0] + '_' +  f"{28 + int(file_name.split('_')[1][:-4]):04d}" + '.jpg'
            
            new_img_path = osp.join(dst_dir,  osp.basename(osp.dirname(img_path)), new_file_name)
            shutil.copy(img_path, new_img_path)