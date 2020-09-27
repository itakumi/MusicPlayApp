import sys
import numpy as np
import pyaudio
import wave
import os
import time
import threading
import msvcrt
import tkinter as tk
import tkinter
from tkinter import *
from tkinter import ttk
from functools import partial
import glob
import pydub
import random
import shutil
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import pickle

class AudioInformation:
    outputdeviceindex=-1
    Key=0 #音程
    r12=1 #周波数に掛けると音程が変わる
    Quickness=1 #速度
    song=None #曲の情報
    root=None #Tkinter
    playlist_len=-1 #Playlistの長さ
    mode=-1 #再生モード
    basedirname=None #カレントディレクトリが入る
    head,last=None,None #曲のスタート、最後のポインタ位置
    quit=False #曲終了のフラグ
    duration=None #曲の長さ
    thread_play=None #再生中かどうか
    renew_flag=False #音程を更新するかどうか
    back_flag,shuffle_flag,directory_repeat_flag,one_repeat_flag=False,False,False,False #再生方法の変更
    next_play_index=0 #GUIから選択したときにインデックスを取得
    next_play_index_list=[] #GUIから選択したときにインデックスを取得
    onesecframes=None #1秒当たりのフレーム数
    label,playtimeframe=None,None #再生時間のラベル
    targetname_0=None #パス指定のentry
    targetname_1=None #フォルダ指定のentry
    targetname_2=None #ファイル指定のentry
    targetname_0_str=None #パス指定のentry
    targetname_1_str=None #フォルダ指定のentry
    targetname_2_str=None #ファイル指定のentry
    scalebar=None #曲の位置を示すスケールバー
    stop_flag=False
    pitch_entry,speed_entry=None,None
    volume=100 #音量
    algorithm=1 #0:愚直アルゴリズム、1:Librosa
    favorite_songlist=[]
    isfavorite=0 #「お気に入りのみ」モードかどうか
    isfavoritevar=None
    algorithmvar=None
    menu_ROOT=None
    menu_playlist=None
    canvas=None
    playviews=None
    directory_playviews=None
    allplayviews=None
    rootA=None
    def __init__(self):
        self.basedirname=os.path.dirname(os.path.abspath("__file__"))
        if not os.path.isdir(self.basedirname+'/PickleData'):
            os.mkdir(self.basedirname+'/PickleData')
        if os.path.exists(self.basedirname+"/PickleData/MusicPlayApp_allplayviews.pickle"):
            with open(self.basedirname+'/PickleData/MusicPlayApp_allplayviews.pickle', 'rb') as f:
                self.allplayviews=pickle.load(f)
        else:
            self.allplayviews=dict()
    def Reload_allplayviews(self):
        if not os.path.isdir(self.basedirname+'/PickleData'):
            os.mkdir(self.basedirname+'/PickleData')
        if os.path.exists(self.basedirname+"/PickleData/MusicPlayApp_allplayviews.pickle"):
            with open(self.basedirname+'/PickleData/MusicPlayApp_allplayviews.pickle', 'rb') as f:
                self.allplayviews=pickle.load(f)
        else:
            self.allplayviews=dict()

class ClassFrame(tk.Frame):
    def __init__(self, master, bg=None, width=None, height=None):
        super().__init__(master, bg=bg, width=width, height=height)

def NormalPlay_Set(KeyInput,SpeedInput):#標準再生
    KeyInput.delete(0,tkinter.END)
    SpeedInput.delete(0,tkinter.END)
    KeyInput.insert(tkinter.END,"0")
    SpeedInput.insert(tkinter.END,"1")


def help():
    print("操作説明")
    print("p:最初から")
    print("b:前のファイルへ")
    print("n:次のファイルへ")
    print("s:10秒戻る")
    print("d:3秒戻る")
    print("f:3秒進む")
    print("g:10秒進む")
    print("e:音程リセット")
    print("r:速度リセット")
    print("q:PlayList終了")
    print("z:シャッフル再生")
    print("x:フォルダリピート")
    print("c:1曲リピート")
    print("v:ノーマル再生")
    print("Enter:一時停止、再生")
    print("矢印(上):キーを上げる")
    print("矢印(下):キーを下げる")
    print("矢印(右):速度を上げる")
    print("矢印(左):速度を下げる")
def gen_xfade_honesty(x_pre, x_next, fadetime, sr):#愚直アルゴリズム
    ft_len = int(fadetime)#*sr)
    if x_pre is None:
        xfade = x_next
    else:
        x_pre=np.frombuffer(x_pre,dtype="int16")
        x_next=np.frombuffer(x_next,dtype="int16")
        prelen=len(x_pre)
        nextlen=len(x_next)
        x_pre_len = len(x_pre)
        x_next_len = len(x_next)
        x_pre_len -= ft_len
        x_next_len -= ft_len
        r = np.arange(0, ft_len)*np.pi/ft_len
        w_fo = (0.5+0.5*np.cos(r))**0.5
        w_fi = (0.5-0.5*np.cos(r))**0.5
        x_pre=x_pre.astype(np.float64)
        x_next=x_next.astype(np.float64)
        x_pre[-ft_len:]*=w_fo
        x_next[:ft_len]*=w_fi
        #sin_wave = np.sin(r)/10+1
        xfade= np.r_[x_pre,np.zeros(x_next_len)] + np.r_[np.zeros(x_pre_len),x_next]
        #xfade[int((len(xfade)-ft_len)/2):int((len(xfade)+ft_len)/2)]*=sin_wave
        #xfade=np.fft.fft(xfade)
        #xfade_abs=np.abs(xfade)
        #xfade_amp=xfade_abs/len(xfade)*2
        #xfade_amp[0]=xfade_amp[0]/2
        #xfade=np.where(xfade_amp>8000,0,xfade)
        #xfade[10:]=0
        #xfade=np.fft.ifft(xfade)
        #xfade=xfade.real
        xfade*=0.78
        xfade=xfade.astype(np.int16)
        x_pre=xfade[:prelen]
        x_next=xfade[prelen:]
        x_pre=np.ndarray.tobytes(x_pre)
        x_next=np.ndarray.tobytes(x_next)
    return x_pre,x_next

def gen_stft(data, Quickness,r12,fs,fn):#短時間フーリエ変換
    data=np.frombuffer(data,dtype="int16")
    data=data.astype(np.float64)
    frq,t,Pxx=scipy.signal.stft(data,fs=int(fn/fs),nperseg=2048)
    Pxx=Pxx.real
    Pxx = np.where(np.abs(Pxx) >= 10, Pxx, 0)
    Converted_Pxx=[]
    for i in range(Pxx.shape[0]):
        Converted_Pxx.append(samplerate.resample(Pxx[i],r12/Quickness,'sinc_best'))
    _,data=scipy.signal.istft(Converted_Pxx,2048)
    data=data.astype("int16")
    data=data.tobytes()
    return data
