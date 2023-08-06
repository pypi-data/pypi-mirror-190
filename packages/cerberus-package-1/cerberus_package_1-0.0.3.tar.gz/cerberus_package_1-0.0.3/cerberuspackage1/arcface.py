
import onnxruntime 
import cv2 
import numpy as np 
import time
import os.path as osp 
from torch import nn 

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
        # print("ok")


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