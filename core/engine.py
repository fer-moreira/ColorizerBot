from core.logger import logging
from core.exceptions import ValueIsTooLargeError, ValueIsTooSmallError
import numpy as np
from cv2 import cv2 as cv
import os.path

class DeepLearning (object):
    def __init__ (self, input_path, output_path):
        self.file = input_path
        self.output_path = output_path
        self.resolution_x = 200
        self.resolution_y = 200
        self.prototxt_path = ""
        self.caffemodel_path = ""
        self.__pts_in_hull = "./core/helpers/pts_in_hull.npy"
        logging.info("Input > {0}".format(self.file))


    def load (self):
        # Read image data with OpenCV
        self.frame = cv.imread(self.file)
        self.numpy_file = np.load(self.__pts_in_hull)
        self.Caffe_net = cv.dnn.readNetFromCaffe(self.prototxt_path,self.caffemodel_path)

    def build (self):
        if self.output_path == ""\
        or self.caffemodel_path == ""\
        or self.prototxt_path == "":
            raise FileNotFoundError

        if ((self.resolution_x + self.resolution_y) / 2) < 10:
            raise ValueIsTooSmallError("Minimum Resolution x10*y10 ")
        if ((self.resolution_x + self.resolution_y) / 2) > 2000:
            raise ValueIsTooSmallError("Maximum Resolution x2000*y2000")

        logging.info("Building...")

        # Loading Data
        self.numpy_file = self.numpy_file.transpose().reshape(2, 313, 1, 1)
        self.Caffe_net.getLayer(self.Caffe_net.getLayerId('class8_ab')).blobs = [self.numpy_file.astype(np.float32)]
        self.Caffe_net.getLayer(self.Caffe_net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

        # Lightness L
        rgb_img = (self.frame[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
        lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
        l_channel = lab_img[:,:,0] 
        l_channel_resize = cv.resize(l_channel, (self.resolution_x, self.resolution_y))
        l_channel_resize -= 50
        
        # (A,B) Probability Distribution
        self.Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
        ab_channel = self.Caffe_net.forward()[0,:,:,:].transpose((1,2,0)) 
        (original_height,original_width) = rgb_img.shape[:2] 
        ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
        lab_output = np.concatenate((l_channel[:,:,np.newaxis],ab_channel_us),axis=2) 
        self.bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)

        # Lab Image to file
        cv.imwrite(self.output_path, (self.bgr_output*255).astype(np.uint8))
        logging.info("Output > {0}".format(self.output_path))