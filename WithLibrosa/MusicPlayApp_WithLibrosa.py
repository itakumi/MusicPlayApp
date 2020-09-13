from MusicPlayApp_Interface_WithLibrosa import *
import librosa
info=AudioInformation()

def dirdialog_clicked(PlayListTkinter):#フォルダ参照
    PlayListTkinter.attributes("-topmost", False)
    iDir = os.path.abspath(os.path.dirname("__file__")+"../")
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    if iDirPath !='':
        info.targetname_0.delete(0,tkinter.END)
        info.targetname_2.delete(0,tkinter.END)
        info.targetname_1.delete(0,tkinter.END)
        info.targetname_1.insert(tkinter.END,iDirPath)
    PlayListTkinter.attributes("-topmost", True)
def dir_play(PlayListTkinter):#フォルダ再生
    if os.path.isdir(info.targetname_1.get()):
        info.mode=1
        info.targetname_0_str=None
        info.targetname_1_str=info.targetname_1.get()
        info.targetname_2_str=None
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')
def filedialog_clicked(PlayListTkinter):#ファイル参照
    PlayListTkinter.attributes("-topmost", False)
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname("__file__")+"../")
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    if iFilePath != '':
        info.targetname_0.delete(0,tkinter.END)
        info.targetname_1.delete(0,tkinter.END)
        info.targetname_2.delete(0,tkinter.END)
        info.targetname_2.insert(tkinter.END,iFilePath)
    PlayListTkinter.attributes("-topmost", True)
def file_play(PlayListTkinter):#ファイル再生
    if os.path.isfile(info.targetname_2.get()):
        info.mode=2
        info.targetname_0_str=None
        info.targetname_1_str=None
        info.targetname_2_str=info.targetname_2.get()
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')
def getTextInput(PlayListTkinter):#パス指定再生
    if info.targetname_0.get()=='./' or os.path.isdir(info.targetname_0.get()):
        info.mode=0
        info.targetname_0_str=info.targetname_0.get()
        info.targetname_1_str=None
        info.targetname_2_str=None
        PlayListTkinter.quit()
    elif os.path.isfile(info.targetname_0.get()):
        info.mode=2
        info.targetname_2.delete(0,tkinter.END)
        info.targetname_2.insert(tkinter.END,info.targetname_0.get())
        info.targetname_0.delete(0,tkinter.END)
        info.targetname_1.delete(0,tkinter.END)
        time.sleep(0.5)
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')
def setcurrent():#カレントセット
    info.targetname_1.delete(0,tkinter.END)
    info.targetname_2.delete(0,tkinter.END)
    info.targetname_0.delete(0,tkinter.END)
    info.targetname_0.insert(tkinter.END,info.basedirname)

def KeySpeedRead(KeySpeedInput,KeyInput,SpeedInput):#最初のウィンドウにおいてキーと速度を読み込み時
    if KeyInput.get().replace(',', '').replace('.', '').replace('-', '').isnumeric() and SpeedInput.get().replace(',', '').replace('.', '').replace('-', '').isnumeric():
        try:
            round(float(KeyInput.get()),2)
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
    else:
        messagebox.showinfo('エラー', 'KeyとSpeedはfloat型でお願いします')
def OutputDeviceRead(outputdeviceInputClass,var):
    info.outputdeviceindex=var.get()
    outputdeviceInputClass.destroy()

class AudioFile:
        chunk_mul=128
        chunk = 1024*chunk_mul
        buffer=1024*32
        #chunk = 44100*3
        #buffer=44100
        def __init__(self, file, speed):
           """ Init audio stream """
           self.wf = wave.open(file, 'rb')
           self.speed = speed
           self.p = pyaudio.PyAudio()
           self.stream = self.p.open(
               format = self.p.get_format_from_width(self.wf.getsampwidth()),
               channels = self.wf.getnchannels(),
               frames_per_buffer = self.buffer,
               rate = int(self.wf.getframerate()),
               output_device_index=info.outputdeviceindex,
               input=False,
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
                    backgroundprocess(msvcrt.getch(),'')
                else:
                    if self.stream.is_active():
                        currentpos=self.wf.tell()
                        data = self.wf.readframes(int(self.chunk))
                        nextpos=self.wf.tell()
                        self.wf.setpos(currentpos)
                        if len(data)!=0:
                            data = np.frombuffer(data,dtype="int16")
                            data=data.astype(np.float64)
                            if info.Key!=0:
                                data = librosa.effects.pitch_shift(data,self.wf.getframerate(),info.Key)
                            #data = librosa.effects.time_stretch(data,info.r12/info.Quickness)#/info.r12)
                            if info.Quickness!=1:
                                data = librosa.effects.time_stretch(data,info.Quickness)
                            data*=round(float(info.volume),2)/100
                            data = data.astype(np.int16)
                            data = np.ndarray.tobytes(data)
                        #data*=info.volume
                        size=1024
                        if currentpos+(self.chunk)<info.last:
                            for i in range(int(len(data)/(size*4))+1):
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
                                    backgroundprocess(msvcrt.getch(),'')
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
                    rate = int(self.wf.getframerate()),
                    output_device_index=info.outputdeviceindex,
                    input=False,
                    output = True)
