from MusicPlayApp_Interface_WithLibrosa import *
import librosa
info=AudioInformation()

def dirdialog_clicked():#フォルダ参照
    iDir = os.path.abspath(os.path.dirname("__file__"))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    info.targetname_0.delete(0,tkinter.END)
    info.targetname_2.delete(0,tkinter.END)
    info.targetname_1.delete(0,tkinter.END)
    info.targetname_1.insert(tkinter.END,iDirPath)
def dir_play(PlayListTkinter):#フォルダ再生
    if os.path.isdir(info.targetname_1.get()):
        info.mode=1
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')
            #print("指定されたパスが存在しません")
def filedialog_clicked():#ファイル参照
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname("__file__"))
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    info.targetname_0.delete(0,tkinter.END)
    info.targetname_1.delete(0,tkinter.END)
    info.targetname_2.delete(0,tkinter.END)
    info.targetname_2.insert(tkinter.END,iFilePath)
def file_play(PlayListTkinter):#ファイル再生
    if os.path.isfile(info.targetname_2.get()):
        info.mode=2
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')
        #print("指定されたパスが存在しません")
def getTextInput(PlayListTkinter):#パス指定再生
    if info.targetname_0.get()=='./' or os.path.isdir(info.targetname_0.get()):
        info.mode=0
        PlayListTkinter.quit()
    elif os.path.isfile(info.targetname_0.get()):
        info.mode=0
        print("fileplaymodeに移ります")
        info.mode=2
        info.targetname_2.delete(0,tkinter.END)
        info.targetname_2.insert(tkinter.END,info.targetname_0.get())
        info.targetname_0.delete(0,tkinter.END)
        info.targetname_1.delete(0,tkinter.END)
        time.sleep(0.5)
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')
        #print("指定されたパスが存在しません")
def setcurrent():#カレントセット
    info.targetname_1.delete(0,tkinter.END)
    info.targetname_2.delete(0,tkinter.END)
    info.targetname_0.delete(0,tkinter.END)
    info.targetname_0.insert(tkinter.END,"./")

def KeySpeedRead(KeySpeedInput,KeyInput,SpeedInput):#最初のウィンドウにおいてキーと速度を読み込み時
    if KeyInput.get().replace(',', '').replace('.', '').replace('-', '').isnumeric() and SpeedInput.get().replace(',', '').replace('.', '').replace('-', '').isnumeric():
        try:
            round(float(SpeedInput.get()),2)
            round(float(SpeedInput.get()),2)
        except:
            messagebox.showinfo('エラー', 'float型として適切ではありません')
            return
        if round(float(KeyInput.get()),2)>=-12 and round(float(KeyInput.get()),2)<=12:
            info.Key = round(float(KeyInput.get()),2)
            if round(float(SpeedInput.get()),2)>=0.01:
                info.Quickness = round(float(SpeedInput.get()),2)
                KeySpeedInput.destroy()
            else:
                messagebox.showinfo('エラー', 'Speedは0.01以上でお願いします')
        else:
            messagebox.showinfo('エラー', 'Keyは-12~12でお願いします')
            #print("Keyは-12~12でお願いします.")
    else:
        messagebox.showinfo('エラー', 'KeyとSpeedはfloat型でお願いします')
        #print("KeyとSpeedはfloat型でお願いします")

