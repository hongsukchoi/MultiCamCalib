<h1>Tutorial (a step-by-step example)</h1>

You can find the original tutorial of `hjoonpark` [here](https://github.com/hjoonpark/MultiCamCalib/blob/master/docs/tutorial.md).
The tutorial below is summarized and slightly modified from the original tutorial for my (Hongsuk Choi) purpose.

> Please use the example data in hjoonpark's repository after you install the environment for now (10/04/2023).

Example data can be found [here](). __Waiting for permission.__ Download and place it as below: 

>The example data and the example `config.json`  assumes:
>- 7 synchronized RGB cameras, 
>- Camera of index 3 being the center of them (at least share more than one full view images of the chess board with every other camera),
>- 6x9 chess board (n_rows=5, n_cols=8) with the checker size of 40mm. Generated from [here](https://calib.io/pages/camera-calibration-pattern-generator).


    MultiCamCalib/
    +-- example_data
    |   +-- images
    |   +-- config.json  # for reference       
    |   +-- output  # will be re-created after completing the turorial 
    +-- ceres_bundle_adjustment # contains C/C++ codes
    +-- docs                    
    +-- multicamcalib           # contains python codes
    +-- README.md
    +-- LICENSE

Or put your custom data into whatever location you want.

<figure>
<img src="./assets/tutorial/studio.jpg" width="600px"/>
</figure>

<h2 id="s_input_data">I. Prepare input data</h2>


Modify two paths (*"abs_input_dir"* and *"abs_output_dir"*) inside *"/multicamcalib/config.json"*. (The pre-configured *config.json* file is also located at *"/example_data/"* for reference).

*config.json*:

{
    "paths": {
        "abs_input_dir": "/home/hongsuk.c/Projects/MultiCamCalib/example_data",
        "abs_output_dir": "/home/hongsuk.c/Projects/MultiCamCalib/example_data/output",
        ...
    }
...
}
Replace */home/hongsuk.c/Projects/MultiCamCalib* with your own *absolute* directory for your custom data.

This *config.json* file contains all the parameters needed by the project. Each part is explained [here](#iii-configjson), but for now you can leave everything else as it is.


***[IMPORTANT FOR OTHER DATASET]*** **Directory structure and naming convention**

The example dataset are provides in the following structure and naming convention:

    /example_data/images/
    +-- cam_0
    |   +-- 0_0000.png
    |   ...
    |   +-- 0_00xx.png
    .
    .
    .
    +-- cam_6
    |   +-- 6_0000.png
    |   ...
    |   +-- 6_00xx.png


The input image folders **MUST** be organized as the following structure:

    .
    +-- cam_0
    |   +-- {image 0}
    |   +-- ...
    .
    .
    .
    +-- cam_N
    |   +-- {image 0}
    |   +-- ...

And the image names **MUST** follow this naming convention:

    {CAMERA INDEX}_{FRAME NUMBER}.{png/jpg/pgm/etc.} // e.g., 2_000120.png for camera 2's 120-th image.

Here, the frame numbers must contain the same number of characters. The names of the example images are chosen to contain four characters (ex: 0_0000.png, 0_0001.png, ..., 0_0250.png).

These are the only constraints required in this project.

<h2 id="s_run">II. Run!</h2>

Open up a command prompt and navigate to *"/home/hongsuk.c/Projects/MultiCamCalib/multicamcalib/"* where all the python codes reside and run *multicamcalib.py* with the installed Anaconda environment.

    cd "/home/hongsuk.c/Projects/MultiCamCalib/multicamcalib"
    conda activate {YOUR_ENV_NAME}
    python multicamcalib.py

A menu explaining each of the code number will pop up:

<figure>
<img src="./assets/tutorial/prompt1.png" width="100%"/>
</figure>

As explained in [2. Overview](../readme.md#s_overview), each step in the pipeline is executed by running its corresponding *code number*, delimited by a whitespace. Inside */multicamcalib/config.json* contains all the configurations needed for the dataset, but for this example everything is already configured. So let's run through all the steps (type in *1 2 3 4 5*):

<figure>
<img src="./assets/tutorial/prompt2.png" width="100%"/>
</figure>

*Alternately,* you can skip the menu and specify the code numbers from the start by typing:

    python multicamcalib.py 1 2 3 4 5

or, (for example) if you wish to run only the corner detection part, run *1a*:

    python multicamcalib.py 1a
    
or, you can run more specificially like this:

    python multicamcalib.py 2b 2c 2d 4 5b

The codes will execute all the steps from [(1). Corner detection](../readme.md#step_1) to [(5). Analyze the calibration result](../readme.md#step_5). This takes several minutes to finish.

**Once finished, the following results are saved:**

* Initial/final camera configurations *"/home/hongsuk.c/Projects/MultiCamCalib/example_data/output/cam_params/"*:

<p style="text-align:left">
    <img src="./assets/tutorial/initial_cameras.png" width="40%"/>
    <img src="./assets/tutorial/final_cameras.png" width="40%"/>
</p>

* Initial/final camera configurations with the estimated checkerboard points *"/home/hongsuk.c/Projects/MultiCamCalib/example_data/output/world_points/"*:

<p style="text-align:left">
    <img src="./assets/tutorial/initial_world_points.png" width="40%"/>
    <img src="./assets/tutorial/final_world_points.png" width="40%"/>
</p>

* Images with large reprojection errors *"/home/hongsuk.c/Projects/MultiCamCalib/example_data/output/analysis/images/"*:
<figure style="display:inline-block; display:block;" id="fig_reprojerrors">
    <img src="./assets/tutorial/reproj_err_img.jpg" width="80%"/>
</figure>

* Reprojection error historgram *"/home/hongsuk.c/Projects/MultiCamCalib/example_data/output/analysis/"*:
<figure style="display:inline-block; display:block;" id="fig_histogram">
    <img src="./assets/tutorial/reproj_err_histograms.png" width="80%"/>
</figure>

* VAE corner detector  
  * train loss plot *"/home/hongsuk.c/Projects/MultiCamCalib/example_data/output/vae_outlier_detector/train_loss_plot.png"*:
    <figure style="display:inline-block; display:block;" id="fig_histogram">
        <img src="./assets/tutorial/train_loss_plot.png" width="60%"/>
    </figure>

  * outlier corners and their reconstructions *"/home/hongsuk.c/Projects/MultiCamCalib/example_data/output/vae_outlier_detector/outliers/"*:
    <figure style="display:inline-block; display:block;" id="fig_histogram">
        <img src="./assets/tutorial/outliers_0.png" width="60%"/>
    </figure>

**<h3>Note on step ***[4] FINAL CALIBRATION (BUNDLE ADJUSTMENT)***</h3>**
Running code number 4 executes *"/home/hongsuk.c/Projects/MultiCamCalib/ceres_bundle_adjustment/build/bin/CeresMulticamCalib"*. If you do not see this folder, that means you have not compiled *"CeresMulticamCalib"* yet. Follow [this tutorial](compile_project.md) before moving on.

<h2 id="s_config">III. config.json</h2>

This section explains the parameters defined inside *"/home/hongsuk.c/Projects/MultiCamCalib/multicamcalib/config.json"*.
Here I only explain the part that I modified for my (Hongsuk Choi) purpose. [[Original source](https://github.com/hjoonpark/MultiCamCalib/blob/master/docs/tutorial.md#iii-configjson)]. 

***paths***

    "paths": {
        "abs_input_dir": "/home/hongsuk.c/Projects/MultiCamCalib/example_data",
        "abs_output_dir": "/home/hongsuk.c/Projects/MultiCamCalib/example_data/output",
        "logs": "logs",
        "corners": "corners",
        "vae_outlier_detector": "vae_outlier_detector",
        "corner_crops": "vae_outlier_detector/corner_crops",
        "outliers": "vae_outlier_detector/outliers",
        "cam_params": "cam_params",
        "world_points": "world_points",
        "ceres_output": "bundle_adjustment",
        "analysis": "analysis"
    },

As mentioned before, *"abs_input_dir"* and *"abs_output_dir"* must be *absolute* paths. 

* *abs_input_dir*: absolute path to a data root directory.
* *abs_output_dir*: absolute directory where all the output data will be saved.
* *logs*, *corners*, ..., *analysis*: the output folder names saved to *abs_output_dir*. You don't need to change them unless different folder names are desired.

***calib_initial***

    "calib_initial": {
        "center_cam_idx": 12,
        "center_img_name": "0000",
        "intrinsics": {
            "n_max_imgs": 40
        },
        "extrinsics": {
            "n_max_stereo_imgs": 3
        }
    },

* *center_cam_idx*, *center_img_name*: Bundle adjustment results in an arbitrary coordinates system. Therefore, choose a camera and a frame in which the origin of the coordinates system should be defined. For example, *"center_cam_idx": 12, "center_img_name": "0000"* is this frame:

* In my (Hongsuk Choi) code, the center camera should share at least more than one full view images of the chess board with every other camera. The original code of `hjoonpark` used the chained stereo calibraiton for the initial external calibration. However, I found that it could be unreliable in a sparse view settings where the distance between cameras are big and the veiwing angles are highly different. So I (Hongsuk Choi) did the extenral calibration by performing stereo calibration using the fixed reference camera (the center camera).
 
<p style="text-align:left">
    <img src="./assets/tutorial/12_0000.png" height="300px"/>
    <img src="./assets/tutorial/12_0000_origin.png" height="300px"/>
    <figcaption>Camera 12's 0-th frame is used to define the origin of a coordiates system.</figcaption>
</p>

This center camera and checkerboard is colored *red* when the camera configuration and world points are rendered:

<p style="text-align:left">
    <img src="./assets/tutorial/initial_world_points.png" width="40%"/>
    <img src="./assets/tutorial/final_world_points.png" width="40%"/>
</p>

* *intrinsics* - *n_max_imgs*: number of images to use when calibrating intrinsics parameters of each camera using *cv2.calibrateCamera()*.
* *extrinsics* - *n_max_stereo_imgs*: number of images to use when stereo-calibrating two cameras using *cv2.stereoCalibrate()*.