def backgroundprocess(kb,scaleint=None,shuffle_button=None,directory_repeat_button=None,one_repeat_button=None,windowroot=None):
    if isinstance(kb,int):#playlistの曲のボタンが押されたとき
        info.next_play_index=kb
        info.back_flag=False
        info.quit=True
    elif isinstance(kb,float):
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            info.song.wf.setpos(int(info.head+info.onesecframes*float(scaleint)))
            info.renew_flag=True
    elif kb==b'\xe0':
        kb=msvcrt.getch()
        if kb==b'K':#Left
            if info.Quickness<=0.1:
                messagebox.showinfo('エラー', 'これ以上は速度を落とせません')
            else:
                info.Quickness-=0.1
                info.speed_entry.delete(0,tkinter.END)
                info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
                print("Speed=",round(info.Quickness,3))
        elif kb==b'H':#Up
            info.Key+=0.1
            info.r12=r**np.float(info.Key)
            info.pitch_entry.delete(0,tkinter.END)
            info.pitch_entry.insert(tkinter.END,round(info.Key,2))
            info.renew_flag=True
            print("Key=",round(info.Key,2))
        elif kb==b'M':#Right
            info.Quickness+=0.1
            info.speed_entry.delete(0,tkinter.END)
            info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
            print("Speed=",round(info.Quickness,3))
        elif kb==b'P':#Down
            info.Key-=0.1
            info.r12=r**np.float(info.Key)
            info.pitch_entry.delete(0,tkinter.END)
            info.pitch_entry.insert(tkinter.END,round(info.Key,2))
            info.renew_flag=True
            print("Key=",round(info.Key,2))
    elif kb.decode()=='\r':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            if info.song.stream.is_active():
                messagebox.showinfo('一時停止', '一時停止します')
                info.stop_flag=True
                info.song.stream.stop_stream()
            else:
                messagebox.showinfo('再開', '再開します')
                info.stop_flag=False
                info.song.stream.start_stream()
            info.renew_flag=True
            time.sleep(0.2)
    elif kb.decode()=='n':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            print("next")
            info.back_flag=False
            info.quit=True
    elif kb.decode()=='p':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            print("最初から")
            info.song.wf.rewind()
        info.renew_flag=True
    elif kb.decode()=='b':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            info.back_flag=True
            info.shuffle_flag=False
            info.directory_repeat_flag=False
            info.one_repeat_flag=False
            shuffle_button['bg']='SystemButtonFace'
            directory_repeat_button['bg']='SystemButtonFace'
            one_repeat_button['bg']='SystemButtonFace'
            info.quit=True
    elif kb.decode()=='h':
        help()
    elif kb.decode()=='g':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            if (info.song.wf.tell()+(info.onesecframes*10))>info.last:
                info.song.wf.setpos(info.last-1)
            else:
                info.song.wf.setpos(info.song.wf.tell()+int(info.onesecframes*10))
            info.renew_flag=True
    elif kb.decode()=='f':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            if (info.song.wf.tell()+(info.onesecframes*5))>info.last:
                info.song.wf.setpos(info.last-1)
            else:
                info.song.wf.setpos(info.song.wf.tell()+int(info.onesecframes*5))
            info.renew_flag=True
    elif kb.decode()=='d':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            if (info.song.wf.tell()-(info.onesecframes*5))<info.head:
                info.song.wf.setpos(info.head)
            else:
                info.song.wf.setpos(info.song.wf.tell()-int(info.onesecframes*5))
            info.renew_flag=True
    elif kb.decode()=='s':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            if (info.song.wf.tell()-(info.onesecframes*10))<info.head:
                info.song.wf.setpos(info.head)
            else:
                info.song.wf.setpos(info.song.wf.tell()-int(info.onesecframes*10))
            info.renew_flag=True
    elif kb.decode()=='e':
        info.Key=0
        info.r12=1
        info.pitch_entry.delete(0,tkinter.END)
        info.pitch_entry.insert(tkinter.END,round(info.Key,2))
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb.decode()=='r':
        info.Quickness=1
        info.speed_entry.delete(0,tkinter.END)
        info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
        print("Speed=",round(info.Quickness,3))
    elif kb.decode()=='q':
        if info.song is not None and info.thread_play is not None:
            info.next_play_index=info.playlist_len+1
            info.back_flag=False
            info.quit=True
        elif info.thread_play is None:
            windowroot.destroy()
        else:
            messagebox.showinfo('エラー', 'PlayListを終了させてください')
    elif kb.decode()=='z':
        if info.shuffle_flag:
            print("ノーマル再生")
            info.back_flag=False
            info.shuffle_flag=False
            info.directory_repeat_flag=False
            info.one_repeat_flag=False
            shuffle_button['bg']='SystemButtonFace'
            directory_repeat_button['bg']='SystemButtonFace'
            one_repeat_button['bg']='SystemButtonFace'
        else:
            print("シャッフル再生")
            info.back_flag=False
            info.shuffle_flag=True
            info.directory_repeat_flag=False
            info.one_repeat_flag=False
            shuffle_button['bg']='black'
            directory_repeat_button['bg']='SystemButtonFace'
            one_repeat_button['bg']='SystemButtonFace'
    elif kb.decode()=='x':
        if info.directory_repeat_flag:
            print("ノーマル再生")
            info.back_flag=False
            info.shuffle_flag=False
            info.directory_repeat_flag=False
            info.one_repeat_flag=False
            shuffle_button['bg']='SystemButtonFace'
            directory_repeat_button['bg']='SystemButtonFace'
            one_repeat_button['bg']='SystemButtonFace'
        else:
            print("フォルダリピート")
            info.back_flag=False
            info.shuffle_flag=False
            info.directory_repeat_flag=True
            info.one_repeat_flag=False
            shuffle_button['bg']='SystemButtonFace'
            directory_repeat_button['bg']='black'
            one_repeat_button['bg']='SystemButtonFace'
    elif kb.decode()=='c':
        if info.one_repeat_flag:
            print("ノーマル再生")
            info.back_flag=False
            info.shuffle_flag=False
            info.directory_repeat_flag=False
            info.one_repeat_flag=False
            shuffle_button['bg']='SystemButtonFace'
            directory_repeat_button['bg']='SystemButtonFace'
            one_repeat_button['bg']='SystemButtonFace'
        else:
            print("1曲リピート")
            info.back_flag=False
            info.shuffle_flag=False
            info.directory_repeat_flag=False
            info.one_repeat_flag=True
            shuffle_button['bg']='SystemButtonFace'
            directory_repeat_button['bg']='SystemButtonFace'
            one_repeat_button['bg']='black'
    elif kb==b'left':#Left
        if round(info.Quickness,2)==0.1:
            messagebox.showinfo('エラー', 'これ以上は速度を落とせません')
        else:
            info.Quickness-=0.1
            info.speed_entry.delete(0,tkinter.END)
            info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
            print("Speed=",round(info.Quickness,3))
    elif kb==b'up_much':#Up
        info.Key+=1.0
        info.r12=r**np.float(info.Key)
        info.pitch_entry.delete(0,tkinter.END)
        info.pitch_entry.insert(tkinter.END,round(info.Key,2))
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb==b'right':#Right
        info.Quickness+=0.1
        info.speed_entry.delete(0,tkinter.END)
        info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
        print("Speed=",round(info.Quickness,3))
    elif kb==b'down_much':#Down
        info.Key-=1.0
        info.r12=r**np.float(info.Key)
        info.pitch_entry.delete(0,tkinter.END)
        info.pitch_entry.insert(tkinter.END,round(info.Key,2))
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb==b'changekey':
        if info.pitch_entry.get().replace(',', '').replace('.', '').replace('-', '').isnumeric():
            try:
                round(float(info.pitch_entry.get()),2)
            except:
                messagebox.showinfo('エラー', 'float型として適切ではありません')
                return
            if round(float(info.pitch_entry.get()),2)>=-12 and round(float(info.pitch_entry.get()),2)<=12:
                info.Key = round(float(info.pitch_entry.get()),2)
                info.r12=r**np.float(info.Key)
                if info.thread_play is not None:
                    info.renew_flag=True
                print("Key=",round(info.Key,2))
            else:
                messagebox.showinfo('エラー', 'Keyは-12~12でお願いします')
        else:
            messagebox.showinfo('エラー', 'Keyはfloat型でお願いします')
        info.pitch_entry.delete(0,tkinter.END)
        info.pitch_entry.insert(tkinter.END,round(info.Key,2))
    elif kb==b'changespeed':
        if info.speed_entry.get().replace(',', '').replace('.', '').replace('-', '').isnumeric():
            try:
                round(float(info.speed_entry.get()),2)
            except:
                messagebox.showinfo('エラー', 'float型として適切ではありません')
                return
            if round(float(info.speed_entry.get()),2)>=0.01:
                info.Quickness = round(float(info.speed_entry.get()),2)
                if info.thread_play is not None:
                    info.renew_flag=True
                print("Speed=",round(info.Quickness,3))
            else:
                messagebox.showinfo('エラー', 'Speedは0.01以上でお願いします')
        else:
            messagebox.showinfo('エラー', 'Speedはfloat型でお願いします')
        info.speed_entry.delete(0,tkinter.END)
        info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
