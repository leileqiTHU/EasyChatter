import socket
import cv2
import numpy as np
import time
import pyaudio
import wavio
import wave
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
#定义声音输入流，直接调用stream.read(CHUNK)函数即可获取对应的data
stream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
ostream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, output=True, frames_per_buffer = CHUNK)

#发送buffer类型的data，会先发送其长度，再发送该数据
def sendData(serversocket, stringData):
    #先发送要发送的数据的长度
    #ljust() 方法返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
    serversocket.send(str.encode(str(len(stringData)).ljust(16)))
    #发送数据
    serversocket.send(stringData)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverhost = socket.gethostname()
serverport = 10000
serversocket.connect((serverhost, serverport))

while True:
    stringVoiceData = stream.read(CHUNK)
    sendData(serversocket, stringVoiceData)
    # print(stringVoiceData)
    # break
    # ostream.write(stringVoiceData)
    # print(frame.shape)
    if(cv2.waitKey(1)==ord('q')):
        break
print("客户端关机")
stream.stop_stream()
stream.close()
p.terminate()
serversocket.close()
