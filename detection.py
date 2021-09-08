import sys
import os
cur_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(cur_dir)

from utils.torch_utils import select_device
from utils.general import check_img_size,  non_max_suppression, scale_coords,  set_logging
from utils.datasets import letterbox
from models.experimental import attempt_load
import numpy as np
import torch.backends.cudnn as cudnn
import torch
import cv2



class Detection:
    def __init__(self, path_weight, imgsize=640, device="", conf_thres=0.25, iou_thres=0.45):
        # set_logging()
        self._device = select_device(device)
        self.half = self._device.type != 'cpu'
        self._weight = path_weight
        self._model = None
        self._imgsize = imgsize
        self. _conf_thres = conf_thres
        self._iou_thres = iou_thres
        self.stride = None
        self.load_model()

    def load_model(self):
        set_logging()
        self._model = attempt_load(self._weight, map_location=self._device)
        self.stride = int(self._model.stride.max())  # model stride
        self._imgsz = check_img_size(self._imgsize, s=self.stride)
        if self.half:
            self._model.half()  # to FP16
        # Get names and colors
        self._names = self._model.module.names if hasattr(
            self._model, 'module') else self._model.names
        if self._device.type != 'cpu':
            self._model(torch.zeros(1, 3, self._imgsize, self._imgsize).to(self._device).type_as(next(self._model.parameters())))  # run once

        print("model loaded")

    def detect(self, img, is_draw=False):
        num_head = 0
        # img = cv2.resize(img, (640,640))
        img0 = img.copy()

        img = letterbox(img, self._imgsize, stride=self.stride)[0]

        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self._device)
        img = img.half() if self._device.type != 'cpu' else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        
        pred = self._model(img)[0]
        pred = non_max_suppression(
            pred, conf_thres=self._conf_thres, iou_thres=self._iou_thres, agnostic=True)

        
        return  pred, img.shape[2:]

    