def playback(filename):
    info.song = AudioFile(filename+".wav",info.r12)
    try:
        info.song.play()
    except KeyboardInterrupt:
        info.song.stream.close()
        info.song.p.terminate()
        messagebox.showinfo('強制終了', '強制終了します')
        sys.exit()

def volumeset(dummy,volume):
    info.volume=volume
    info.renew_flag=True
class WinodwClass(tk.Frame):
    PlayImage,RestartImage,exitImage=None,None,None
    stop_and_startimage=None
    sharpimage,flatimage=None,None
    leftarrowimage,rightarrowimage=None,None
    fastimage,slowimage=None,None
    shuffle_Image,directory_repeat_Image,one_repeat_Image=None,None,None
    back10secimage,forward10secimage,back5secimage,forward5secimage=None,None,None,None
    def __init__(self,master):
        super().__init__(master)
        master.title("音楽再生アプリ") #タイトル作成
        #master.protocol('WM_DELETE_WINDOW', (lambda:master.quit() if info.thread_play is None else messagebox.showinfo('エラー', 'PlayListを終了させてください')))

        image = Image.open("img/フラット.png").resize((50, 50))
        self.flatimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="pitch-1", fg = "red", image=self.flatimage,command=partial(backgroundprocess,b'down_much',''),font=("",20)).grid(row=4, column=2, padx=10, pady=10)
        image = Image.open("img/シャープ.png").resize((50, 50))
        self.sharpimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="pitch+1", fg = "red", image=self.sharpimage,command=partial(backgroundprocess,b'up_much',''),font=("",20)).grid(row=0, column=2, padx=10, pady=10)

        entryframe = ttk.Frame(master, padding=10)
        entryframe.grid(row=1, column=1,rowspan=3,columnspan=3)
        pitchframe = ttk.Frame(entryframe, padding=5)
        IDirLabel = ttk.Label(pitchframe, text="Pitch=")
        IDirLabel.pack(side=LEFT)
        info.pitch_entry = ttk.Entry(pitchframe,width=10)
        info.pitch_entry.insert(tk.END, info.Key) # 最初から文字を入れておく
        info.pitch_entry.pack(side=LEFT)
        pitchRead=ttk.Button(pitchframe, width=10, text="変更",command=partial(backgroundprocess,b'changekey',''))
        pitchRead.pack(side=LEFT)
        tk.Button(pitchframe, text="reset", fg = "red",command=partial(backgroundprocess,b'e','')).pack(side=LEFT)
        pitchframe.pack(side=TOP)

        ttk.Label(entryframe, text='--------------------------------------------').pack(side=TOP)

        image = Image.open("img/速度プラス10パー.png").resize((50, 50))
        self.fastimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="speed+10%", fg = "blue", image=self.fastimage,command=partial(backgroundprocess,b'right',''),font=("",20)).grid(row=2, column=4, padx=10, pady=10)
        image = Image.open("img/速度マイナス10パー.png").resize((50, 50))
        self.slowimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="speed-10%", fg = "blue", image=self.slowimage,command=partial(backgroundprocess,b'left',''),font=("",20)).grid(row=2, column=0, padx=10, pady=10)

        speedframe = ttk.Frame(entryframe, padding=5)
        IDirLabel = ttk.Label(speedframe, text="Speed=")
        IDirLabel.pack(side=LEFT)
        info.speed_entry = ttk.Entry(speedframe,width=10)
        info.speed_entry.insert(tk.END, info.Quickness) # 最初から文字を入れておく
        info.speed_entry.pack(side=LEFT)
        speedRead=ttk.Button(speedframe, width=10, text="変更",command=partial(backgroundprocess,b'changespeed',''))
        speedRead.pack(side=LEFT)
        tk.Button(speedframe, text="reset", fg = "blue",command=partial(backgroundprocess,b'r','')).pack(side=LEFT)
        speedframe.pack(side=TOP)


        image = Image.open("img/10秒巻き戻し.png").resize((50, 50))
        self.back10secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="back_10sec", fg = "green", image=self.back10secimage,command=partial(backgroundprocess,b's',''),font=("",20)).grid(row=5, column=1, padx=10, pady=10)
        image = Image.open("img/5秒巻き戻し.png").resize((50, 50))
        self.back5secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="back_5sec", fg = "green", image=self.back5secimage,command=partial(backgroundprocess,b'd',''),font=("",20)).grid(row=5, column=2, padx=10, pady=10)
        image = Image.open("img/5秒早送り.png").resize((50, 50))
        self.forward5secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="forward_5sec", fg = "green", image=self.forward5secimage,command=partial(backgroundprocess,b'f',''),font=("",20)).grid(row=5, column=3, padx=10, pady=10)
        image = Image.open("img/10秒早送り.png").resize((50, 50))
        self.forward10secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="forward_10sec", fg = "green", image=self.forward10secimage,command=partial(backgroundprocess,b'g',''),font=("",20)).grid(row=5, column=4, padx=10, pady=10)

        image = Image.open("img/リスタート.png").resize((50, 50))
        self.RestartImage=ImageTk.PhotoImage(image)
        tk.Button(master, text="restart", fg = "deep pink",image=self.RestartImage,command=partial(backgroundprocess,b'p',''),font=("",20)).grid(row=6, column=4, padx=10, pady=10)
        image = Image.open("img/EXIT.png").resize((50, 50))
        self.exitImage=ImageTk.PhotoImage(image)
        tk.Button(master, text="終了", fg = "deep pink",image=self.exitImage,command=partial(backgroundprocess,b'q','',windowroot=master),font=("",20)).grid(row=6, column=5, padx=10, pady=10)

        image = Image.open("img/再生ボタン.png").resize((50, 50))
        self.PlayImage=ImageTk.PhotoImage(image)
        tk.Button(master, text="再生", fg = "navy",image=self.PlayImage,command=start_playthread,font=("",20)).grid(row=6, column=2, padx=10, pady=10)
        info.playtimeframe = tk.LabelFrame(master, text="再生時間",font=("",20))
        info.playtimeframe.grid(row=6, column=0,columnspan=2,padx=10, pady=10)
        info.label=tk.Label(info.playtimeframe, text='--s/--s',font=("",20))
        info.label.pack()
        getplaytime(master)

        image = Image.open("img/一時停止再開ボタン.png").resize((50, 50))
        self.stop_and_startimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="一時停止/再開", fg = "navy", image=self.stop_and_startimage,command=partial(backgroundprocess,b'\r',''),font=("",20)).grid(row=6, column=3, padx=10, pady=10)

        image = Image.open("img/左矢印.png").resize((50, 50))
        self.leftarrowimage=ImageTk.PhotoImage(image)
        backbutton=tk.Button(master, text="back", fg = "orange", image=self.leftarrowimage,command=partial(backgroundprocess,b'b',''),font=("",20))
        image = Image.open("img/右矢印.png").resize((50, 50))
        self.rightarrowimage=ImageTk.PhotoImage(image)
        nextbutton=tk.Button(master, text="next", fg = "orange", image=self.rightarrowimage,command=partial(backgroundprocess,b'n',''),font=("",20))


        image = Image.open("img/シャッフル再生.png").resize((50, 50))
        self.shuffle_Image=ImageTk.PhotoImage(image)
        shuffle_button=tk.Button(master, text="シャッフル", fg = "purple",image=self.shuffle_Image,font=("",20))
        image = Image.open("img/フォルダリピート.png").resize((50, 50))
        self.directory_repeat_Image=ImageTk.PhotoImage(image)
        directory_repeat_button=tk.Button(master, text="フォルダリピート", fg = "purple", image=self.directory_repeat_Image,font=("",20))
        image = Image.open("img/1曲リピート.png").resize((50, 50))
        self.one_repeat_Image=ImageTk.PhotoImage(image)
        one_repeat_button=tk.Button(master, text="1曲リピート", fg = "purple", image=self.one_repeat_Image,font=("",20))

        backbutton['command']=partial(backgroundprocess,b'b','',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        backbutton.grid(row=5, column=0, padx=10, pady=10)
        nextbutton['command']=partial(backgroundprocess,b'n','',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        nextbutton.grid(row=5, column=5, padx=10, pady=10)
        shuffle_button['command']=partial(backgroundprocess,b'z','',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        shuffle_button.grid(row=0, column=5, padx=10, pady=10)
        directory_repeat_button['command']=partial(backgroundprocess,b'x','',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        directory_repeat_button.grid(row=2, column=5, padx=10, pady=10)
        one_repeat_button['command']=partial(backgroundprocess,b'c','',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        one_repeat_button.grid(row=4, column=5, padx=10, pady=10)

        scaleframe = ttk.Frame(master,padding=10)
        first_label=tk.Label(scaleframe, text="first",font=("",20))
        first_label.pack(side=tk.LEFT)
        val = DoubleVar()
        info.scalebar = ttk.Scale(
            scaleframe,
            variable=val,
            orient=HORIZONTAL,
            length=700,
            from_=0,
            to=info.duration,
            command=partial(backgroundprocess,val.get()))
        pos_renew(master,scaleframe)
        info.scalebar.pack(side=tk.LEFT)
        last_label=tk.Label(scaleframe, text="last",font=("",20))
        last_label.pack(side=tk.RIGHT)
        scaleframe.grid(row=7,column=0,columnspan=6,sticky=(N, W, S, E))

        volumescaleframe = ttk.Frame(master)
        volume_label_0=tk.Label(volumescaleframe, text="Volume: 0")
        volume_label_0.pack(side=tk.LEFT)
        volumeval = IntVar(master=master,value=100)
        volumescalebar = tk.Scale(
            volumescaleframe,
            variable=volumeval,
            orient=HORIZONTAL,
            length=100,
            from_=0,
            to=100,
            command=partial(volumeset,volumeval.get()))
        volumescalebar.pack(side=tk.LEFT)
        volume_label_100=tk.Label(volumescaleframe, text="100")
        volume_label_100.pack(side=tk.RIGHT)
        volumescaleframe.grid(row=0,column=3,columnspan=2,sticky=(E))

def pos_renew(root,scaleframe):
    if (info.thread_play is not None) and (info.head is not None) and (info.song is not None):
        val = DoubleVar(master=root,value=int((info.song.wf.tell()-info.head)/(info.last-info.head)*info.duration))
        info.scalebar['variable']=val
        info.scalebar['to']=info.duration
    root.after(100,pos_renew,root,scaleframe)
class WindowThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        window()
        print("終了")
        sys.exit()

def window():
    info.root = Tk()
    info.root.configure(bg='gray')
    rootA = WinodwClass(master = info.root)
    rootA.mainloop()

def getplaytime(root):
    if (info.thread_play is not None) and (info.head is not None) and (info.song is not None):
        info.label['text']=str('{:.2f}'.format((info.song.wf.tell()-info.head)/(info.last-info.head)*info.duration))+"s/"+str('{:.2f}'.format(info.duration))+"s"
    root.after(100,getplaytime,root)

class PlayListTkinterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        PlayListTkintertk = Tk()
        PlayListTkinter=PlayListTkinterClass(master=PlayListTkintertk)
        PlayListTkinter.mainloop()
class ScrollFrame(ClassFrame):
    def __init__(self, master, playlist, bg=None, width=None, height=None):
        super(ScrollFrame, self).__init__(master, bg=bg, width=width, height=height)

        # スクロールバーの作成
        self.scroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.scroll_bar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        self.canvas = tk.Canvas(self, yscrollcommand=self.scroll_bar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_bar.config(command=self.canvas.yview)

        # ビューをリセット
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = tk.Frame(self.canvas, bg="gray90", borderwidth=10)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

        self.interior.bind('<Configure>', self.configure_interior)
        self.canvas.bind('<Configure>', self.configure_canvas)

        self.buttons = []
        for i, target in enumerate(playlist):
            self.buttons.append(tk.Button(self.interior, text=str(i+1)+": "+target, command=partial(backgroundprocess,i+1,'')))
            self.buttons[i].pack(anchor=tk.NW, fill=tk.X, pady=(0, 10))

    def configure_interior(self, event=None):
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def configure_canvas(self, event=None):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())


class PlayListTkinterClass(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        master.title("Playlistの選択")
        master.protocol('WM_DELETE_WINDOW', (lambda:master.quit()))
        master.attributes("-topmost", True)

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
        IDirButton = ttk.Button(frame1, text="参照", command=partial(dirdialog_clicked,master))
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
        IFileButton = ttk.Button(frame2, text="参照", command=partial(filedialog_clicked,master))
        IFileButton.pack(side=LEFT)
        btnRead2=ttk.Button(frame2, width=10, text="再生",
                            command=lambda:file_play(master))
        btnRead2.pack(side=LEFT)

        # Frame3の作成
        frame3 = ttk.Frame(master, padding=10)
        frame3.grid(row=7,column=1,sticky=W)

class PlaylistCanvas:
    def __init__(self, playlist):
        self.canvas = tk.Canvas(info.root)
        self.playlistframe =  ScrollFrame(master=self.canvas, playlist=playlist)
        self.canvas.grid(row=1, column=6, rowspan=5,padx=10, pady=10,sticky="WNES")
        self.canvas.create_window((0,0), window=self.playlistframe, anchor=tk.NW, width=self.canvas.cget('width'))
        self.playlistframe.interior.bind("<MouseWheel>",self.mouse_y_scroll)
        if len(playlist)>=8:
            for i in range(len(playlist)):
                self.playlistframe.buttons[i].bind("<MouseWheel>", self.mouse_y_scroll)
    def getCanvas(self):
        return self.canvas
    def move_start(self, event):
        self.playlistframe.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.playlistframe.canvas.scan_dragto(event.x, event.y, gain=1)

    def mouse_y_scroll(self, event):
        if event.delta > 0:
            self.playlistframe.canvas.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.playlistframe.canvas.yview_scroll(1, 'units')

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
            thread_playlisttkinter=PlayListTkinterThread()
            thread_playlisttkinter.start()
            thread_playlisttkinter.join()
            if info.mode==0:
                if info.targetname_0_str != '':
                    os.chdir(info.targetname_0_str)
                    info.root.title("音楽再生アプリ("+info.targetname_0_str+")")
            elif info.mode==1:
                if info.targetname_1_str != '' :
                    os.chdir(info.targetname_1_str)
                    info.root.title("音楽再生アプリ("+info.targetname_1_str+")")
            elif info.mode==2:
                if info.targetname_2_str != '':
                    playfile=info.targetname_2_str
                    info.root.title("音楽再生アプリ("+info.targetname_2_str+")")
            else:
                print("×が押されました")
                info.thread_play=None
                return
        except e:
            messagebox.showinfo('エラー', '予期せぬエラーが発生しました(これを見たときは至急私まで)')
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
                shutil.copyfile(info.basedirname + "/lib/ffmpeg.exe", "./ffmpeg.exe")
                shutil.copyfile(info.basedirname + "/lib/ffplay.exe", "./ffplay.exe")
                shutil.copyfile(info.basedirname + "/lib/ffprobe.exe", "./ffprobe.exe")
                print(playlistdirname,"フォルダを発見しました")
                print("ファイルをチェックします")
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
                                    os.system("ffmpeg.exe -i "+ os.path.split(f)[1].replace(' ','') + " " + playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                            elif os.path.splitext(f)[1]=='.mp4':
                                print(os.path.split(f)[1],'→',end='')
                                if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                                    print("wavが既にあるため変換しません")
                                else:
                                    print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                                    os.system("ffmpeg.exe -i "+ os.path.split(f)[1].replace(' ','') + " " +  playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                if os.getcwd()!= info.basedirname:
                    os.remove("./ffmpeg.exe")
                    os.remove("./ffplay.exe")
                    os.remove("./ffprobe.exe")
                print("ファイルチェック完了!")
            else:
                shutil.copyfile(info.basedirname + "/lib/ffmpeg.exe", "./ffmpeg.exe")
                shutil.copyfile(info.basedirname + "/lib/ffplay.exe", "./ffplay.exe")
                shutil.copyfile(info.basedirname + "/lib/ffprobe.exe", "./ffprobe.exe")
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
                            os.system("ffmpeg.exe -i "+ os.path.split(f)[1].replace(' ','') + " " + playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                    elif os.path.splitext(f)[1]=='.mp4':
                        print(os.path.split(f)[1],'→',end='')
                        if os.path.exists(os.path.splitext(f)[0].replace(' ','')+".wav"):
                            print("wavが既にあるため変換しません")
                        else:
                            print(os.path.split(f)[1],"を",os.path.splitext(f)[0],".wav","へ変換")
                            os.system("ffmpeg.exe -i "+ os.path.split(f)[1].replace(' ','') + " " +  playlistdirname+"/" + os.path.splitext(f)[0].replace(' ','') + ".wav")
                if os.getcwd()!= info.basedirname:
                    os.remove("./ffmpeg.exe")
                    os.remove("./ffplay.exe")
                    os.remove("./ffprobe.exe")
                print("変換完了！")
            print("")
            print("playlistを作成します")
            os.chdir(playlistdirname)
            playlist=[]
            for f in glob.glob("./*"):
                if os.path.splitext(f)[1]=='.wav':
                    print(os.path.split(f)[1])
                    playlist.append(os.path.basename(f).split('.', 1)[0])
            print("playlist作成完了！")
            print("")
            print("playlist=",playlist)
            index=0
            info.playlist_len=len(playlist)
            if info.playlist_len==0:
                messagebox.showinfo('エラー', 'playlistの曲がありません')
                os.chdir("../")
                os.rmdir(playlistdirname)
                info.thread_play=None
                return
            #canvas処理
            canvas=PlaylistCanvas(playlist=playlist)
            canvas=canvas.getCanvas()
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
        canvas.grid_forget()
        #bar_ver.grid_forget()
        info.label['text']='--s/--s'

def start_windowthread():
    thread_window=WindowThread()
    thread_window.start()

def start_playthread():
    if info.thread_play is None:
        info.song=None
        info.thread_play=PlayThread()
        info.thread_play.start()
    else:
        messagebox.showinfo('エラー', '既に再生しています')

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

class outputdeviceInputClass(tk.Frame):
    def __init__(self,master,outputdevicelist):
        super().__init__(master)
        master.title("出力デバイスの選択")
        var = tk.IntVar()
        var.set(outputdevicelist[0]['index'])

        for i in range(len(outputdevicelist)):
            tk.Radiobutton(master, value=outputdevicelist[i]['index'], variable=var, text=outputdevicelist[i]['name']).pack(side='top')
        DeviceReadButton=tk.Button(master, height=1, width=10, text="OK", command = lambda:OutputDeviceRead(master,var))
        DeviceReadButton.pack(side='top')

if __name__ == "__main__":
    KeySpeedInputtk = Tk()
    KeySpeedInput=KeySpeedInputClass(master=KeySpeedInputtk)
    KeySpeedInput.mainloop()
    info.Key=round(info.Key,1)
    info.Quickness=round(info.Quickness,2)
    info.basedirname=os.path.dirname(os.path.abspath("__file__"))
    p=pyaudio.PyAudio()
    outputdevicelist=[]
    for index in range(0,p.get_device_count()):
        if p.get_device_info_by_index(index)['hostApi']==0 and p.get_device_info_by_index(index)['maxOutputChannels']==2:
            outputdevicelist.append(p.get_device_info_by_index(index))
    print("出力デバイスを選択")
    if len(outputdevicelist)==0:
        print("出力デバイスがありません。プレイヤーを開始できません")
    elif len(outputdevicelist)==1:
        info.outputdeviceindex=outputdevicelist[0]['index']
    elif len(outputdevicelist)>=2:
        outputdeviceInputtk=Tk()
        outputdeviceInput=outputdeviceInputClass(master=outputdeviceInputtk,outputdevicelist=outputdevicelist)
        outputdeviceInput.mainloop()
    help()
    r = 2**(1/12)
    info.r12=(2**(1/12))**np.float(info.Key)
    start_windowthread()
