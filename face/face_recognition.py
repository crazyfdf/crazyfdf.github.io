import dlib
import cv2
import glob
import numpy as np
import os
import json
import math
from django.conf import settings

class Face_recognition:

    # 审查照片
    def face_verification1(self,path):
        # 用于存放人脸的标记
        label=[]
        # 128维的空向量
        data=np.zeros((1,128))

        for file in os.listdir(path):

            path = os.path.join(settings.MEDIA_ROOT, "photo")
            path=os.path.join(path,file)
            feature_tmp = np.zeros((1, 128))
            label_name = file
            num = 0
            for image in os.listdir(path):
                if '.png' in image or '.jpg' in image or '.jpeg' in image:
                    num += 1

                    file_path = os.path.join(path, image)
                    # path = os.path.dirname(path)

                    try:
                        len(self.face_features(file_path))
                            # feature_tmp += self.face_features(file_path)
                    except Exception as e:
                        print('错误图片: {}'.format(file_path))
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        pass


    # 遍历图片目录
    def face_features(self,img):
        image=cv2.imread(img)
        m=image.shape[0]*image.shape[1]
        if m>360000:
            image=cv2.resize(image,(0,0),fx=0.5,fy=0.5)
        # 转换rgb顺序的颜色。
        b, g, r = cv2.split(image)
        img2 = cv2.merge([r, g, b])
        # 检测人脸
        faces = self.detector(image, 1)
        print("检测的人脸图像：", img, "\n")

        if len(faces):
            for index, face in enumerate(faces):
                # 提取68个特征点
                shape = self.shape_predictor(img2, face)
                # 计算人脸的128维的向量
                face_descriptor = self.face_rec_model.compute_face_descriptor(img2, shape)
                #转换numpy的数据结构
                face_array=np.array(face_descriptor).reshape((1,128))

        return face_array

    # 添加标签
    def face_label(self,path):
        # 用于存放人脸的标记
        label=[]
        # 128维的空向量
        data=np.zeros((1,128))

        for file in os.listdir(path):
            path = os.path.join(settings.MEDIA_ROOT, "photo")
            path=os.path.join(path,file)
            feature_tmp = np.zeros((1, 128))
            label_name = file
            num = 0
            for image in os.listdir(path):
                if '.png' in image or '.jpg' in image or '.jpeg' in image:
                    num += 1

                    file_path = os.path.join(path, image)
                    # path = os.path.dirname(path)
                    print('current image: {}, \ncurrent label: {}'.format(file_path, label_name))
                    if len(self.face_features(file_path)):
                        feature_tmp += self.face_features(file_path)
            if num > 0:
                feature = feature_tmp / num
                # 保存每个人的人脸特征
                data = np.concatenate((data, feature))
                # 保存标签
                label.append(label_name)
        # 因为data的第一行是128维0向量，所以实际存储的时候从第二行开始
        data = data[1:, :]
        # 保存人脸特征向量合成的矩阵到本地
        np.savetxt(self.face_descriptor_path, data, fmt='%f')
        label_file = open(self.face_label_path, 'w')
        # 使用json保存list到本地
        json.dump(label, label_file)
        label_file.close()
        # 关闭所有的窗口
        cv2.destroyAllWindows()

    # 载入人脸标签
    def face_find_label(self,face_descriptor):
        # 载入本地特征向量
        face_old_descriptor=np.loadtxt(self.face_descriptor_path,dtype=float)

        face_label=open(self.face_label_path,'r')
        #载入本地标签
        label=json.load(face_label)
        face_label.close()
        face_distance=face_descriptor-face_old_descriptor

        # 欧氏距离来判断
        if len(label)==1:
            euclidean_distance=np.linalg.norm(face_distance)
        else:
            euclidean_distance=np.linalg.norm(face_distance,axis=1,keepdims=True)
        min_distance = euclidean_distance.min()
        print('distance: ', min_distance)
        if min_distance > 0.4:
            return 'other'
        index = np.argmin(euclidean_distance)

        return label[index]
    # 图像识别
    def recognition(self,img):
        img = cv2.imread(img)
        # 检测人脸
        try:
            faces = self.detector(img, 1)

            if faces is not None:
                if len(faces):
                    for i,j in enumerate(faces):
                        left = np.maximum(j.left(), 0)
                        top = np.maximum(j.top(), 0)
                        right = np.minimum(j.right(), img.shape[1])
                        bottom = np.minimum(j.bottom(), img.shape[0])
                        rec = dlib.rectangle(left, top, right, bottom)
                        # 68特征点
                        shape = self.shape_predictor(img, rec)
                        # 128维向量
                        face_descriptor = self.face_rec_model.compute_face_descriptor(img, shape)
                        # 载入标签
                        class_pre = self.face_find_label(face_descriptor)
                        # print(class_pre)
                        cv2.rectangle(img, (rec.left(), rec.top()), (rec.right(), rec.bottom()), (0, 255, 0), 2)
                        cv2.putText(img, class_pre, (rec.left(), rec.top()), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,cv2.LINE_AA)
                    cv2.imshow('image', img)
                    cv2.waitKey(5)

                    return class_pre
                else:
                    print("未识别到人脸")
        except Exception as e:
            print(e)
            pass


    # 摄像头识别
    def face_recognition1(self):
        # 捕获指定摄像头的实时视频流
        cap = cv2.VideoCapture(0)
        # 人脸识别分类器本地存储路径
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        # 循环检测识别人脸
        while True:
            ret, frame = cap.read()  # 读取一帧视频
            if ret is True:
                # 图像灰化，降低计算复杂度
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                continue
            # 使用人脸识别分类器，读入分类器
            cascade = cv2.CascadeClassifier(cascade_path)
            # 利用分类器识别出哪个区域为人脸
            faceRects = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=3, minSize=(32, 32))
            cv2.imshow("start", frame)
            if len(faceRects) > 0:
                for faceRect in faceRects:
                    x, y, w, h = faceRect

                    image = frame[y - 10: y + h + 10, x - 10: x + w + 10]

                    # print(image)
                    cv2.imwrite('1.jpg',image)
                    label=self.recognition('1.jpg')
                    if not label is None:
                        return label
                        break


                # 等待10毫秒看是否有按键输入
                k = cv2.waitKey(10)
                # 如果输入q则退出循环
                if k & 0xFF == ord('q') or k==27:
                    break
                if not label is None:
                    # 释放摄像头并销毁所有窗口
                    cap.release()
                    cv2.destroyAllWindows()

    # 判断两张图片是不是一个人
    def face_detection(self,url_img_1,url_img_2):
        img_path_list = [url_img_1,url_img_2]
        dist = []
        for img_path in img_path_list:
            img = cv2.imread(img_path)
            # 转换rgb顺序的颜色。
            b, g, r = cv2.split(img)
            img2 = cv2.merge([r, g, b])
            # 检测人脸
            faces = self.detector(img, 1)
            if len(faces):
                for index, face in enumerate(faces):
                    # 提取68个特征点
                    shape = self.shape_predictor(img2, face)
                    # 计算人脸的128维的向量
                    face_descriptor = self.face_rec_model.compute_face_descriptor(img2, shape)

                    dist.append(list(face_descriptor))
            else:
                pass
        return dist

    # # 欧氏距离
    # def dist_o(self,dist_1,dist_2):
    #     dis = np.sqrt(sum((np.array(dist_1)-np.array(dist_2))**2))
    #     return dis
    # # 余弦距离
    # def distance(self,embeddings1, embeddings2, distance_metric=0):
    #     if distance_metric == 0:
    #         # Euclidian distance
    #         diff = np.subtract(embeddings1, embeddings2)
    #         dist = np.sum(np.square(diff), 1)
    #     elif distance_metric == 1:
    #         # Distance based on cosine similarity
    #         dot = np.sum(np.multiply(embeddings1, embeddings2), axis=1)
    #         norm = np.linalg.norm(embeddings1, axis=1) * np.linalg.norm(embeddings2, axis=1)
    #         similarity = dot / norm
    #         dist = np.arccos(similarity) / math.pi
    #     else:
    #         raise 'Undefined distance metric %d' % distance_metric
    #
    #     return dist
    #
    # def score(self,url_img_1,url_img_2):
    #     url_img_1 = glob.glob(url_img_1)[0]
    #     url_img_2 = glob.glob(url_img_2)[0]
    #     data = self.face_detection(url_img_1,url_img_2)
    #     goal = self.dist_o(data[0],data[1])
    #     # 判断结果，如果goal小于0.6的话是同一个人，否则不是
    #     return 1-goal

    def __init__(self,predictor_path,face_rec_model_path,face_descriptor_path,face_label_path):
        self.predictor_path = predictor_path
        self.face_descriptor_path = face_descriptor_path
        self.face_label_path = face_label_path
        self.face_rec_model_path = face_rec_model_path
        self.detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor(self.predictor_path)
        self.face_rec_model = dlib.face_recognition_model_v1(self.face_rec_model_path)



# predictor_path = "F://shape_predictor_68_face_landmarks.dat"
# face_rec_model_path = "F://dlib_face_recognition_resnet_model_v1.dat"
# face_descriptor_path="face_feature_vec.txt"
# face_label_path="label.txt"

# face = Face_recognition(predictor_path, face_rec_model_path, face_descriptor_path, face_label_path)

# img_1 = 'image1.jpg'
# img_2 = '185.jpg'
# goal = face.score(img_1,img_2)
# print(goal)
# face.face_recognition1()
# path="D:\\facemodel\data1"
# path = os.path.join(settings.MEDIA_ROOT, "photo")
# path1=face.face_verification1(path)
# face.recognition('1.jpg')