# socket命名规范：与谁通信的socket就命名为谁，如用来与server通信的socket就命名为serversocket，与client通信的socket就命名为clientsocket
import socket
import time
import threading
import cv2
import numpy as np
import pyaudio
import wavio
import wave
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
class serve_client_video(threading.Thread):
    def __init__(self, clientsocket, clientaddr):
        threading.Thread.__init__(self)
        self.clientaddr = clientaddr
        self.clientsocket = clientsocket
    def run(self):
        print("连接地址"+str(self.clientaddr))
        lastTimeRecvData = time.time()
        # self.clientsocket.setblocking(False)
        self.clientsocket.settimeout(20)

        # ostream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, output=True, frames_per_buffer = CHUNK)
        
        while True:
            stringVideoData = self.recvData()
            videodata = np.frombuffer(stringVideoData, np.uint8)#将获取到的字符流数据转换成1维数组
            decoded_img=cv2.imdecode(videodata,cv2.IMREAD_COLOR)#将数组解码成图像
            cv2.imshow('SERVER',decoded_img)#显示图像

            # stringVoiceData = self.recvData()
            # try:
            #     ostream.write(stringVoiceData)
            # except Exception as e:
            #     print(e)
            #     ostream.close()
            #     ostream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, output=True, frames_per_buffer = CHUNK)
            if(cv2.waitKey(1)==ord('q')):
                break

        # if(msg==b''):
        #     print('客户端断开连接')
        # else:
        #     self.clientsocket.send(timeouterr.encode('utf-8'))
        #     print(timeouterr)
        self.clientsocket.close()
        # ostream.stop_stream()
        # ostream.close()
        # p.terminate()
        cv2.destroyAllWindows()
    #从socket接收数据，字符串形式
    def recvData(self):
        length = self.recvall(self.clientsocket,16)#获得图片文件的长度,16代表获取长度
        stringData = self.recvall(self.clientsocket, int(length))#根据获得的文件长度，获取图片文件
        return stringData
    def recvall(self, sock, count):
        buf=b''
        while count:
            newBuf = sock.recv(count)
            if(not newBuf):
                return None
            buf+=newBuf
            count-=len(newBuf)
            return buf

class serve_client_voice(threading.Thread):
    def __init__(self, clientsocket, clientaddr):
        threading.Thread.__init__(self)
        self.clientaddr = clientaddr
        self.clientsocket = clientsocket
    def run(self):
        print("连接地址"+str(self.clientaddr))
        lastTimeRecvData = time.time()
        # self.clientsocket.setblocking(False)
        self.clientsocket.settimeout(20)

        ostream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, output=True, frames_per_buffer = CHUNK)
        while True:

            stringVoiceData = self.recvData()
            if(stringVoiceData==False):
                break
            try:
                ostream.write(stringVoiceData)
            except Exception as e:
                print(e)
                ostream.close()
                ostream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, output=True, frames_per_buffer = CHUNK)
            if(cv2.waitKey(1)==ord('q')):
                break
        self.clientsocket.close()
        ostream.stop_stream()
        ostream.close()
    #从socket接收数据，字符串形式
    def recvData(self):
        length = self.recvall(self.clientsocket,16)#获得图片文件的长度,16代表获取长度
        if(length==None):
            return False
        stringData = self.recvall(self.clientsocket, int(length))#根据获得的文件长度，获取图片文件
        return stringData
    def recvall(self, sock, count):
        buf=b''
        while count:
            newBuf = sock.recv(count)
            if(not newBuf):
                return None
            buf+=newBuf
            count-=len(newBuf)
            return buf
# threads=[]

class startlistener(threading.Thread):
    def __init__(self, stype):#type='video'/'voice'
        threading.Thread.__init__(self)
        self.type = stype
        self.timecount=0
        self.timeout=10#超时时间为3*10秒，若30秒未收到套接字连接请求，则超时中止线程 
        print(stype)
        if(stype=='video'):
            print("子线程开始监听9999端口")
            self.listenport = 9999
        else:
            self.listenport = 10000
            print("子线程开始监听10000端口")
        
        self.listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenhost = socket.gethostname()
        self.listensocket.bind((self.listenhost, self.listenport))
        self.listensocket.listen(5)
    def run(self):
        while True:
            
            if(threading.activeCount()<10):#包括主线程不能超过5个线程
                self.timecount=0
                clientsocket, clientaddr = self.listensocket.accept()
                if self.type=='video':
                    print('9999端口收到连接请求')
                    thread = serve_client_video(clientsocket, clientaddr)
                else:
                    print('10000端口收到连接请求')
                    thread = serve_client_voice(clientsocket, clientaddr)
                thread.start()
                # threads.append(thread)
            elif(self.timecount>self.timeout):
                time.sleep(3)
                self.timecount+=1
            else:#长时间没有收到连接请求（30秒）
                    print("服务器长达"+str(timeout*3)+"秒未收到连接请求，超时退出")
                    break
        self.listensocket.close()

timeouterr = '超时断开连接'
listenhost = socket.gethostname()
print(threading.activeCount())#应该输出1，因为此时只有主线程在运行




videostartlistenerThread = startlistener('video')
voicestartlistenerThread = startlistener('voice')

videostartlistenerThread.start()
voicestartlistenerThread.start()

print('服务器子线程持续监听中')
while True:
    time.sleep(3)