class AudioFile:
        chunk_mul=128
        chunk = 1024*chunk_mul
        buffer=1024*32
        def __init__(self, file, speed):
           """ Init audio stream """
           self.wf = wave.open(file, 'rb')
           self.speed = speed
           self.p = pyaudio.PyAudio()
           self.stream = self.p.open(
               format = self.p.get_format_from_width(self.wf.getsampwidth()),
               channels = self.wf.getnchannels(),
               #frames_per_buffer = self.chunk,
               frames_per_buffer = self.buffer,
               #rate = int(self.wf.getframerate()*self.speed),
               rate = int(self.wf.getframerate()),
               input = True,
               output = True)
        def play(self):
            """ Play entire file """
            print("playing...")
            info.head=self.wf.tell()
            data = self.wf.readframes(1)
            frames=self.wf.getnframes()
            framerate=self.wf.getframerate()
            info.last=info.head+frames
            info.duration=self.wf.getnframes()/self.wf.getframerate()
            info.onesecframes=(info.last-info.head)/info.duration
            info.quit=False
            info.stop_flag=False
            nextpos=None
            while len(data)!=0 and info.quit==False:
                if info.renew_flag:
                    self.renew()
                    info.renew_flag=False
                if msvcrt.kbhit():
                    backgroundprocess(msvcrt.getch())
                else:
                    if self.stream.is_active():
                        currentpos=self.wf.tell()
                        data = self.wf.readframes(int(self.chunk))
                        nextpos=self.wf.tell()
                        self.wf.setpos(currentpos)
                        #if info.Quickness/info.r12 != 1 and len(data)!=0:
                        if (info.Quickness!=1 or info.r12 != 1) and len(data)!=0:
                            data = np.frombuffer(data,dtype="int16")
                            data=data.astype(np.float64)
                            #print("Key=",info.Key,"   Quickness=",info.Quickness,"で変換")
                            if info.Key!=0:
                                data = librosa.effects.pitch_shift(data,self.wf.getframerate(),info.Key)
                            #data = librosa.effects.time_stretch(data,info.r12/info.Quickness)#/info.r12)
                            if info.Quickness!=1:
                                data = librosa.effects.time_stretch(data,info.Quickness)
                            data = data.astype(np.int16)
                            data = np.ndarray.tobytes(data)
                        size=1024
                        if currentpos+(self.chunk)<info.last:
                            for i in range(int(len(data)/(size*4))+1):
                                #print(i,end='')
                                if info.quit:
                                    break
                                if info.renew_flag:
                                    self.renew()
                                    info.renew_flag=False
                                    self.wf.setpos(self.wf.tell())
                                    if info.stop_flag:
                                        self.stream.stop_stream()
                                    break
                                if msvcrt.kbhit():
                                    backgroundprocess(msvcrt.getch())
                                if i<int(len(data)/(size*4)):
                                    dummy=self.wf.readframes(size)
                                    if self.stream.is_active():
                                        self.stream.write(data[(size*4)*i:(size*4)*(i+1)])
                                else:
                                    self.wf.setpos(nextpos)
                                    if self.stream.is_active():
                                        self.stream.write(data[(size*4)*i:])
                        else:
                            lastdataindex=0
                            while True:
                                if (size*4)*(lastdataindex+1)<info.last:
                                    dummy=self.wf.readframes(size)
                                    if self.stream.is_active():
                                        self.stream.write(data[(size*4)*lastdataindex:(size*4)*(lastdataindex+1)])
                                else:
                                    if self.stream.is_active():
                                        self.stream.write(data[(size*4)*lastdataindex:])
                                    self.wf.setpos(info.last)
                                    break
                                lastdataindex+=1
                    else:
                        if info.stop_flag ==False:
                            self.stream.start_stream()
                        else:
                            time.sleep(0.1)
            print("done.")
            self.stream.close()
            self.p.terminate()

        def renew(self):#レート更新
                self.speed=info.r12
                self.stream = self.p.open(
                    format = self.p.get_format_from_width(self.wf.getsampwidth()),
                    channels = self.wf.getnchannels(),
                    frames_per_buffer = self.buffer,
                    #frames_per_buffer = self.chunk,
                    #rate = int(self.wf.getframerate()*self.speed),
                    rate = int(self.wf.getframerate()),
                    output = True)
