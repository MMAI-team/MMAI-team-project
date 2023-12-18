import cv2
import numpy as np


class SiftMatcher:

    def __init__(self):
        self.__sift = cv2.SIFT_create()

    def predict(self, image_1_path, image_2_path):
        image_1 = cv2.imread(image_1_path, cv2.IMREAD_GRAYSCALE)
        image_2 = cv2.imread(image_2_path, cv2.IMREAD_GRAYSCALE)

        homography_coeff = self.__find_homography_coefficient(image_1, image_2)

        if -0.01 < homography_coeff < 0.01:
            return False
        else:
            return True

    def __find_homography_coefficient(self, image_1, image_2):
        matches, (keypoints_1, keypoints_2) = self.__get_matches(image_1, image_2)

        if len(matches) > 3:
            src_pts = np.float32([keypoints_1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints_2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            homography_matrix, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            return np.linalg.det(homography_matrix)

        return None

    def __get_matches(self, image_1, image_2):
        keypoints_1, descriptors_1 = self.__sift.detectAndCompute(image_1, None)
        keypoints_2, descriptors_2 = self.__sift.detectAndCompute(image_2, None)

        matcher = cv2.BFMatcher()
        matches = matcher.knnMatch(descriptors_1, descriptors_2, k=2)

        matches_filtered = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                matches_filtered.append(m)

        return matches_filtered, (keypoints_1, keypoints_2)
