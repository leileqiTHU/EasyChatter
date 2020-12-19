import socket
import cv2
import numpy as np
import time
import threading

import pyaudio
import wavio
import wave

class sendDataThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    #发送buffer类型的data，会先编码，发送其长度，再发送该数据
    def sendData(self,serversocket, stringData):
        #先发送要发送的数据的长度
        #ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
        serversocket.send(str.encode(str(len(stringData)).ljust(16)))
        #发送数据
        serversocket.send(stringData)

class videoClientThread(sendDataThread):
    def __init__(self):
        super().__init__()
        self.encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),15]
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        serverhost = socket.gethostname()
        serverport = 9999
        self.serversocket.connect((serverhost, serverport))
        while True:
            ret, frame = cap.read()
            #停止0.1S 防止发送过快服务的处理不过来，如果服务端的处理很多，那么应该加大这个值
            time.sleep(0.01)
            #cv2.imencode将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输
            #'.jpg'表示将图片按照jpg格式编码。
            result, imgencode = cv2.imencode('.jpg', frame, self.encode_param)
            #建立矩阵
            videodata = np.array(imgencode)
            #将numpy矩阵转换成buffer形式，以便在网络中传输
            stringVideoData = videodata.tostring()
            ##传输长度和内容
            self.sendData(self.serversocket, stringVideoData)

            if(cv2.waitKey(1)=='q'):
                break

        print("客户端关机")
        serversocket.close()
class voiceClientThread(sendDataThread):
    def __init__(self,videoCT):
        super().__init__()
        self.videoct = videoCT
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        serverhost = socket.gethostname()
        serverport = 10000
        self.serversocket.connect((serverhost, serverport))

        #定义声音输入流，直接调用stream.read(CHUNK)函数即可获取对应的data
        stream = self.p.open(format=self.FORMAT, channels = self.CHANNELS, rate = self.RATE, input = True, frames_per_buffer = self.CHUNK)

        while self.videoct.isAlive():
            stringVoiceData = stream.read(self.CHUNK)
            self.sendData(self.serversocket, stringVoiceData)

            if(cv2.waitKey(1)==ord('q')):
                break
        print("客户端关机")
        stream.stop_stream()
        stream.close()
        self.p.terminate()
        self.serversocket.close()





videoCT = videoClientThread()
videoCT.start()
voiceCT = voiceClientThread(videoCT)
voiceCT.start()