def backgroundprocess(kb):
    if isinstance(kb,int):#playlistの曲のボタンが押されたとき
        info.next_play_index=kb
        info.back_flag=False
        info.quit=True
    elif kb==b'\xe0':
        kb=msvcrt.getch()
        if kb==b'K':#Left
            if info.Quickness<=0.1:
                messagebox.showinfo('エラー', 'これ以上は速度を落とせません')
                #print("これ以上は速度を落とせません")
            else:
                info.Quickness-=0.1
                info.speed_label.grid_forget()
                info.speed_label=tk.Label(info.root, text="Speed="+str(round(info.Quickness,3)),font=("",20))
                info.speed_label.grid(row=5,column=1, sticky="e")
                print("Speed=",round(info.Quickness,3))
        elif kb==b'H':#Up
            info.Key+=0.1
            info.r12=r**np.float(info.Key)
            info.pitch_label.grid_forget()
            info.pitch_label=tk.Label(info.root, text="Pitch="+str(round(info.Key,2)),font=("",20))
            info.pitch_label.grid(row=5,column=0, sticky="e")
            info.renew_flag=True
            print("Key=",round(info.Key,2))
        elif kb==b'M':#Right
            info.Quickness+=0.1
            info.speed_label.grid_forget()
            info.speed_label=tk.Label(info.root, text="Speed="+str(round(info.Quickness,3)),font=("",20))
            info.speed_label.grid(row=5,column=1, sticky="e")
            print("Speed=",round(info.Quickness,3))
        elif kb==b'P':#Down
            info.Key-=0.1
            info.r12=r**np.float(info.Key)
            info.pitch_label.grid_forget()
            info.pitch_label=tk.Label(info.root, text="Pitch="+str(round(info.Key,2)),font=("",20))
            info.pitch_label.grid(row=5,column=0, sticky="e")
            info.renew_flag=True
            print("Key=",round(info.Key,2))
    elif kb.decode()=='\r':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            if info.song.stream.is_active():
                messagebox.showinfo('一時停止', '一時停止します')
                #print("一時停止します")
                info.stop_flag=True
                info.song.stream.stop_stream()
            else:
                messagebox.showinfo('再開', '再開します')
                #print("再開します")
                info.stop_flag=False
                info.song.stream.start_stream()
            info.renew_flag=True
            time.sleep(0.2)
    elif kb.decode()=='n':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            print("next")
            info.back_flag=False
            info.shuffle_flag=False
            info.directory_repeat_flag=False
            info.one_repeat_flag=False
            info.quit=True
    elif kb.decode()=='p':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            print("最初から")
            info.song.wf.rewind()
        info.renew_flag=True
    elif kb.decode()=='b':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            info.back_flag=True
            info.shuffle_flag=False
            info.directory_repeat_flag=False
            info.one_repeat_flag=False
            info.quit=True
    elif kb.decode()=='h':
        help()
    elif kb.decode()=='g':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            if (info.song.wf.tell()+(info.onesecframes*10))>info.last:
                info.song.wf.setpos(info.last-1)
            else:
                info.song.wf.setpos(info.song.wf.tell()+int(info.onesecframes*10))
            info.renew_flag=True
    elif kb.decode()=='f':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            if (info.song.wf.tell()+(info.onesecframes*3))>info.last:
                info.song.wf.setpos(info.last-1)
            else:
                info.song.wf.setpos(info.song.wf.tell()+int(info.onesecframes*3))
            info.renew_flag=True
    elif kb.decode()=='d':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            if (info.song.wf.tell()-(info.onesecframes*3))<info.head:
                info.song.wf.setpos(info.head)
            else:
                info.song.wf.setpos(info.song.wf.tell()-int(info.onesecframes*3))
            info.renew_flag=True
    elif kb.decode()=='s':
        if info.thread_play is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
            #print("音楽を開始してください")
        else:
            if (info.song.wf.tell()-(info.onesecframes*10))<info.head:
                info.song.wf.setpos(info.head)
            else:
                info.song.wf.setpos(info.song.wf.tell()-int(info.onesecframes*10))
            info.renew_flag=True
    elif kb.decode()=='e':
        info.Key=0
        info.r12=1
        info.pitch_label.grid_forget()
        info.pitch_label=tk.Label(info.root, text="Pitch="+str(round(info.Key,2)),font=("",20))
        info.pitch_label.grid(row=5,column=0, sticky="e")
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb.decode()=='r':
        info.Quickness=1
        info.speed_label.grid_forget()
        info.speed_label=tk.Label(info.root, text="Speed="+str(round(info.Quickness,3)),font=("",20))
        info.speed_label.grid(row=5,column=1, sticky="e")
        print("Speed=",round(info.Quickness,3))
    elif kb.decode()=='q':
        info.next_play_index=info.playlist_len+1
        info.back_flag=False
        info.quit=True
    elif kb.decode()=='z':
        print("シャッフル再生")
        info.back_flag=False
        info.shuffle_flag=True
        info.directory_repeat_flag=False
        info.one_repeat_flag=False
    elif kb.decode()=='x':
        print("フォルダリピート")
        info.back_flag=False
        info.shuffle_flag=False
        info.directory_repeat_flag=True
        info.one_repeat_flag=False
    elif kb.decode()=='c':
        print("1曲リピート")
        info.back_flag=False
        info.shuffle_flag=False
        info.directory_repeat_flag=False
        info.one_repeat_flag=True
    elif kb.decode()=='v':
        print("ノーマル再生")
        info.back_flag=False
        info.shuffle_flag=False
        info.directory_repeat_flag=False
        info.one_repeat_flag=False
    elif kb==b'left':#Left
        if round(info.Quickness,2)==0.1:
            messagebox.showinfo('エラー', 'これ以上は速度を落とせません')
            #print("これ以上は速度を落とせません")
        else:
            info.Quickness-=0.1
            info.speed_label.grid_forget()
            info.speed_label=tk.Label(info.root, text="Speed="+str(round(info.Quickness,3)),font=("",20))
            info.speed_label.grid(row=5,column=1, sticky="e")
            print("Speed=",round(info.Quickness,3))
    elif kb==b'left_little':#Left
        if round(info.Quickness,2)==0.01:
            messagebox.showinfo('エラー', 'これ以上は速度を落とせません')
            #print("これ以上は速度を落とせません")
        else:
            info.Quickness-=0.01
            info.speed_label.grid_forget()
            info.speed_label=tk.Label(info.root, text="Speed="+str(round(info.Quickness,3)),font=("",20))
            info.speed_label.grid(row=5,column=1, sticky="e")
            print("Speed=",round(info.Quickness,3))
    elif kb==b'up':#Up
        info.Key+=0.1
        info.r12=r**np.float(info.Key)
        info.pitch_label.grid_forget()
        info.pitch_label=tk.Label(info.root, text="Pitch="+str(round(info.Key,2)),font=("",20))
        info.pitch_label.grid(row=5,column=0, sticky="e")
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb==b'up_much':#Up
        info.Key+=1.0
        info.r12=r**np.float(info.Key)
        info.pitch_label.grid_forget()
        info.pitch_label=tk.Label(info.root, text="Pitch="+str(round(info.Key,2)),font=("",20))
        info.pitch_label.grid(row=5,column=0, sticky="e")
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb==b'right':#Right
        info.Quickness+=0.1
        info.speed_label.grid_forget()
        info.speed_label=tk.Label(info.root, text="Speed="+str(round(info.Quickness,3)),font=("",20))
        info.speed_label.grid(row=5,column=1, sticky="e")
        print("Speed=",round(info.Quickness,3))
    elif kb==b'right_little':#Right
        info.Quickness+=0.01
        info.speed_label.grid_forget()
        info.speed_label=tk.Label(info.root, text="Speed="+str(round(info.Quickness,3)),font=("",20))
        info.speed_label.grid(row=5,column=1, sticky="e")
        print("Speed=",round(info.Quickness,3))
    elif kb==b'down':#Down
        info.Key-=0.1
        info.r12=r**np.float(info.Key)
        info.pitch_label.grid_forget()
        info.pitch_label=tk.Label(info.root, text="Pitch="+str(round(info.Key,2)),font=("",20))
        info.pitch_label.grid(row=5,column=0, sticky="e")
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb==b'down_much':#Down
        info.Key-=1.0
        info.r12=r**np.float(info.Key)
        info.pitch_label.grid_forget()
        info.pitch_label=tk.Label(info.root, text="Pitch="+str(round(info.Key,2)),font=("",20))
        info.pitch_label.grid(row=5,column=0, sticky="e")
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))

