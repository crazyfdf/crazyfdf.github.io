import os
import cv2
import sys
import dlib

def Facecollection(window_name, camera_idx, catch_pic_num, path_name):
    window_name=window_name.encode("gbk").decode(errors="ignore")


    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx,cv2.CAP_DSHOW)
    # 使用opencv人脸识别分类器
    classfier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    # 人脸分类器
    detector = dlib.get_frontal_face_detector()

    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (249,204,226)
    num = 0

    while cap.isOpened():
        try:
            ret, frame = cap.read()  # 读取一帧数据
            if not ret:
                break

            # 将当前帧转换成灰度图像
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 人脸检测，1.1和3分别为图片缩放比例和每一个级联矩形应该保留的邻近个数
            face = classfier.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=3, minSize=(128, 128))
            # 检测人脸
            faces = detector(grey, 1)

            if len(faces)>0 and len(face) > 0:  # 大于0则检测到人脸
                for face in face:  # 单独框出每一张人脸
                    x, y, w, h = face
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
                    # 人脸保存的路径和名称
                    photo_name="facecollection"+str(num)
                    img_name = r'%s/%s.jpg' % (path_name, photo_name)
                    image = frame[y - 10: y + h + 10, x - 10: x + w + 10]

                    # 将人脸保存为图片
                    cv2.imencode('.jpg', image)[1].tofile(img_name)
                    num += 1
                    if num > (catch_pic_num):  # 如果超过指定最大保存数量退出循环
                        # 释放摄像头并销毁所有窗口
                        cap.release()
                        cv2.destroyAllWindows()
                        break

                    # 画出矩形框
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

                    # 显示当前捕捉到了多少人脸图片了
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, 'num:%d' % (num), (x + 30, y + 30), font, 1, (255, 0, 255), 4)
            # 超过指定最大保存数量结束程序
            if num > (catch_pic_num):
                # 释放摄像头并销毁所有窗口
                cap.release()
                cv2.destroyAllWindows()
                break
            # 显示图像
            cv2.imshow(u'{}'.format(window_name), frame)
            # 按键q退出
            c = cv2.waitKey(10)

            if c & 0xFF == ord('q') or c==27:
                # 释放摄像头并销毁所有窗口
                cap.release()
                cv2.destroyAllWindows()
                break
        except Exception as e:
            pass
    # # 释放摄像头并销毁所有窗口
    # cap.release()
    # cv2.destroyAllWindows()


# if __name__ == '__main__':
#     if len(sys.argv) != 1:
#         print("Usage:%s camera_id face_num_max path_name\r\n" % (sys.argv[0]))
#     else:
#         path='D:\\facemodel\\data\\sy'
#         if not os.path.exists(path):
#             os.makedirs(path)
#         Facecollection("人脸采集", 0, 1000,path)

