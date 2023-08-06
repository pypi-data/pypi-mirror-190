
import onnxruntime 
import cv2 
import numpy as np 
import time
import os.path as osp 

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
        
    def get_feature(self, img):
        input_image = np.expand_dims(img, axis=0).astype(np.float32)

        ort_inputs = {self.session.get_inputs()[0].name: input_image}

        feature = self.session.run(None, ort_inputs)

        return feature



if __name__ == "__main__":

    providers = [
        'CUDAExecutionProvider', 
        # 'CPUExecutionProvider',
    ]

    # ort_session =  onnxruntime.InferenceSession("/home/hoangleminh/work_ceberus/face_reg/arcface_onnx_model/model.onnx", providers=providers)

    arcface = ARCFACE('./arcface_onnx_model/model.onnx')
    start = time.time()

    img1 = cv2.imread('./images/1.png')
    img1 = cv2.resize(img1, (112, 112))
    img1 = img1.transpose(2, 0, 1)
    feature1 = arcface.get_feature(img1)

    end = time.time()

    img2 = cv2.imread('./images/2.png')
    img2 = cv2.resize(img2, (112, 112))
    img2 = img2.transpose(2, 0, 1)
    feature2 = arcface.get_feature(img2)

    from sklearn.metrics.pairwise import cosine_similarity

    score = cosine_similarity(feature1[0], feature2[0])

    print("score: ", score)
    print("time: ", end - start)