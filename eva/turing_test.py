import requests
import json
from aip import AipSpeech
import speech_recognition as sr
import pyaudio
import wave,os,time
from nono import globalvariable
from django.shortcuts import render,redirect
# 百度
APP_ID = '16817140'
API_KEY = 'GTcbLqppCEM9Z0uSEBQbLe1S'
SECRET_KEY = 'cvSyqRa5kK7SQCRgYtdCuGQS0DDoudzS'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 图灵
TURING_KEY = "011163556d864101ab96a3d2e3f9a5a8"
URL = "http://openapi.tuling123.com/openapi/api/v2"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}


def listen():
    with open('test.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })

    result_text = result["result"][0]

    print("我: " + result_text)

    return result_text
def robot(request,text=""):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": ""
            },
            "selfInfo": {
                "location": {
                    "city": "京山",#漳州
                    "street": ""#南滨大道
                }
            }
        },
        "userInfo": {
            "apiKey": TURING_KEY,
            "userId": "starky"
        }
    }

    data["perception"]["inputText"]["text"] = text
    response = requests.request("post", URL, json=data, headers=HEADERS)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("AI: " + result)
    # context = {'text': result}
    # render(request, 'eva/Amadeus-index.html', context)
    return result
def ai_speech(text):
    result = client.synthesis(text, 'zh', 3, {
        'vol': 5,  # 音量
        'per': 4,  # 音色（0：女，1：男，3逍遥，4萝莉）
        'spd': 4,  # 音速
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('ai.wav', 'wb') as f:
            f.write(result)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# to(robot(listen()))
# 识别本地文件
# client.asr(get_file_content('ai.wav'), 'wb', 16000, {
#     'dev_pid': 1536,
# })

# from sphfile import SPHFile
def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("test.wav", "wb") as f:
        f.write(audio.get_wav_data())

def play():

    os.system(r"ffmpeg -i ai.wav ai1.wav -loglevel quiet")

    wf = wave.open('ai1.wav', 'rb')
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()
    if (os.path.exists("ai1.wav")):
        os.remove("ai1.wav")
        # print("删除成功")

# def aimain(request,flag):
#     try:
#         while True:
#             if (not flag) or (not globalvariable.flag):
#                 print("已关闭聊天")
#                 break
#             else:
#                 rec()
#                 speak = listen()
#                 ai_speak = robot(request,speak)
#                 ai_speech(ai_speak)
#                 play()
#
#     except Exception as e:
#         aimain(request,flag)
#         pass

