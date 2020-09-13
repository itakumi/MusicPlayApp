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
    volume=100


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
