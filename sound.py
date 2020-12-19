import pyaudio
import wavio
import cv2
import wave
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
wave_out_path = 'test.wav'
wave_input_path = 'test.wav'
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
ostream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, output=True, frames_per_buffer = CHUNK)
wf = wave.open(wave_out_path,'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
print("start recording")
record_second =10

for i in range(0, int(RATE*record_second/CHUNK)):
    data = stream.read(CHUNK)
    wf.writeframes(data)
    inputs = cv2.waitKey(1)
    ostream.write(data)
    if(inputs==ord('q')):
        break
stream.stop_stream()
stream.close()
p.terminate()
wf.close()

# print("Playing")
# p = pyaudio.PyAudio()  # 实例化
# wf = wave.open(wave_input_path, 'rb')  # 读 wav 文件
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True)
# data = wf.readframes(CHUNK)  # 读数据
# print("Playing")
# while len(data) > 0:
#     stream.write(data)
#     data = wf.readframes(CHUNK)
#     print("looping!")

# stream.stop_stream()  # 关闭资源
# stream.close()
# p.terminate()