def playback(filename):
    info.song = AudioFile(filename,info.r12)
    try:
        info.song.play()
    except KeyboardInterrupt:
        info.song.stream.close()
        info.song.p.terminate()
        messagebox.showinfo('強制終了', '強制終了します')
        #print("強制終了します")
        sys.exit()
class WinodwClass(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        master.title("音楽再生アプリ") #タイトル作成
        #master.protocol('WM_DELETE_WINDOW', (lambda:master.quit() if info.thread_play is None else print("再生を終了させてください")))

        tk.Button(master, text="pitch-1", fg = "red",command=partial(backgroundprocess,b'down_much'),font=("",20)).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(master, text="pitch-0.1", fg = "red",command=partial(backgroundprocess,b'down'),font=("",20)).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(master, text="pitch+0.1", fg = "red",
        command=partial(backgroundprocess,b'up'),font=("",20)).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(master, text="pitch+1", fg = "red",command=partial(backgroundprocess,b'up_much'),font=("",20)).grid(row=0, column=0, padx=10, pady=10)
        info.pitch_label=tk.Label(master, text="Pitch="+str(round(info.Key,2)),font=("",20))
        info.pitch_label.grid(row=5,column=0, sticky="e")
        tk.Button(master, text="pitch_reset", fg = "red",command=partial(backgroundprocess,b'e'),font=("",20)).grid(row=2, column=0, padx=10, pady=10)

        tk.Button(master, text="speed+10%", fg = "blue",command=partial(backgroundprocess,b'right'),font=("",20)).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(master, text="speed+1%", fg = "blue",command=partial(backgroundprocess,b'right_little'),font=("",20)).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(master, text="speed-1%", fg = "blue",command=partial(backgroundprocess,b'left_little'),font=("",20)).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(master, text="speed-10%", fg = "blue",command=partial(backgroundprocess,b'left'),font=("",20)).grid(row=4, column=1, padx=10, pady=10)
        info.speed_label=tk.Label(master, text="Speed="+str(round(info.Quickness,3)),font=("",20))
        info.speed_label.grid(row=5,column=1, sticky="e")
        tk.Button(master, text="speed_reset", fg = "blue",command=partial(backgroundprocess,b'r'),font=("",20)).grid(row=2, column=1, padx=10, pady=10)

        tk.Button(master, text="back_10sec", fg = "green",command=partial(backgroundprocess,b's'),font=("",20)).grid(row=3, column=2, padx=10, pady=10)
        tk.Button(master, text="back_3sec", fg = "green",command=partial(backgroundprocess,b'd'),font=("",20)).grid(row=2, column=2, padx=10, pady=10)
        tk.Button(master, text="forward_3sec", fg = "green",command=partial(backgroundprocess,b'f'),font=("",20)).grid(row=1, column=2, padx=10, pady=10)
        tk.Button(master, text="forward_10sec", fg = "green",command=partial(backgroundprocess,b'g'),font=("",20)).grid(row=0, column=2, padx=10, pady=10)

        tk.Button(master, text="restart", fg = "deep pink",command=partial(backgroundprocess,b'p'),font=("",20)).grid(row=5, column=2, padx=10, pady=10)
        tk.Button(master, text="playlist終了", fg = "deep pink",command=partial(backgroundprocess,b'q'),font=("",20)).grid(row=5, column=3, padx=10, pady=10)
        tk.Button(master, text="back", fg = "orange",command=partial(backgroundprocess,b'b'),font=("",20)).grid(row=4, column=2, padx=10, pady=10)
        tk.Button(master, text="next", fg = "orange",command=partial(backgroundprocess,b'n'),font=("",20)).grid(row=4, column=3, padx=10, pady=10)

        tk.Button(master, text="再生", fg = "navy",command=start_playthread,font=("",20)).grid(row=6, column=1, padx=10, pady=10)
        info.playtimeframe = tk.LabelFrame(master, text="再生時間",font=("",20))
        info.playtimeframe.grid(row=6, padx=10, pady=10)
        info.label=tk.Label(info.playtimeframe, text='--s/--s',font=("",20))
        info.label.pack()
        getplaytime(master)
        tk.Button(master, text="プログラム終了", fg = "deep pink",command=lambda: master.destroy() if info.thread_play is None else messagebox.showinfo('エラー', 'PlayListを終了させてください'),font=("",20)).grid(row=6, column=3, padx=10, pady=10)
        tk.Button(master, text="一時停止/再開", fg = "navy",command=partial(backgroundprocess,b'\r'),font=("",20)).grid(row=6, column=2, padx=10, pady=10)

        tk.Button(master, text="ノーマル再生", fg = "purple",command=partial(backgroundprocess,b'v'),font=("",20)).grid(row=0, column=3, padx=10, pady=10)
        tk.Button(master, text="シャッフル", fg = "purple",command=partial(backgroundprocess,b'z'),font=("",20)).grid(row=1, column=3, padx=10, pady=10)
        tk.Button(master, text="フォルダリピート", fg = "purple",command=partial(backgroundprocess,b'x'),font=("",20)).grid(row=2, column=3, padx=10, pady=10)
        tk.Button(master, text="1曲リピート", fg = "purple",command=partial(backgroundprocess,b'c'),font=("",20)).grid(row=3, column=3, padx=10, pady=10)

def window():
    info.root = Tk()
    info.root.configure(bg='gold')
    rootA = WinodwClass(master = info.root)
    rootA.mainloop()

def getplaytime(root):
    if (info.thread_play is not None) and (info.head is not None):
        info.label.pack_forget()
        info.label=tk.Label(info.playtimeframe, text=str('{:.2f}'.format((info.song.wf.tell()-info.head)/(info.last-info.head)*info.duration))+"s/"+str('{:.2f}'.format(info.duration))+"s",font=("",20))
        info.label.pack()
    root.after(100,getplaytime,root)

class WindowThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        window()
        print("終了")
        sys.exit()
class PlayListTkinterClass(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        master.title("Playlistの選択")
        master.protocol('WM_DELETE_WINDOW', (lambda:master.quit()))

        frame0 = ttk.Frame(master, padding=10)
        frame0.grid(row=0, column=1, sticky=E)

        IDirLabel = ttk.Label(frame0, text="パス指定＞＞", padding=(5, 2))
        IDirLabel.pack(side=LEFT)
        info.targetname_0 = ttk.Entry(frame0,width=50)
        info.targetname_0.insert(tk.END, u'パスを入力(カレントディレクトリ内なら./,それ以外なら相対パス)') # 最初から文字を入れておく
        info.targetname_0.pack(side=LEFT)
        current=ttk.Button(frame0, width=10, text="カレント",
                            command=setcurrent)
        current.pack(side=LEFT)
        btnRead0=ttk.Button(frame0, width=10, text="再生",
                            command=lambda:getTextInput(master))
        btnRead0.pack(side=LEFT)

        # Frame1の作成
        frame1 = ttk.Frame(master, padding=10)
        frame1.grid(row=2, column=1, sticky=E)

        # 「フォルダ参照」ラベルの作成
        IDirLabel = ttk.Label(frame1, text="フォルダ参照＞＞", padding=(5, 2))
        IDirLabel.pack(side=LEFT)

        # 「フォルダ参照」エントリーの作成
        info.targetname_1 = ttk.Entry(frame1,width=50)
        info.targetname_1.insert(tk.END, u'フォルダ参照')
        info.targetname_1.pack(side=LEFT)

        # 「フォルダ参照」ボタンの作成
        IDirButton = ttk.Button(frame1, text="参照", command=dirdialog_clicked)
        IDirButton.pack(side=LEFT)
        btnRead1=ttk.Button(frame1, width=10, text="再生",
                            command=lambda:dir_play(master))
        btnRead1.pack(side=LEFT)

        # Frame2の作成
        frame2 = ttk.Frame(master, padding=10)
        frame2.grid(row=4, column=1, sticky=E)

        # 「ファイル参照」ラベルの作成
        IFileLabel = ttk.Label(frame2, text="ファイル参照＞＞", padding=(5, 2))
        IFileLabel.pack(side=LEFT)


        # 「ファイル参照」エントリーの作成
        info.targetname_2 = ttk.Entry(frame2,width=50)
        info.targetname_2.insert(tk.END, u'ファイル参照')
        info.targetname_2.pack(side=LEFT)

        # 「ファイル参照」ボタンの作成
        IFileButton = ttk.Button(frame2, text="参照", command=filedialog_clicked)
        IFileButton.pack(side=LEFT)
        btnRead2=ttk.Button(frame2, width=10, text="再生",
                            command=lambda:file_play(master))
        btnRead2.pack(side=LEFT)

        # Frame3の作成
        frame3 = ttk.Frame(master, padding=10)
        frame3.grid(row=7,column=1,sticky=W)

class PlayListTkinterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        PlayListTkintertk = Tk()
        PlayListTkinter=PlayListTkinterClass(master=PlayListTkintertk)
        PlayListTkinter.mainloop()
class PlayThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        info.mode=-1
        info.back_flag=False
        info.shuffle_flag,info.directory_repeat_flag,info.one_repeat_flag=False,False,False
        info.next_play_index=0
        os.chdir(info.basedirname)
        playlist_label=[]
        playlistframe=None
        playlist=[]
        print("再生を開始します")
        print("")
        try:
            print("Playlistの選択")
            PlayListTkintertk = Tk()
            PlayListTkinter=PlayListTkinterClass(master=PlayListTkintertk)
            PlayListTkinter.mainloop()
            if info.mode==0:
                if info.targetname_0.get()=='./':
                    os.chdir(info.basedirname)
                    info.root.title("音楽再生アプリ("+info.basedirname+")")
                else:
                    if info.targetname_0.get != '':
                        os.chdir(info.targetname_0.get())
                        info.root.title("音楽再生アプリ("+info.targetname_0.get()+")")
            elif info.mode==1:
                if info.targetname_1.get != '' :
                    os.chdir(info.targetname_1.get())
                    info.root.title("音楽再生アプリ("+info.targetname_1.get()+")")
            elif info.mode==2:
                if info.targetname_2.get != '':
                    playfile=info.targetname_2.get()
                    print("playfile=",playfile)
                    info.root.title("音楽再生アプリ("+info.targetname_2.get()+")")
            else:
                print("×が押されました")
                info.thread_play=None
                return
        except:
            messagebox.showinfo('エラー', '何らかのエラーが発生しました(これを見たときは至急私まで)')
            #print("何らかのエラーが発生しました")
            #print(e)
        else:
            if info.mode==2:
                playlistdirname=""
                playlistdirname="PythonMusicApp_Playlist_"+os.path.splitext(os.path.basename(playfile))[0].replace(' ','').replace('&','').replace('.','')
                if os.path.exists(playlistdirname) and os.path.isdir(playlistdirname):
                    print(playlistdirname,"フォルダを発見しました")
                else:
                    print("PlayListフォルダを作ります")
                    os.mkdir(playlistdirname)
                    print("ターゲットファイルをコピーします")
                    shutil.copyfile(playfile,playlistdirname+"/" + os.path.split(playfile)[1])
                os.chdir(playlistdirname)

            print("ファイル名のエスケープ処理を行います")
            for f in glob.glob("./*"):
                if (os.path.splitext(f)[1]=='.wav' or os.path.splitext(f)[1]=='.mp3' or os.path.splitext(f)[1]=='.m4a' or os.path.splitext(f)[1]=='.mp4'):
                    if ' ' in os.path.split(f)[1]:
                        print("空白があるから空白を除去したファイル名にします")
                        os.rename(os.path.split(f)[1],os.path.split(f)[1].replace(' ',''))
                        f=os.path.split(f)[1].replace(' ','')
                    if '&' in os.path.split(f)[1]:
                        print("&があるから空白を除去したファイル名にします")
                        os.rename(os.path.split(f)[1],os.path.split(f)[1].replace('&',''))
                        f=os.path.split(f)[1].replace('&','')
                    if '.' in os.path.splitext(os.path.basename(f))[0]:
                        print(".があるから空白を除去したファイル名にします")
                        os.rename(os.path.split(f)[1],os.path.splitext(os.path.basename(f))[0].replace('.','')+os.path.splitext(f)[1])
            print("エスケープ処理完了！")
            print("")
            playlistdirname=""
            playlistdirname="PythonMusicApp_Playlist"
            if os.path.exists(playlistdirname) and os.path.isdir(playlistdirname):
                print(playlistdirname,"フォルダを発見しました")
                print(" ファイルをチェックします")
                for f in glob.glob("./*"):
                    if (os.path.splitext(f)[1]=='.wav' or os.path.splitext(f)[1]=='.mp3' or os.path.splitext(f)[1]=='.m4a' or os.path.splitext(f)[1]=='.mp4') and os.path.isfile(os.path.split(f)[1]):
                        if os.path.exists(playlistdirname + "/" + os.path.splitext(f)[0].replace(' ','')+".wav"):
                            print(os.path.splitext(f)[0].replace(' ','')+".wavはあります")
                        else:
                            print(os.path.split(f)[1],"をwav形式でplaylistに追加します")
                            if os.path.splitext(f)[1]=='.wav':
                                print(os.path.split(f)[1])
                                shutil.copyfile(os.path.split(f)[1],playlistdirname+"/" + os.path.split(f)[1])
                            elif os.path.splitext(f)[1]=='.mp3':
                                print(os.path.split(f)[1],'→',end='')
                                if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                                    print("wavが既にあるため変換しません")
                                else:
                                    print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                                    sound = pydub.AudioSegment.from_mp3(os.path.split(f)[1].replace(' ',''))
                                    sound.export(playlistdirname+"/"+os.path.splitext(f)[0].replace(' ','')+".wav", format="wav")
                            elif os.path.splitext(f)[1]=='.m4a':
                                print(os.path.split(f)[1],'→',end='')
                                if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                                    print("wavが既にあるため変換しません")
                                else:
                                    print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                                    os.system("ffmpeg -i "+ os.path.split(f)[1].replace(' ','') + " " + playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                            elif os.path.splitext(f)[1]=='.mp4':
                                print(os.path.split(f)[1],'→',end='')
                                if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                                    print("wavが既にあるため変換しません")
                                else:
                                    print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                                    os.system("ffmpeg -i "+ os.path.split(f)[1].replace(' ','') + " " +  playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                print("ファイルチェック完了!")
            else:
                print("PlayListフォルダを作ります")
                os.mkdir(playlistdirname)
                print("対象のファイルをwavへ変換します")
                for f in glob.glob("./*"):
                    if os.path.splitext(f)[1]=='.wav':
                        print(os.path.split(f)[1])
                        shutil.copyfile(os.path.split(f)[1],playlistdirname+"/" + os.path.split(f)[1])
                    elif os.path.splitext(f)[1]=='.mp3':
                        print(os.path.split(f)[1],'→',end='')
                        if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                            print("wavが既にあるため変換しません")
                        else:
                            print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                            sound = pydub.AudioSegment.from_mp3(os.path.split(f)[1].replace(' ',''))
                            sound.export(playlistdirname+"/"+os.path.splitext(f)[0].replace(' ','')+".wav", format="wav")
                    elif os.path.splitext(f)[1]=='.m4a':
                        print(os.path.split(f)[1],'→',end='')
                        if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                            print("wavが既にあるため変換しません")
                        else:
                            print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                            os.system("ffmpeg -i "+ os.path.split(f)[1].replace(' ','') + " " + playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                    elif os.path.splitext(f)[1]=='.mp4':
                        print(os.path.split(f)[1],'→',end='')
                        if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                            print("wavが既にあるため変換しません")
                        else:
                            print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                            os.system("ffmpeg -i "+ os.path.split(f)[1].replace(' ','') + " " +  playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                print("変換完了！")
            print("")
            print("playlistを作成します")
            os.chdir(playlistdirname)
            if len(playlist)!=0:
                 playlistframe.grid_forget()
            playlist=[]
            for f in glob.glob("./*"):
                if os.path.splitext(f)[1]=='.wav':
                    print(os.path.split(f)[1])
                    playlist.append(os.path.split(f)[1])
            print("playlist作成完了！")
            print("")
            print("playlist=",playlist)
            index=0
            info.playlist_len=len(playlist)
            if info.playlist_len==0:
                print("playlistの曲がありません")
                info.thread_play=None
                return
            # Canvas Widget を生成
            canvas = tk.Canvas(info.root)
            # Frame Widgetを 生成
            playlistframe = tk.Frame(canvas)
            # Scrollbar を生成して配置
            bar_ver = tk.Scrollbar(info.root, orient=tk.VERTICAL)
            bar_ver.grid(row=1, column=5,rowspan=5, padx=10, pady=10,sticky="NS")
            bar_ver.config(command=canvas.yview)

            # Canvas Widget を配置
            canvas.config(yscrollcommand=bar_ver.set)
            canvas.config(scrollregion=(0,0,400,27*info.playlist_len)) #スクロール範囲
            canvas.grid(row=1, column=4, rowspan=5,padx=10, pady=10,sticky="WES")

            # Frame Widgetを Canvas Widget上に配置
            canvas.create_window((0,0), window=playlistframe, anchor=tk.NW, width=canvas.cget('width'))

            for i, target in enumerate(playlist):
                plbtn=tk.Button(playlistframe, text=str(i+1)+":"+target, command=partial(backgroundprocess,i+1))
                playlist_label.append(plbtn)
                plbtn.pack(fill=tk.X)
            while True:
                print(index+1,"番目の",playlist[index],"を再生")
                playback(playlist[index])
                if info.next_play_index!=0:
                    index=info.next_play_index-1
                    info.next_play_index=0
                elif info.back_flag:
                    if index>=1:
                        index-=1
                    else:
                        print("最初の曲です")
                    info.back_flag=False
                elif info.one_repeat_flag:
                    pass
                elif info.shuffle_flag:
                    index=random.randint(0,info.playlist_len-1)
                else:
                    if index==info.playlist_len-1:
                        print("最後の曲です")
                    index+=1
                if index ==info.playlist_len and info.directory_repeat_flag:
                    index=0
                if index==info.playlist_len:
                    break
        print("Playlistが終了しました")
        info.thread_play=None

def start_windowthread():
    thread_window=WindowThread()
    thread_window.start()

def start_playthread():
    if info.thread_play is None:
        info.thread_play=PlayThread()
        info.thread_play.start()
    else:
        messagebox.showinfo('エラー', '既に再生しています')
        #print("既に再生しています")
class KeySpeedInputClass(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        master.title("KeyとSpeedの入力")

        KeySpeedLabel = ttk.Label(master, text="KeyとSpeedを入力(後から変更できます)", padding=(5, 2))
        KeySpeedLabel.grid(row=0, column=0, sticky=E)
        Keyframe = ttk.Frame(master, padding=10)
        Keyframe.grid(row=1, column=0, sticky=E)
        KeyInputLabel = ttk.Label(Keyframe, text="Key=", padding=(5, 2))
        KeyInputLabel.pack(side=LEFT)
        KeyInput = tk.Entry(Keyframe,width=50)                   # widthプロパティで大きさを変える
        KeyInput.insert(tk.END, u'Keyを入力')        # 最初から文字を入れておく
        KeyInput.pack(side=LEFT)

        Speedframe = ttk.Frame(master, padding=10)
        Speedframe.grid(row=2, column=0, sticky=E)
        SpeedInputLabel = ttk.Label(Speedframe, text="Speed=", padding=(5, 2))
        SpeedInputLabel.pack(side=LEFT)
        SpeedInput = tk.Entry(Speedframe,width=50)                   # widthプロパティで大きさを変える
        SpeedInput.insert(tk.END, u'Speedを入力')        # 最初から文字を入れておく
        SpeedInput.pack(side=LEFT)
        btnRead=tk.Button(master, height=1, width=10, text="OK",
                            command=lambda:KeySpeedRead(master,KeyInput,SpeedInput))
        btnRead.grid(row=3, column=1, sticky=E)
        NormalPlay=tk.Button(master, height=1, width=10, text="標準再生",
                            command=lambda:NormalPlay_Set(KeyInput,SpeedInput))
        NormalPlay.grid(row=3, column=0)

if __name__ == "__main__":
    KeySpeedInputtk = Tk()
    KeySpeedInput=KeySpeedInputClass(master=KeySpeedInputtk)
    KeySpeedInput.mainloop()
    info.Key=round(info.Key,1)
    info.Quickness=round(info.Quickness,2)
    info.basedirname=os.path.dirname(os.path.abspath("__file__"))
    help()
    r = 2**(1/12)
    info.r12=(2**(1/12))**np.float(info.Key)
    start_windowthread()
