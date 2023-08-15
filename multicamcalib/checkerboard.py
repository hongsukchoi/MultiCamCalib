import numpy as np
from cv2 import aruco


class Checkerboard():
    def __init__(self, n_cols, n_rows, sqr_size):
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.sqr_size = sqr_size
        self.chb_pts = self._create_chb_points()

        self.charuco_grid_board = aruco.CharucoBoard(
            (n_rows+1, n_cols+1), # markersX, markersY
            30.0 / 1000,  # squareLength
            30.0 / 1000 * 6 / 8, #markerLength
            aruco.getPredefinedDictionary(aruco.DICT_5X5_100), # aruco_dict
        )

        
    def _create_chb_points(self):
        #        columns
        #   +z o -------- +y
        # rows |
        #      |
        #      | +x

        pts = []
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                pts.append([r*self.sqr_size, c*self.sqr_size, 0])
        return np.float32(pts)

