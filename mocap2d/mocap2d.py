import torch
import cv2
import numpy as np

from torchvision.models.detection import keypointrcnn_resnet50_fpn as keypoint


class BoneDetector:
    __BONES = [
        (17, 0), (17, 5), (5, 7), (7, 9), (17, 6), (6, 8), (8, 10), (17, 18),
        (18, 11), (11, 13), (13, 15), (18, 12), (12, 14), (14, 16)
    ]

    def __init__(self, gpu=False):
        self._model = keypoint(pretrained=True)
        self._device = None
        if gpu:
            print("Detecting gpu device...")
            self._device = torch.device("cuda:0")
            if self._device is None:
                raise Exception("No GPU instance detected!!")
            self._model.to(self._device)
        self._model.eval()
        print("Pose detector initialized.")

    def _image_to_tensor(self, image):
        img = np.transpose(image / 255, (2, 0, 1))
        img = torch.from_numpy(img).float()
        if self._device:
            img = img.to(self._device)
        return img

    def extract_bone(self, image, show=False):
        im_tensor = self._image_to_tensor(image)
        result = self._model([im_tensor])[0]
        points, scores = self._find_human(result)
        if points is None:
            return None
        if show:
            self._draw_human(image, points)
        skeleton = {}
        for idx, keys in enumerate(self.__BONES):
            k1, k2 = keys
            skeleton[f"bone{idx + 1}"] = self._get_bone_vector(
                points[k1], points[k2])
        pt1 = points[17]
        pt2 = points[18]
        ref = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
        return skeleton, points[17], ref

    def _draw_human(self, image, points):
        for pt1, pt2 in self.__BONES:
            image = cv2.line(image, tuple(points[pt1][:2]),
                             tuple(points[pt2][:2]), (255, 0, 0), 3)
        cv2.imshow("Result", image)
        cv2.waitKey(1)

    @staticmethod
    def _get_bone_vector(key1, key2):
        return int(key2[0] - key1[0]), int(key1[1] - key2[1])

    def _find_human(self, raw_result):
        scores = raw_result["scores"].data.cpu().numpy()
        if len(scores) == 0:
            return None, None
        human_idx = np.argmax(scores)
        points = raw_result["keypoints"][human_idx].data.cpu().numpy()
        scores = raw_result["keypoints_scores"][human_idx].data.cpu().numpy()
        mid_top = self._mid_point(points[5], points[6])
        mid_bot = self._mid_point(points[11], points[12])
        points = np.append(points, [mid_top, mid_bot], axis=0).astype(np.int32)
        scores = np.append(
            scores, [scores[5] + scores[6], scores[11] + scores[12]]
        )
        return points, scores

    @staticmethod
    def _mid_point(point1, point2):
        return (point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2, 1
