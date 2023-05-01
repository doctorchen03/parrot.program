
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from pynput.keyboard import Key, Listener,Controller
from gtts import gTTS
import winsound
import uuid
import pyglet.media as media
import time
from datetime import datetime,timedelta
import os
from pathlib import Path
import whisper

freq = 44100
duration = 5
recording = None
press_cnt = 0

#parrot program
def Voice_TW(text):
    #text = '''你可以問下列類別的相關問題,設備請購,BPM其他,系統'''
    #print('Voice_TW()=>'+text)
    est_play_len = len(text)*0.3
    #print(est_play_len)
    voiceFile="voice/pp_@.wav".replace('@',datetime.now().strftime('%Y%m%d_%H%M%S')+"_" + str(uuid.uuid4()))
    #<zh-TW>,<zh-CN>,<en>
    tts = gTTS(text, lang='zh-TW', slow=False)
    tts.save(voiceFile)
    src=media.load(voiceFile)
    player=media.Player()
    player.queue(src)
    player.volume=1.0
    player.play()
    time.sleep(est_play_len)#*****************************
    #os.remove(voiceFile)   
    #winsound.Beep(frequency=1500, duration=300)

def VoiceRecord():
    print("[*]請開始講話")
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()    
    voice_file = "voice/pp_@.wav".replace('@',datetime.now().strftime('%Y%m%d_%H%M%S')+"_" + str(uuid.uuid4()))
    wv.write(voice_file, recording, freq, sampwidth=2)
    print("[*]請結束講話")

def Voice2Text():
    dir_path = "D:\\PROJECTS\\ZFOLD.NET\\BACK_TESTER_VCP\\ChatGPT\\TEST_WHISPER\\voice"
    paths = sorted(Path(dir_path).iterdir(), key=os.path.getmtime)
    latest_voice_file = str(paths[-1])
    print(latest_voice_file)
    #
    Model_Type = "small"
    DEVICE = "cpu"
    model = whisper.load_model(Model_Type, device=DEVICE)
    result = model.transcribe(latest_voice_file, fp16=False)
    print(result["text"])
    Voice_TW(result["text"])
    pass

def on_press(key,press_cnt):
    print('{0} pressed'.format(key))
    print(str(press_cnt))
    if str(key).upper() == "'S'":
        press_cnt += 1
        print(str(press_cnt))
        winsound.Beep(frequency=1500, duration=300)
        VoiceRecord()
        winsound.Beep(frequency=1500, duration=300)
        Voice2Text()
        winsound.Beep(frequency=1500, duration=300)
        pass

def on_release(key):
    print('{0} release'.format(key))
    if str(key).upper() == "'S'":
        pass
    elif key == Key.esc:
        # Stop listener
        return False

if __name__ == '__main__':
    print("--------------------------------------------------------")
    print("-                   parrot program                     -")
    print("-           Created by BrianChen-Wistronits            -")
    print("-           (2023/5/11 WITS.LAB經驗分享DEMO)            -")
    print("--------------------------------------------------------")
    print("-[使用說明]                                             -")
    print("-[*] 點選<S>，開始講話，然後parrot program將學你說話-")
    print("-[*] <ESC>=離開程式                                     -")
    Voice_TW("點選S，開始講話，然後parrot program將學你說話")
    try:
        with Listener(
            on_press=lambda event: on_press(event, press_cnt=press_cnt),
            on_release=on_release) as listener:listener.join()
    except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print (message)   