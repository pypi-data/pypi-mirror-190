
import onnxruntime 
import cv2 
import numpy as np 
import time
import os.path as osp 
from torch import nn 
import math
from PIL import Image

cos = nn.CosineSimilarity(dim=1, eps=1e-6)



class ARCFACE:
    def __init__(self, model_file = None, provider = None):
        self.model_file = model_file
        self.provider = provider
        if self.provider is None:
            assert self.model_file is not None 
            assert osp.exists(self.model_file)
            self.session = onnxruntime.InferenceSession(self.model_file, providers=['CUDAExecutionProvider'])
        else:
            self.session = onnxruntime.InferenceSession(self.model_file, providers=self.provider)
    
    def euclidean_distance(self, a, b):
        x1 = a[0]; y1 = a[1]
        x2 = b[0]; y2 = b[1]
        return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))
        
    def get_feature(self, img):
        input_image = np.expand_dims(img, axis=0).astype(np.float32)

        ort_inputs = {self.session.get_inputs()[0].name: input_image}

        feature = self.session.run(None, ort_inputs)

        return feature

    def preprocess(self, img):
        img = cv2.resize(img, (112, 112))
        img = img / 255.0
        img = (img - 0.5) / 0.5
        img = img.transpose(2, 0, 1)
        return img
    
    def alignment(self, img, l_eye, r_eye):
        left_eye_x = l_eye[0]; left_eye_y = l_eye[1]
        right_eye_x = r_eye[0]; right_eye_y = r_eye[1]

        if left_eye_y > right_eye_y:
            point_3rd = (right_eye_x, left_eye_y)
            direction = -1 #rotate same direction to clock
            print("rotate to clock direction")
        else:
            point_3rd = (left_eye_x, right_eye_y)
            direction = 1 #rotate inverse direction of clock
            # print("rotate to inverse clock direction")

        a = self.euclidean_distance(l_eye, point_3rd)
        b = self.euclidean_distance(r_eye, l_eye)
        c = self.euclidean_distance(r_eye, point_3rd)

        cos_a = (b*b + c*c - a*a)/(2*b*c)
        # print("cos(a) = ", cos_a)
        
        angle = np.arccos(cos_a)
        # print("angle: ", angle," in radian")
        
        angle = (angle * 180) / math.pi
        # print("angle: ", angle," in degree")

        if direction == -1:
            angle = 90 - angle

        new_img = Image.fromarray(img)
        new_img = np.array(new_img.rotate(direction * angle))
        return new_img


if __name__ == "__main__":

    providers = [
        'CUDAExecutionProvider', 
        # 'CPUExecutionProvider',
    ]

    # ort_session =  onnxruntime.InferenceSession("/home/hoangleminh/work_ceberus/face_reg/arcface_onnx_model/model.onnx", providers=providers)

    arcface = ARCFACE('./arcface_onnx_model/model.onnx')
    start = time.time()

    img1 = cv2.imread('./images/test.jpg')
    img1 = arcface.preprocess(img1)
    feature1 = arcface.get_feature(img1)

    end = time.time()

    img2 = cv2.imread('./images/test1.jpg')
    img2 = arcface.preprocess(img2)
    feature2 = arcface.get_feature(img2)

    # from sklearn.metrics.pairwise import cosine_similarity
    import torch
    score = cos(torch.tensor(feature1[0]), torch.tensor(feature2[0]))

    print("score: ", score)
    print("time: ", end - start)