from MusicPlayApp_IF import *
import librosa
info=AudioInformation()

def dirdialog_clicked(PlayListTkinter):#フォルダ参照
    PlayListTkinter.attributes("-topmost", False)
    iDir = os.path.abspath(os.path.dirname("__file__")+"../")
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    PlayListTkinter.attributes("-topmost", True)
    if iDirPath !='':
        info.targetname_0.delete(0,tkinter.END)
        info.targetname_2.delete(0,tkinter.END)
        info.targetname_1.delete(0,tkinter.END)
        info.targetname_1.insert(tkinter.END,iDirPath)
def dir_play(PlayListTkinter):#フォルダ再生
    if os.path.isdir(info.targetname_1.get()):
        info.mode=1
        info.targetname_str=info.targetname_1.get()
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')

def filedialog_clicked(PlayListTkinter):#ファイル参照
    PlayListTkinter.attributes("-topmost", False)
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname("__file__")+"../")
    iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
    PlayListTkinter.attributes("-topmost", True)
    if iFilePath != '':
        info.targetname_0.delete(0,tkinter.END)
        info.targetname_1.delete(0,tkinter.END)
        info.targetname_2.delete(0,tkinter.END)
        info.targetname_2.insert(tkinter.END,iFilePath)
def file_play(PlayListTkinter):#ファイル再生
    if os.path.isfile(info.targetname_2.get()):
        info.mode=2
        info.targetname_str=info.targetname_2.get()
        PlayListTkinter.quit()
    else:
        messagebox.showinfo('エラー', '指定されたパスが存在しません')
def getTextInput(PlayListTkinter):#パス指定再生
    if info.targetname_0.get()=='./' or os.path.isdir(info.targetname_0.get()):
        info.mode=0
        info.targetname_str=info.targetname_0.get()
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
    info.targetname_0.insert(tkinter.END,info.basedirname.replace('\\','/'))

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
def OutputDeviceRead(event=None,outputdeviceInputClass=None):
    if info.thread_play is not None:
        info.song.renew()
    if outputdeviceInputClass is not None:
        outputdeviceInputClass.destroy()
class PSThread(threading.Thread):
    data=None
    def __init__(self,data_pre):
        self.data=data_pre
        threading.Thread.__init__(self)
    def run(self):
        if len(self.data)!=0:
            self.data = np.frombuffer(self.data,dtype="int16")
            self.data=self.data.astype(np.float64)
            self.data = librosa.effects.pitch_shift(self.data,info.song.wf.getframerate(),info.Key)

            self.data = librosa.effects.time_stretch(self.data,info.Quickness)
            self.data*=0.9
            self.data*=round(float(info.volume),2)/100
            self.data = self.data.astype(np.int16)
            self.data = np.ndarray.tobytes(self.data)
    def getdata(self):
        return self.data

class AudioFile:
        if info.algorithm==0:
            chunk = 1024*2
            buffer=1024*2
        elif info.algorithm==1:
            chunk_mul=128
            chunk = 1024*chunk_mul
            buffer=1024*2
        def __init__(self, file, speed,song_index):
            """ Init audio stream """
            self.song_index=song_index
            self.wf = wave.open(file, 'rb')
            self.speed = speed
            self.p = pyaudio.PyAudio()
            if info.targetname_str != None:
                info.root.title("音楽再生アプリ("+info.targetname_str+")   「"+os.path.basename(file).split('.', 1)[0]+"」再生中...")
            if info.algorithm==0:
               self.stream = self.p.open(
                   format = self.p.get_format_from_width(self.wf.getsampwidth()),
                   channels = self.wf.getnchannels(),
                   frames_per_buffer = self.buffer,
                   rate = int(self.wf.getframerate()*info.r12),
                   output_device_index=info.outputdeviceindex.get(),
                   input=False,
                   output = True)
            elif info.algorithm==1:
               self.stream = self.p.open(
                   format = self.p.get_format_from_width(self.wf.getsampwidth()),
                   channels = self.wf.getnchannels(),
                   frames_per_buffer = self.buffer,
                   rate = int(self.wf.getframerate()),
                   output_device_index=info.outputdeviceindex.get(),
                   input=False,
                   output = True)

        def play(self):
            """ Play entire file """
            print("playing...")
            info.head=self.wf.tell()
            data_pre = self.wf.readframes(1)
            data=''
            frames=self.wf.getnframes()
            framerate=self.wf.getframerate()
            info.last=info.head+frames
            info.duration=self.wf.getnframes()/self.wf.getframerate()
            info.onesecframes=(info.last-info.head)/info.duration
            info.quit=False
            info.stop_flag=False
            nextpos=None
            if info.algorithm==0:
                self.chunk = 1024*2
                self.buffer=1024*2
            elif info.algorithm==1:
                chunk_mul=128
                self.chunk = 1024*chunk_mul
                self.buffer=1024*4
            while True:
                if not (len(data_pre)!=0 and info.quit==False):
                    if info.quit==False:
                        info.playviews[self.song_index][1]+=1
                    break
                if info.renew_flag:
                    self.renew()
                    info.renew_flag=False
                if self.stream.is_active():
                    if info.algorithm==0:
                        if data == '':
                            data_pre = self.wf.readframes(int(self.chunk))
                            time.sleep(0.1)
                        elif data != '':
                            data_pre=data
                            data=''
                        crossfadelength=2048
                        if info.Quickness < 1 or info.r12 >1:
                            if self.wf.tell()==info.last:
                                if self.stream.is_active():
                                    self.stream.write(data_pre)
                                data_pre=''
                                continue
                            else:
                                if self.wf.tell()-int(self.chunk*(1-(info.Quickness/info.r12)))-crossfadelength >=info.head:
                                    self.wf.setpos(self.wf.tell()-int(self.chunk*(1-(info.Quickness/info.r12)))-crossfadelength)
                                data = self.wf.readframes(int(self.chunk)+crossfadelength)
                        elif info.Quickness > 1 or info.r12 < 1:
                            if self.wf.tell()==info.last:
                                if self.stream.is_active():
                                    self.stream.write(data_pre)
                                data_pre=''
                                continue
                            else:
                                if self.wf.tell()-crossfadelength >= info.head:
                                    self.wf.setpos(self.wf.tell()-crossfadelength)
                                dummy = self.wf.readframes(int(self.chunk*((info.Quickness/info.r12)-1)))
                                data = self.wf.readframes(int(self.chunk)+crossfadelength)
                        else:
                            data = self.wf.readframes(int(self.chunk)+crossfadelength)
                        if (info.Quickness != 1 or info.r12 !=1):
                            data_pre,data = gen_xfade_honesty(data_pre,data,crossfadelength*(len(data)/(self.chunk+crossfadelength))/2,int(self.wf.getframerate()*info.r12))
                        data_pre=np.frombuffer(data_pre,dtype="int16")
                        data_pre=data_pre.astype(np.float64)
                        data_pre=data_pre*round(float(info.volume),2)/100
                        data_pre=data_pre.astype(np.int16)
                        data_pre=data_pre.tobytes()
                        if info.stop_flag:
                            self.stream.stop_stream()
                            while self.stream.is_active()==False:
                                if info.quit or info.stop_flag==False:
                                    break
                                time.sleep(0.1)
                            self.stream.start_stream()
                        if self.stream.is_active():
                            self.stream.write(data_pre)

                    if info.algorithm==1:
                        if self.wf.tell()==info.last:
                            data_pre=''
                            continue
                        currentpos=self.wf.tell()
                        try:
                            if data !='':
                                dummy = self.wf.readframes(int(self.chunk))
                                nextpos=self.wf.tell()
                                data=self.wf.readframes(int(self.chunk))
                                self.wf.setpos(currentpos)
                            else:
                                data_pre=self.wf.readframes(int(self.chunk))
                                nextpos=self.wf.tell()
                                data = self.wf.readframes(int(self.chunk))
                                self.wf.setpos(currentpos)
                                thread_PS=PSThread(data_pre)
                                thread_PS.start()
                                thread_PS.join()
                                data_pre=thread_PS.getdata()
                        except Runtimeerror:
                            print("Runtimeerror出ましたが続けます")
                        thread_PS=PSThread(data)
                        thread_PS.start()
                        size=1024*2
                        datakind=int(len(data_pre)/(1024*128))
                        if datakind==0:
                            datakind=int(len(data)/(1024*128))
                        if datakind==0:
                            data_pre=''
                            continue
                        for i in range(int(len(data_pre)/(size*datakind))+1):
                            if info.quit:
                                break
                            if info.renew_flag:
                                self.renew()
                                info.renew_flag=False
                                try:
                                    self.wf.setpos(self.wf.tell())
                                except wave.Error:
                                    print("waveerror出たけど続けます")
                                    data_pre=''
                                    continue
                                data=''#多分ここが飛んでる原因
                                if info.stop_flag:
                                    self.stream.stop_stream()
                                    while self.stream.is_active()==False:
                                        if info.quit or info.stop_flag==False:
                                            break
                                        time.sleep(0.1)
                                    self.stream.start_stream()
                                if info.stop_flag==False:
                                    break
                            if i<int(len(data_pre)/(size*datakind)):
                                if self.stream.is_active():
                                    if info.stop_flag:
                                        thread_PS.join()
                                        self.stream.stop_stream()
                                    if self.stream.is_active():
                                        dummy=self.wf.readframes(size)
                                        self.stream.write(data_pre[(size*datakind)*i:(size*datakind)*(i+1)])
                            else:
                                if info.stop_flag:
                                    self.stream.stop_stream()
                                if self.stream.is_active():
                                    self.wf.setpos(nextpos)
                                    self.stream.write(data_pre[(size*datakind)*i:])
                                thread_PS.join()
                                data_pre=thread_PS.getdata()
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
                if info.algorithm==0:
                    self.stream = self.p.open(
                        format = self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels = self.wf.getnchannels(),
                        frames_per_buffer = self.buffer,
                        rate = int(self.wf.getframerate()*info.r12),
                        output_device_index=info.outputdeviceindex.get(),
                        input=False,
                        output = True)
                elif info.algorithm==1:
                    self.stream = self.p.open(
                        format = self.p.get_format_from_width(self.wf.getsampwidth()),
                        channels = self.wf.getnchannels(),
                        frames_per_buffer = self.buffer,
                        rate = int(self.wf.getframerate()),
                        output_device_index=info.outputdeviceindex.get(),
                        input=False,
                        output = True)

def backgroundprocess(event=None,kb=None,scaleint=None,shuffle_button=None,directory_repeat_button=None,one_repeat_button=None,windowroot=None):
    print(kb)
    if isinstance(kb,int):#playlistの曲のボタンが押されたとき
        if info.isfavorite==0:
            info.next_play_index=kb
            info.back_flag=False
            info.quit=True
        else:
            if info.favorite_songlist[kb-1]==1:
                info.next_play_index=kb
                info.back_flag=False
                info.quit=True
            else:
                messagebox.showinfo('エラー', 'お気に入り以外の曲を再生するにはお気に入りのみをoffにしてください')
    elif scaleint is not None:
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            try:
                info.song.wf.setpos(int(info.head+info.onesecframes*float(scaleint.get())))
            except wave.Error:
                pass
            info.renew_flag=True
    elif kb.decode()=='\r':
        if info.thread_play is None or info.song is None:
            messagebox.showinfo('エラー', '音楽を開始してください')
        else:
            if info.song.stream.is_active():
                info.stop_flag=True
                print("停止します")
                # info.song.stream.stop_stream()
            else:
                info.stop_flag=False
                print("再開します")
                # info.song.stream.start_stream()
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
        info.Quickness=round(info.Quickness,3)
        info.speed_entry.delete(0,tkinter.END)
        info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
        if info.thread_play is not None:
            info.renew_flag=True
        print("Speed=",round(info.Quickness,3))
    elif kb.decode()=='q':
        if info.song is not None and info.thread_play is not None:
            info.next_play_index=info.playlist_len+2
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
            info.Quickness=round(info.Quickness,3)
            info.speed_entry.delete(0,tkinter.END)
            info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
            if info.thread_play is not None:
                info.renew_flag=True
            print("Speed=",round(info.Quickness,3))
    elif kb==b'up_much':#Up
        info.Key+=1.0
        info.Key=round(info.Key,2)
        info.r12=r**np.float(info.Key)
        info.pitch_entry.delete(0,tkinter.END)
        info.pitch_entry.insert(tkinter.END,round(info.Key,2))
        if info.thread_play is not None:
            info.renew_flag=True
        print("Key=",round(info.Key,2))
    elif kb==b'right':#Right
        info.Quickness+=0.1
        info.Quickness=round(info.Quickness,3)
        info.speed_entry.delete(0,tkinter.END)
        info.speed_entry.insert(tkinter.END,round(info.Quickness,3))
        if info.thread_play is not None:
            info.renew_flag=True
        print("Speed=",round(info.Quickness,3))
    elif kb==b'down_much':#Down
        info.Key-=1.0
        info.Key=round(info.Key,2)
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
def playback(filename,song_index):
    info.song = AudioFile(filename+".wav",speed=info.r12,song_index=song_index)
    try:
        info.song.play()
    except KeyboardInterrupt:
        info.song.stream.close()
        info.song.p.terminate()
        messagebox.showinfo('強制終了', '強制終了します')
        sys.exit()

def setalgorithm(algorithm_num):
    if info.song is None or info.thread_play is None:
        if algorithm_num==0:
            info.algorithm=0
        elif algorithm_num==1:
            info.algorithm=1
        return
    if algorithm_num==0:
        info.algorithm=0
        info.song.chunk=1024*2
        info.song.buffer=1024*2
        if info.thread_play is not None:
            info.renew_flag=True
    elif algorithm_num==1:
        info.algorithm=1
        info.song.chunk=1024*128
        info.song.buffer=1024*2
        if info.thread_play is not None:
            info.renew_flag=True
def setisfavorite(isfavorite_num,isfavoritevar=None):
    if isfavorite_num==0:
        info.isfavorite=0
    if isfavorite_num==1:
        if 1 in info.favorite_songlist:
            info.isfavorite=1
            if len(info.next_play_index_list)!=0:
                i=0
                delflag=False
                while True:
                    i_label=info.Window.menu_playlist.entrycget(i,"label")
                    i_label=i_label[i_label.find('→')+1:i_label.find(':')]
                    if info.favorite_songlist[int(i_label)-1]==0:
                        if delflag==False:
                            delflag = messagebox.askyesno('確認', '「お気に入りのみ」にすると「次に再生」リストからお気に入りされていない曲が削除されます。続けますか？')
                        if delflag==True:
                            del info.next_play_index_list[i]
                            info.Window.menu_playlist.delete(i)#削除
                            del info.canvas.second_menu[i]
                            id=i
                            while True:
                                if id==len(info.next_play_index_list):
                                    break
                                else:
                                    i_label=info.Window.menu_playlist.entrycget(id,"label")
                                    info.canvas.second_menu[id].entryconfigure(0, command=partial(info.canvas.deletesong_fromnextplayindexlist,i=id))#更新
                                    if (id+1)%10==1:
                                        ordinal_end='st'
                                    elif (id+1)%10==2:
                                        ordinal_end='nd'
                                    elif (id+1)%10==3:
                                        ordinal_end='rd'
                                    else:
                                        ordinal_end='th'
                                    info.Window.menu_playlist.entryconfigure(id,label=str(int(id)+1)+ordinal_end+'→'+i_label[i_label.find('→')+1:])
                                    id+=1
                            if len(info.next_play_index_list)!=0:
                                info.Window.menu_ROOT.entryconfigure(3, label="次に再生(N)("+str(len(info.next_play_index_list))+")")#更新
                            else:
                                info.Window.menu_ROOT.entryconfigure(3, label='次に再生(N)')#更新
                        else:
                            info.isfavorite=0
                            isfavoritevar.set(0)
                            break
                    else:
                        i+=1
                    if i==len(info.next_play_index_list):
                        break
        else:
            messagebox.showinfo('エラー', '最低１曲お気に入り登録してください')
            isfavoritevar.set(0)

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
        #master.resizable(0,0)
        master.protocol('WM_DELETE_WINDOW', (lambda:master.quit() if info.thread_play is None else messagebox.showinfo('エラー', 'PlayListを終了させてください')))
        master.unbind_class("Button", "<Key-space>")
        image = Image.open("img/フラット.png").resize((50, 50))
        self.flatimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="pitch-1", fg = "red", image=self.flatimage,command=partial(backgroundprocess,kb=b'down_much'),font=("",20)).grid(row=4, column=2, padx=10, pady=10)
        image = Image.open("img/シャープ.png").resize((50, 50))
        self.sharpimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="pitch+1", fg = "red", image=self.sharpimage,command=partial(backgroundprocess,kb=b'up_much'),font=("",20)).grid(row=0, column=2, padx=10, pady=10)

        entryframe = ttk.Frame(master, padding=10)
        entryframe.grid(row=1, column=1,rowspan=3,columnspan=3)
        pitchframe = ttk.Frame(entryframe, padding=5)
        IDirLabel = ttk.Label(pitchframe, text="Pitch=")
        IDirLabel.pack(side=LEFT)
        info.pitch_entry = ttk.Entry(pitchframe,width=10)
        info.pitch_entry.insert(tk.END, info.Key) # 最初から文字を入れておく
        info.pitch_entry.pack(side=LEFT)
        pitchRead=ttk.Button(pitchframe, width=10, text="変更",command=partial(backgroundprocess,kb=b'changekey'))
        pitchRead.pack(side=LEFT)
        tk.Button(pitchframe, text="reset", fg = "red",command=partial(backgroundprocess,kb=b'e')).pack(side=LEFT)
        pitchframe.pack(side=TOP)

        ttk.Label(entryframe, text='--------------------------------------------').pack(side=TOP)

        image = Image.open("img/速度プラス10パー.png").resize((50, 50))
        self.fastimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="speed+10%", fg = "blue", image=self.fastimage,command=partial(backgroundprocess,kb=b'right'),font=("",20)).grid(row=2, column=4, padx=10, pady=10)
        image = Image.open("img/速度マイナス10パー.png").resize((50, 50))
        self.slowimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="speed-10%", fg = "blue", image=self.slowimage,command=partial(backgroundprocess,kb=b'left'),font=("",20)).grid(row=2, column=0, padx=10, pady=10)

        speedframe = ttk.Frame(entryframe, padding=5)
        IDirLabel = ttk.Label(speedframe, text="Speed=")
        IDirLabel.pack(side=LEFT)
        info.speed_entry = ttk.Entry(speedframe,width=10)
        info.speed_entry.insert(tk.END, info.Quickness) # 最初から文字を入れておく
        info.speed_entry.pack(side=LEFT)
        speedRead=ttk.Button(speedframe, width=10, text="変更",command=partial(backgroundprocess,kb=b'changespeed'))
        speedRead.pack(side=LEFT)
        tk.Button(speedframe, text="reset", fg = "blue",command=partial(backgroundprocess,kb=b'r')).pack(side=LEFT)
        speedframe.pack(side=TOP)

        master.bind("<Shift-Left>",partial(backgroundprocess,kb=b'left'))
        master.bind("<Shift-Right>",partial(backgroundprocess,kb=b'right'))
        master.bind("<Shift-Up>",partial(backgroundprocess,kb=b'up_much'))
        master.bind("<Shift-Down>",partial(backgroundprocess,kb=b'down_much'))

        image = Image.open("img/10秒巻き戻し.png").resize((50, 50))
        self.back10secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="back_10sec", fg = "green", image=self.back10secimage,command=partial(backgroundprocess,kb=b's'),font=("",20)).grid(row=5, column=1, padx=10, pady=10)
        image = Image.open("img/5秒巻き戻し.png").resize((50, 50))
        self.back5secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="back_5sec", fg = "green", image=self.back5secimage,command=partial(backgroundprocess,kb=b'd'),font=("",20)).grid(row=5, column=2, padx=10, pady=10)
        image = Image.open("img/5秒早送り.png").resize((50, 50))
        self.forward5secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="forward_5sec", fg = "green", image=self.forward5secimage,command=partial(backgroundprocess,kb=b'f'),font=("",20)).grid(row=5, column=3, padx=10, pady=10)
        image = Image.open("img/10秒早送り.png").resize((50, 50))
        self.forward10secimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="forward_10sec", fg = "green", image=self.forward10secimage,command=partial(backgroundprocess,kb=b'g'),font=("",20)).grid(row=5, column=4, padx=10, pady=10)

        master.bind("<Left>",partial(backgroundprocess,kb=b'd'))
        master.bind("<Right>",partial(backgroundprocess,kb=b'f'))
        master.bind("<Control-Left>",partial(backgroundprocess,kb=b's'))
        master.bind("<Control-Right>",partial(backgroundprocess,kb=b'g'))

        image = Image.open("img/リスタート.png").resize((50, 50))
        self.RestartImage=ImageTk.PhotoImage(image)
        tk.Button(master, text="restart", fg = "deep pink",image=self.RestartImage,command=partial(backgroundprocess,kb=b'p'),font=("",20)).grid(row=6, column=4, padx=10, pady=10)
        master.bind("<Key-BackSpace>",partial(backgroundprocess,kb=b'p'))
        #master.bind("<Key-p>",partial(backgroundprocess,kb=b'p'))

        image = Image.open("img/EXIT.png").resize((50, 50))
        self.exitImage=ImageTk.PhotoImage(image)
        tk.Button(master, text="終了", fg = "deep pink",image=self.exitImage,command=partial(backgroundprocess,kb=b'q',windowroot=master),font=("",20)).grid(row=6, column=5, padx=10, pady=10)
        master.bind("<Escape>",partial(backgroundprocess,kb=b'q',windowroot=master))

        image = Image.open("img/再生ボタン.png").resize((50, 50))
        self.PlayImage=ImageTk.PhotoImage(image)
        tk.Button(master, text="再生", fg = "navy",image=self.PlayImage,command=start_playthread,font=("",20)).grid(row=6, column=2, padx=10, pady=10)
        self.playtimeframe = tk.LabelFrame(master, text="再生時間",font=("",20))
        self.playtimeframe.grid(row=6, column=0,columnspan=2,padx=10, pady=10)
        self.label=tk.Label(self.playtimeframe, text='--s/--s',font=("",20))
        self.label.pack()
        playtime=getplaytime(root=master,label=self.label)
        playtime.renewplaytime()
        image = Image.open("img/一時停止再開ボタン.png").resize((50, 50))
        self.stop_and_startimage=ImageTk.PhotoImage(image)
        tk.Button(master, text="一時停止/再開", fg = "navy", image=self.stop_and_startimage,command=partial(backgroundprocess,kb=b'\r'),font=("",20)).grid(row=6, column=3, padx=10, pady=10)
        master.bind("<Return>",partial(backgroundprocess,kb=b'\r'))

        image = Image.open("img/左矢印.png").resize((50, 50))
        self.leftarrowimage=ImageTk.PhotoImage(image)
        backbutton=tk.Button(master, text="back", fg = "orange", image=self.leftarrowimage,command=partial(backgroundprocess,kb=b'b'),font=("",20))
        image = Image.open("img/右矢印.png").resize((50, 50))
        self.rightarrowimage=ImageTk.PhotoImage(image)
        nextbutton=tk.Button(master, text="next", fg = "orange", image=self.rightarrowimage,command=partial(backgroundprocess,kb=b'n'),font=("",20))


        image = Image.open("img/シャッフル再生.png").resize((50, 50))
        self.shuffle_Image=ImageTk.PhotoImage(image)
        shuffle_button=tk.Button(master, text="シャッフル", fg = "purple",image=self.shuffle_Image,font=("",20))
        image = Image.open("img/フォルダリピート.png").resize((50, 50))
        self.directory_repeat_Image=ImageTk.PhotoImage(image)
        directory_repeat_button=tk.Button(master, text="フォルダリピート", fg = "purple", image=self.directory_repeat_Image,font=("",20))
        image = Image.open("img/1曲リピート.png").resize((50, 50))
        self.one_repeat_Image=ImageTk.PhotoImage(image)
        one_repeat_button=tk.Button(master, text="1曲リピート", fg = "purple", image=self.one_repeat_Image,font=("",20))

        backbutton['command']=partial(backgroundprocess,kb=b'b',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        backbutton.grid(row=5, column=0, padx=10, pady=10)
        nextbutton['command']=partial(backgroundprocess,kb=b'n',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        nextbutton.grid(row=5, column=5, padx=10, pady=10)
        shuffle_button['command']=partial(backgroundprocess,kb=b'z',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        shuffle_button.grid(row=0, column=5, padx=10, pady=10)
        directory_repeat_button['command']=partial(backgroundprocess,kb=b'x',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        directory_repeat_button.grid(row=2, column=5, padx=10, pady=10)
        one_repeat_button['command']=partial(backgroundprocess,kb=b'c',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button)
        one_repeat_button.grid(row=4, column=5, padx=10, pady=10)
        master.bind("<Control-Shift-Left>",partial(backgroundprocess,kb=b'b',shuffle_button=shuffle_button,directory_repeat_button=directory_repeat_button,one_repeat_button=one_repeat_button))
        master.bind("<Control-Shift-Right>",partial(backgroundprocess,kb=b'n'))

        scaleframe = ttk.Frame(master,padding=10)
        first_label=tk.Label(scaleframe, text="first",font=("",20))
        first_label.pack(side=tk.LEFT)
        val = DoubleVar()
        self.scalebar = ttk.Scale(
            scaleframe,
            variable=val,
            orient=HORIZONTAL,
            length=700,
            from_=0,
            to=info.duration,
            command=partial(backgroundprocess,scaleint=val))
        position=pos_renew(master,self.scalebar)
        position.renewposition()
        self.scalebar.pack(side=tk.LEFT)
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
            command=partial(self.volumeset,volumeval.get()))
        volumescalebar.pack(side=tk.LEFT)
        volume_label_100=tk.Label(volumescaleframe, text="100")
        volume_label_100.pack(side=tk.RIGHT)
        volumescaleframe.grid(row=0,column=3,columnspan=2,sticky=(E))
        master.bind("<Control-Shift-O>",self.shortcut_dirplay)
        master.bind("<Control-o>",self.shortcut_fileplay)
        self.menu_create()
    def shortcut_dirplay(self,event=None):
        iDir = os.path.abspath(os.path.dirname("__file__")+"../")
        #iDirPath = filedialog.askdirectory(initialdir = info.basedirname+"/../")
        iDirPath = filedialog.askdirectory(initialdir = iDir+"/../")
        if iDirPath !='':
            if os.path.isdir(iDirPath):
                self.quitandplay(directoryname=iDirPath)
            else:
                messagebox.showinfo('エラー', '指定されたパスが存在しません')
    def shortcut_fileplay(self,event=None):
        fTyp = [("", "*")]
        iFile = os.path.abspath(os.path.dirname("__file__")+"../")
        iFilePath = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile+"/../")
        if iFilePath !='':
            if os.path.isfile(iFilePath):
                self.quitandplay(directoryname=iFilePath)
            else:
                messagebox.showinfo('エラー', '指定されたパスが存在しません')
    def volumeset(self,dummy,volume):
        info.volume=volume
        info.renew_flag=True
    def showplayviews(self):
        master=tk.Tk()
        master.title("再生回数")
        for i in range(len(info.playviews)):
            tk.Label(master, text=str(info.playviews[i+1][0])+'→'+str(info.playviews[i+1][1])+'回').pack(side='top',anchor=tk.E)
        master.mainloop()
    def showplayviews_top10(self):
        master=tk.Tk()
        master.title("再生回数トップ10!(プレイリスト内の曲のみ)")
        sorted_playviews = sorted(info.playviews.items(), key=lambda x:x[1][1],reverse=True)
        for i in range(min(10,len(sorted_playviews))):
            tk.Label(master, text=str(sorted_playviews[i][1][0])+'→'+str(sorted_playviews[i][1][1])+'回').pack(side='top',anchor=tk.E)
        master.mainloop()
    def showallplayviews_top10(self):
        if info.thread_play is not None:
            master=tk.Tk()
            master.title("再生回数トップ10!(すべてのプレイリストの曲)")
            unsorted_allplayviews=info.allplayviews
            for i in range(info.playlist_len):
                if info.playviews[i+1][1]!=0:
                    if info.playviews[i+1][0] in info.allplayviews:
                        if info.allplayviews[info.playviews[i+1][0]]!=info.playviews[i+1][1]:
                            unsorted_allplayviews[info.playviews[i+1][0]]=info.playviews[i+1][1]
                    else:
                        unsorted_allplayviews[info.playviews[i+1][0]]=info.playviews[i+1][1]

            sorted_allplayviews = sorted(info.allplayviews.items(), key=lambda x:x[1],reverse=True)
            if len(sorted_allplayviews)!=0:
                for i in range(min(10,len(sorted_allplayviews))):
                    tk.Label(master, text=str(sorted_allplayviews[i][0])+'→'+str(sorted_allplayviews[i][1])+'回').pack(side='top',anchor=tk.E)
            else:
                tk.Label(master, text='再生した曲がありません').pack(side='top',anchor=tk.E)
            master.mainloop()
        else:
            master=tk.Tk()
            master.title("再生回数トップ10!(すべてのプレイリスト)")
            info.Reload_allplayviews()
            sorted_allplayviews = sorted(info.allplayviews.items(), key=lambda x:x[1],reverse=True)
            if len(sorted_allplayviews)!=0:
                for i in range(min(10,len(sorted_allplayviews))):
                    tk.Label(master, text=str(sorted_allplayviews[i][0])+'→'+str(sorted_allplayviews[i][1])+'回').pack(side='top',anchor=tk.E)
            else:
                tk.Label(master, text='再生した曲がありません').pack(side='top',anchor=tk.E)
            master.mainloop()

    def deletepickle(self):
        if len(info.allplayviews)!=0:
            delflag = messagebox.askyesno('確認', '再生回数をリセットします。よろしいですか？')
            if delflag:
                os.remove(info.basedirname+"/PickleData/MusicPlayApp_allplayviews.pickle")
                messagebox.showinfo('リセット完了', '再生回数をリセットしました')
        else:
            messagebox.showinfo('エラー', '再生した曲がありません')
    def quitandplay(self,event=None,directoryname=None):
        if info.song is not None and info.thread_play is not None:
            delflag = messagebox.askyesno('確認', '別のプレイリスト('+str(directoryname)+')を再生するには今のプレイリストを終了します。よろしいですか？')
            if delflag:
                info.next_play_index=info.playlist_len+2
                info.back_flag=False
                info.quit=True
            else:
                return
        self.master.after(100,self.MusicPlay,directoryname)
    def MusicPlay(self,directoryname):
        if info.thread_play is not None:
            self.master.after(100,self.MusicPlay,directoryname)
        if info.thread_play is None :
            if os.path.isdir(directoryname):
                info.mode=1
            elif os.path.isfile(directoryname):
                info.mode=2
            info.targetname_str=directoryname
            info.song=None
            info.thread_play=PlayThread()
            info.thread_play.start()

    def show_latestopendirectory(self):
        second_menu=Menu(self.menu_playlist_open,tearoff=0)
        self.menu_playlist_open.entryconfigure(0, menu=second_menu)#更新
        if os.path.exists(info.basedirname+'/PickleData/Latest5Directory.pickle'):
            with open(info.basedirname+'/PickleData/Latest5Directory.pickle', 'rb') as f:
                Latest5Directory=pickle.load(f)
            for im,name in enumerate(Latest5Directory):
                second_menu.add_command(label = name, command = partial(self.quitandplay,directoryname=name),under=5)
    def add_favoritedirectory(self):
        if os.path.exists(info.basedirname+'/PickleData/FavoriteDirectory.pickle'):
            with open(info.basedirname+'/PickleData/FavoriteDirectory.pickle', 'rb') as f:
                FavoriteDirectory=pickle.load(f)
        else:
            FavoriteDirectory=[]
        if info.targetname_str in FavoriteDirectory:
            FavoriteDirectory.remove(info.targetname_str)
        #FavoriteDirectory.insert(0,info.targetname_str)
        FavoriteDirectory.append(info.targetname_str)
        with open(info.basedirname+'/PickleData/FavoriteDirectory.pickle','wb') as f:
            pickle.dump(FavoriteDirectory,f)
        self.show_favoritedirectory()
    def delete_favoritedirectory(self,name,menu):
        id=0
        while True:
            i_label=menu.entrycget(id,"label")
            if i_label==name:
                break
            else:
                id+=1
        delflag = messagebox.askyesno('確認', name+'をお気に入りフォルダから削除します。よろしいですか？')
        if delflag:
            menu.delete(id)#削除
            messagebox.showinfo('削除完了', name+'をお気に入りフォルダから削除しました')
            if os.path.exists(info.basedirname+'/PickleData/FavoriteDirectory.pickle'):
                with open(info.basedirname+'/PickleData/FavoriteDirectory.pickle', 'rb') as f:
                    FavoriteDirectory=pickle.load(f)
                FavoriteDirectory.remove(name)
                with open(info.basedirname+'/PickleData/FavoriteDirectory.pickle','wb') as f:
                    pickle.dump(FavoriteDirectory,f)
        self.show_favoritedirectory()
    def show_favoritedirectory(self):
        second_menu=Menu(self.menu_playlist_open,tearoff=0)
        self.menu_playlist_open.entryconfigure(3, menu=second_menu)#更新
        if os.path.exists(info.basedirname+'/PickleData/FavoriteDirectory.pickle'):
            with open(info.basedirname+'/PickleData/FavoriteDirectory.pickle', 'rb') as f:
                FavoriteDirectory=pickle.load(f)
            for im,name in enumerate(FavoriteDirectory):
                third_menu=Menu(self.menu_playlist_open,tearoff=0)
                second_menu.add_cascade(label = name,under=5,menu=third_menu)
                if im<9:
                    third_menu.add_command(label="再生",command = partial(self.quitandplay,directoryname=name),under=5,accelerator="Ctrl+"+str(im+1))
                elif im==9:
                    third_menu.add_command(label="再生",command = partial(self.quitandplay,directoryname=name),under=5,accelerator="Ctrl+0")
                else:
                    third_menu.add_command(label="再生",command = partial(self.quitandplay,directoryname=name),under=5)
                #self.master.bind("<Control-"+str(im)+">",partial(self.quitandplay,name))
                if im<9:
                    self.master.bind("<Control-KeyPress-"+str(im+1)+">",partial(self.quitandplay,directoryname=name))
                elif im==9:
                    self.master.bind("<Control-KeyPress-0>",partial(self.quitandplay,directoryname=name))
                third_menu.add_command(label="削除",command = partial(self.delete_favoritedirectory,name=name,menu=second_menu),under=5)
            for i in range(im+1,10):
                if i<9:
                    self.master.bind("<Control-KeyPress-"+str(i+1)+">", (lambda: 'pass')())
                elif i==9:
                    self.master.bind("<Control-KeyPress-0>", (lambda: 'pass')())

    def show_outputdevice(self):
        second_menu=Menu(self.device,tearoff=0)
        self.device.entryconfigure(0, menu=second_menu)#更新
        if len(outputdevicelist)==0:
            pass
        elif len(outputdevicelist)==1:
            info.outputdeviceindex=IntVar(value=outputdevicelist[0]['index'])
            second_menu.add_radiobutton(label = outputdevicelist[0]['name'], command = partial(OutputDeviceRead,outputdeviceInputClass=None),under=5,variable=info.outputdeviceindex,value=outputdevicelist[0]['index'])
            #info.outputdeviceindex=outputdevicelist[0]['index']
        elif len(outputdevicelist)>=2:
            info.outputdeviceindex=IntVar(value=outputdevicelist[0]['index'])
            for i in range(len(outputdevicelist)):
                second_menu.add_radiobutton(label = outputdevicelist[i]['name'], command = partial(OutputDeviceRead,outputdeviceInputClass=None),under=5,variable=info.outputdeviceindex,value=outputdevicelist[i]['index'])

    def menu_create(self):
        self.menu_ROOT = Menu(self.master)

        self.menu_FILE = Menu(self.menu_ROOT, tearoff = False)
        self.menu_EDIT = Menu(self.menu_ROOT, tearoff = False)
        self.menu_playlist = Menu(self.menu_ROOT, tearoff = False)
        self.menu_Ranking = Menu(self.menu_ROOT, tearoff = False)
        self.menu_playlist_open = Menu(self.menu_ROOT, tearoff = False)
        self.device = Menu(self.menu_ROOT, tearoff = False)

        self.master.configure(menu = self.menu_ROOT)

        info.algorithmvar = StringVar(value=1)

        self.menu_ROOT.add_cascade(label = 'アルゴリズム(A)', under = 0, menu = self.menu_FILE,underline=7)
        self.menu_FILE.add_radiobutton(label = 'libosa', command = lambda:setalgorithm(algorithm_num=1),variable=info.algorithmvar,value=1)
        self.menu_FILE.add_radiobutton(label = '愚直アルゴリズム', command = lambda:setalgorithm(algorithm_num=0),variable=info.algorithmvar,value=0)

        info.isfavoritevar = StringVar(value=0)

        self.menu_ROOT.add_cascade(label = '再生モード(M)', under = 0, menu = self.menu_EDIT,underline=6)
        self.menu_EDIT.add_radiobutton(label = '通常', command = lambda:setisfavorite(isfavorite_num=0),variable=info.isfavoritevar,value=0)
        self.menu_EDIT.add_radiobutton(label = 'お気に入りのみ', command = lambda:setisfavorite(isfavorite_num=1,isfavoritevar=info.isfavoritevar),variable=info.isfavoritevar,value=1)

        self.menu_ROOT.add_cascade(label = '次に再生(N)', under = 0, menu = self.menu_playlist,underline=5)

        self.menu_ROOT.add_cascade(label = 'ランキング(R)', under = 0, menu = self.menu_Ranking,underline=6)
        self.menu_Ranking.add_command(label = '再生回数表示', command = lambda:self.showplayviews() if info.thread_play is not None else messagebox.showinfo('エラー', '音楽再生中にしか使用できません'))
        self.menu_Ranking.add_command(label = '再生回数トップ10!(このプレイリスト)', command = lambda:self.showplayviews_top10() if info.thread_play is not None else messagebox.showinfo('エラー', '音楽再生中にしか使用できません'))
        self.menu_Ranking.add_command(label = '再生回数トップ10!(すべてのプレイリスト)', command = lambda:self.showallplayviews_top10())
        self.menu_Ranking.add_command(label = '再生回数をリセット', command = lambda:self.deletepickle() if info.thread_play is None else messagebox.showinfo('エラー', 'プレイリストを終了してください'))

        self.menu_ROOT.add_cascade(label = 'プレイリスト(P)', under = 0, menu = self.menu_playlist_open,underline=7)
        #self.master.bind("<Control-KeyPress-p>", self.menu_playlist_open)
        self.menu_playlist_open.add_cascade(label = '最近開いたフォルダから開く')
        self.menu_playlist_open.entryconfigure(0, command= lambda:self.show_latestopendirectory() if info.thread_play is None else messagebox.showinfo('エラー', 'プレイリストを終了してください'))#更新
        self.menu_playlist_open.add_command(label = '再生', command = start_playthread)
        self.menu_playlist_open.add_command(label = '現在再生中のフォルダをお気に入りに登録', command = lambda:self.add_favoritedirectory() if info.thread_play is not None else messagebox.showinfo('エラー', 'プレイリストを開始してください'))
        self.menu_playlist_open.add_cascade(label = 'お気に入りフォルダ', command = self.show_favoritedirectory)
        self.menu_ROOT.add_cascade(label = 'デバイス(D)', under = 0, menu = self.device,underline=5)
        self.device.add_cascade(label = '出力デバイス選択')
        if info.thread_play is None:
            self.show_latestopendirectory()
            self.show_favoritedirectory()
            self.show_outputdevice()

class pos_renew():
    root,scalebar=None,None
    def __init__(self,root,scalebar):
        self.root=root
        self.scalebar=scalebar
    def renewposition(self):
        if (info.thread_play is not None) and (info.head is not None) and (info.song is not None):
            val = DoubleVar(master=self.root,value=int((info.song.wf.tell()-info.head)/(info.last-info.head)*info.duration))
            self.scalebar['variable']=val
            self.scalebar['to']=info.duration
            self.scalebar['command']=partial(backgroundprocess,scaleint=val)
        self.root.after(100,self.renewposition)
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
    info.Window = WinodwClass(master = info.root)
    info.Window.mainloop()

class getplaytime():
    root,label=None,None
    def __init__(self,root,label):
        self.root=root
        self.label=label
    def renewplaytime(self):
        if (info.thread_play is not None) and (info.head is not None) and (info.song is not None):
            currentminutes,currentseconds=divmod((info.song.wf.tell()-info.head)/(info.last-info.head)*info.duration,60)
            lastminutes,lastseconds=divmod(info.duration,60)
            #info.label['text']=str('{:.2f}'.format((info.song.wf.tell()-info.head)/(info.last-info.head)*info.duration))+"s/"+str('{:.2f}'.format(info.duration))+"s" #秒出力
            self.label['text']=str(int(currentminutes))+str(':{:05.2f}'.format(currentseconds))+"/"+str(int(lastminutes))+str(':{:05.2f}'.format(lastseconds)) #分出力
        self.root.after(100,self.renewplaytime)

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
            self.buttons.append(tk.Button(self.interior, text=str(i+1)+": "+target, command=partial(backgroundprocess,kb=i+1)))
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

class PlaylistCanvas():
    popup_menu=None
    def __init__(self, playlist):
        self.start_xy = None
        self.x_y  = None
        self.popup_menu = []
        self.second_menu = []
        self.canvas = tk.Canvas(info.root)
        self.playlistframe =  ScrollFrame(master=self.canvas, playlist=playlist)
        self.canvas.grid(row=1, column=6, rowspan=5,padx=10, pady=10,sticky="WNES")
        self.canvas.create_window((0,0), window=self.playlistframe, anchor=tk.NW, width=self.canvas.cget('width'))
        self.playlistframe.interior.bind("<MouseWheel>",self.mouse_y_scroll)
        if len(playlist)>=8:
            for i in range(len(playlist)):
                self.popup_menu.append(tkinter.Menu(info.root, tearoff=0))
                self.popup_menu[i].add_command(label="「次に再生」リストに追加",
                                           command=partial(self.add_nextplaylist,i=i))
                self.popup_menu[i].add_command(label="お気に入り登録/解除",
                                           command=partial(self.favoritesong,i=i))
                self.playlistframe.buttons[i].bind("<MouseWheel>", self.mouse_y_scroll)
                self.playlistframe.buttons[i].bind("<Button-3>", partial(self.popup,i))
                self.playlistframe.buttons[i].bind("<Button-2>", partial(self.favoritesong,i=i))
    def setactive(self):
        for x in range(len(self.playlistframe.buttons)):
            self.playlistframe.buttons[x].configure(state=tk.NORMAL)
    def popup(self, i,event):
        try:
            for x in range(len(self.playlistframe.buttons)):
                self.playlistframe.buttons[x].configure(state=tk.DISABLED)
            self.popup_menu[i].tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu[i].grab_release()
            self.playlistframe.buttons[i].after(10,self.setactive)
    def getCanvas(self):
        return self.canvas
    def getButtonList(self):
        return self.playlistframe.buttons
    def deletesong_fromnextplayindexlist(self,event=None,i=None):
        del info.next_play_index_list[i]
        info.Window.menu_playlist.delete(i)#削除
        del self.second_menu[i]
        while True:
            if i==len(info.next_play_index_list):
                break
            else:
                i_label=info.Window.menu_playlist.entrycget(i,"label")
                info.canvas.second_menu[i].entryconfigure(0, command=partial(info.canvas.deletesong_fromnextplayindexlist,i=i))#更新
                if (i+1)%10==1:
                    ordinal_end='st'
                elif (i+1)%10==2:
                    ordinal_end='nd'
                elif (i+1)%10==3:
                    ordinal_end='rd'
                else:
                    ordinal_end='th'
                info.Window.menu_playlist.entryconfigure(i,label=str(int(i)+1)+ordinal_end+'→'+i_label[i_label.find('→')+1:])
                i+=1
        if len(info.next_play_index_list)!=0:
            info.Window.menu_ROOT.entryconfigure(3, label="次に再生(N)("+str(len(info.next_play_index_list))+")")#更新
        else:
            info.Window.menu_ROOT.entryconfigure(3, label='次に再生(N)')#更新
    def add_nextplaylist(self, event=None,i=None):
        if info.isfavorite==0 or (info.isfavorite==1 and info.favorite_songlist[i]==1):
            self.playlistframe.buttons[i].after(100,lambda: self.playlistframe.buttons[i].configure(state=tk.DISABLED))
            info.next_play_index_list.append(i+1)
            self.second_menu.append(Menu(info.Window.menu_playlist,tearoff=0))
            if len(info.next_play_index_list)%10==1:
                ordinal_end='st'
            elif len(info.next_play_index_list)%10==2:
                ordinal_end='nd'
            elif len(info.next_play_index_list)%10==3:
                ordinal_end='rd'
            else:
                ordinal_end='th'
            if self.playlistframe.buttons[i]['text'][0]=='♥':
                info.Window.menu_playlist.add_cascade(label = str(len(info.next_play_index_list))+ordinal_end+'→'+self.playlistframe.buttons[i]['text'][1:],menu=self.second_menu[-1],under=5)
            else:
                info.Window.menu_playlist.add_cascade(label = str(len(info.next_play_index_list))+ordinal_end+'→'+self.playlistframe.buttons[i]['text'],menu=self.second_menu[-1],under=5)
            self.second_menu[-1].add_command(label='リストから削除',under=4,command=partial(self.deletesong_fromnextplayindexlist,i=len(info.next_play_index_list)-1))
            if len(info.next_play_index_list)!=0:
                info.Window.menu_ROOT.entryconfigure(3, label="次に再生(N)("+str(len(info.next_play_index_list))+")")#更新
            else:
                info.Window.menu_ROOT.entryconfigure(3, label='次に再生(N)')#更新
            if self.playlistframe.buttons[i]['bg']=='yellow':
                self.playlistframe.buttons[i]['bg']='red'
                self.playlistframe.buttons[i].after(100,lambda: self.playlistframe.buttons[i].configure(bg='yellow'))
                self.playlistframe.buttons[i].after(200,lambda: self.playlistframe.buttons[i].configure(bg='red'))
                self.playlistframe.buttons[i].after(300,lambda: self.playlistframe.buttons[i].configure(bg='yellow'))
                self.playlistframe.buttons[i].after(310,lambda: self.playlistframe.buttons[i].configure(state=tk.NORMAL))
            if self.playlistframe.buttons[i]['bg']=='pink':
                self.playlistframe.buttons[i]['bg']='red'
                self.playlistframe.buttons[i].after(100,lambda: self.playlistframe.buttons[i].configure(bg='pink'))
                self.playlistframe.buttons[i].after(200,lambda: self.playlistframe.buttons[i].configure(bg='red'))
                self.playlistframe.buttons[i].after(300,lambda: self.playlistframe.buttons[i].configure(bg='pink'))
                self.playlistframe.buttons[i].after(310,lambda: self.playlistframe.buttons[i].configure(state=tk.NORMAL))
            if self.playlistframe.buttons[i]['bg']=='SystemButtonFace':
                self.playlistframe.buttons[i]['bg']='red'
                self.playlistframe.buttons[i].after(100,lambda: self.playlistframe.buttons[i].configure(bg='SystemButtonFace'))
                self.playlistframe.buttons[i].after(200,lambda: self.playlistframe.buttons[i].configure(bg='red'))
                self.playlistframe.buttons[i].after(300,lambda: self.playlistframe.buttons[i].configure(bg='SystemButtonFace'))
                self.playlistframe.buttons[i].after(310,lambda: self.playlistframe.buttons[i].configure(state=tk.NORMAL))
        else:
            messagebox.showinfo('エラー', '「お気に入りのみ」モード中はお気に入り以外の曲を追加できません')
    def favoritesong(self, event=None,i=None):
        if info.favorite_songlist[i]==1:
            if sum(x==1 for x in info.favorite_songlist)==1 and info.isfavorite==1:
                messagebox.showinfo('エラー', 'お気に入りの曲は最低１曲お願いします')
            else:
                if info.isfavorite==1:
                    info.favorite_songlist[i]=0
                    id=0
                    delflag=False
                    while True:
                        i_label=info.Window.menu_playlist.entrycget(id,"label")
                        i_label=i_label[i_label.find('→')+1:i_label.find(':')]
                        if info.favorite_songlist[int(i_label)-1]==0:
                            if delflag==False:
                                delflag = messagebox.askyesno('確認', '「次に再生」リストから'+self.playlistframe.buttons[i]['text'][1:]+'が削除されます。続けますか？')
                            if delflag==True:
                                del info.next_play_index_list[id]
                                info.Window.menu_playlist.delete(id)#削除
                                del info.canvas.second_menu[id]
                                id_prime=id
                                while True:
                                    if id_prime==len(info.next_play_index_list):
                                        break
                                    else:
                                        i_label=info.Window.menu_playlist.entrycget(id_prime,"label")
                                        info.canvas.second_menu[id_prime].entryconfigure(0, command=partial(info.canvas.deletesong_fromnextplayindexlist,i=id_prime))#更新
                                        if (id_prime+1)%10==1:
                                            ordinal_end='st'
                                        elif (id_prime+1)%10==2:
                                            ordinal_end='nd'
                                        elif (id_prime+1)%10==3:
                                            ordinal_end='rd'
                                        else:
                                            ordinal_end='th'
                                        info.Window.menu_playlist.entryconfigure(id_prime,label=str(int(id_prime)+1)+ordinal_end+'→'+i_label[i_label.find('→')+1:])
                                        id_prime+=1

                                if len(info.next_play_index_list)!=0:
                                    info.Window.menu_ROOT.entryconfigure(3, label="次に再生(N)("+str(len(info.next_play_index_list))+")")#更新
                                else:
                                    info.Window.menu_ROOT.entryconfigure(3, label='次に再生(N)')#更新
                            else:
                                info.favorite_songlist[i]=1
                                return
                        else:
                            id+=1
                        if id==len(info.next_play_index_list):
                            break
                    if self.playlistframe.buttons[i]['bg']=='yellow' or self.playlistframe.buttons[i]['bg']=='red':
                        pass
                    else:
                        self.playlistframe.buttons[i]['bg']='SystemButtonFace'
                    self.playlistframe.buttons[i]['text']=self.playlistframe.buttons[i]['text'][1:]
                else:
                    info.favorite_songlist[i]=0
                    if self.playlistframe.buttons[i]['bg']=='yellow' or self.playlistframe.buttons[i]['bg']=='red':
                        pass
                    else:
                        self.playlistframe.buttons[i]['bg']='SystemButtonFace'
                    self.playlistframe.buttons[i]['text']=self.playlistframe.buttons[i]['text'][1:]
        else:
            info.favorite_songlist[i]=1
            if self.playlistframe.buttons[i]['bg']=='yellow' or self.playlistframe.buttons[i]['bg']=='red':
                pass
            else:
                self.playlistframe.buttons[i]['bg']='pink'
            self.playlistframe.buttons[i]['text']='♥'+self.playlistframe.buttons[i]['text']

    def mouse_y_scroll(self, event):
        if event.delta > 0:
            self.playlistframe.canvas.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.playlistframe.canvas.yview_scroll(1, 'units')

class PlayThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        info.back_flag=False
        info.next_play_index=0
        os.chdir(info.basedirname)
        playlist=[]
        print("再生を開始します")
        print("")
        try:
            if info.targetname_str ==None:
                print("Playlistの選択")
                thread_playlisttkinter=PlayListTkinterThread()
                thread_playlisttkinter.start()
                thread_playlisttkinter.join()
            if info.targetname_str==None:
                info.thread_play=None
                return
            if not os.path.exists(info.targetname_str):
                messagebox.showinfo('エラー', 'パスが存在しません。')
                info.thread_play=None
                return
            if info.targetname_str != None and info.mode!=-1:
                if info.mode==2:
                    playfile=info.targetname_str
                else:
                    os.chdir(info.targetname_str)
                info.root.title("音楽再生アプリ("+info.targetname_str+")")
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
                    time.sleep(1)
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
            info.Reload_allplayviews()
            info.playviews=dict()
            for i in range(len(playlist)):
                if playlist[i] in info.allplayviews:
                    info.playviews[i+1]=[playlist[i],info.allplayviews[playlist[i]]]
                else:
                    info.playviews[i+1]=[playlist[i],0]
            index=0
            info.playlist_len=len(playlist)
            info.favorite_songlist=[0]*len(playlist)
            if info.playlist_len==0:
                messagebox.showinfo('エラー', 'playlistの曲がありません')
                os.chdir("../")
                os.rmdir(playlistdirname)
                info.root.title("音楽再生アプリ")
                info.thread_play=None
                return
            if os.path.exists(info.basedirname+'/PickleData/Latest5Directory.pickle'):
                with open(info.basedirname+'/PickleData/Latest5Directory.pickle', 'rb') as f:
                    Latest5Directory=pickle.load(f)
            else:
                Latest5Directory=[]
            if info.targetname_str != None:
                if info.targetname_str in Latest5Directory:
                    Latest5Directory.remove(info.targetname_str)
                Latest5Directory.insert(0,info.targetname_str)
            if len(Latest5Directory)>5:
                Latest5Directory=Latest5Directory[:5]
            with open(info.basedirname+'/PickleData/Latest5Directory.pickle','wb') as f:
                pickle.dump(Latest5Directory,f)
            info.Window.show_latestopendirectory()
            #canvas処理
            info.canvas=PlaylistCanvas(playlist=playlist)
            buttons=info.canvas.getButtonList()
            canvas=info.canvas.getCanvas()
            while True:
                if info.isfavorite==1:
                    if 1 in info.favorite_songlist[index:] and info.isfavorite==1:
                        index=index+info.favorite_songlist[index:].index(1)
                    else:
                        print("最後です")
                        index=info.playlist_len
                        if info.directory_repeat_flag:
                            if info.isfavorite==1:
                                index=info.favorite_songlist.index(1)
                            else:
                                index=0
                        else:
                            break
                    print(index+1,"番目の",playlist[index],"を再生")
                    for i,button in enumerate(buttons):
                        if i==index:
                            button['bg']='yellow'
                        else:
                            if info.favorite_songlist[i]==1:
                                button['bg']='pink'
                            else:
                                button['bg']='SystemButtonFace'
                    playback(playlist[index],index+1)
                    if info.next_play_index!=0:
                        if info.isfavorite==1:
                            index=info.next_play_index-1
                        else:
                            index=info.next_play_index-1
                        info.next_play_index=0
                    elif len(info.next_play_index_list)!=0:
                        if info.isfavorite==1:
                            index=info.next_play_index_list[0]-1
                        else:
                            index=info.next_play_index_list[0]-1
                        del info.next_play_index_list[0]
                        info.Window.menu_playlist.delete(0)#削除
                        del info.canvas.second_menu[0]
                        id=0
                        while True:
                            if id==len(info.next_play_index_list):
                                break
                            else:
                                i_label=info.Window.menu_playlist.entrycget(id,"label")
                                info.canvas.second_menu[id].entryconfigure(0, command=partial(info.canvas.deletesong_fromnextplayindexlist,i=id))#更新
                                if (id+1)%10==1:
                                    ordinal_end='st'
                                elif (id+1)%10==2:
                                    ordinal_end='nd'
                                elif (id+1)%10==3:
                                    ordinal_end='rd'
                                else:
                                    ordinal_end='th'
                                info.Window.menu_playlist.entryconfigure(id,label=str(int(id)+1)+ordinal_end+'→'+i_label[i_label.find('→')+1:])
                                id+=1
                        if len(info.next_play_index_list)!=0:
                            info.Window.menu_ROOT.entryconfigure(3, label="次に再生(N)("+str(len(info.next_play_index_list))+")")#更新
                        else:
                            info.Window.menu_ROOT.entryconfigure(3, label='次に再生(N)')#更新
                    elif info.back_flag:
                        if 1 in info.favorite_songlist[:index] and info.isfavorite==1:
                            rev=info.favorite_songlist[:index]
                            rev.reverse()
                            index=index-rev.index(1)-1
                        else:
                            if info.isfavorite==0:
                                if index>=1:
                                    index-=1
                                else:
                                    print("最初の曲です")
                            else:
                                print("最初の曲です")
                        info.back_flag=False
                    elif info.one_repeat_flag:
                        pass
                    elif info.shuffle_flag:
                        indexes = [i for i, x in enumerate(info.favorite_songlist) if x == 1]
                        if len(indexes)!=0:
                            index=indexes[random.randint(0,len(indexes)-1)]
                        else:
                            index=random.randint(0,info.playlist_len-1)
                    else:
                        if index==len(info.favorite_songlist)-1:
                            print("最後の曲です")
                        index+=1
                    if index ==info.playlist_len and info.directory_repeat_flag:
                        index=0
                    if index>=info.playlist_len:
                        break
                else:
                    print(index+1,"番目の",playlist[index],"を再生")
                    for i,button in enumerate(buttons):
                        if i==index:
                            button['bg']='yellow'
                        else:
                            if info.favorite_songlist[i]==1:
                                button['bg']='pink'
                            else:
                                button['bg']='SystemButtonFace'
                    playback(playlist[index],index+1)
                    if info.next_play_index!=0:
                        index=info.next_play_index-1
                        info.next_play_index=0
                    elif len(info.next_play_index_list)!=0:
                        if info.isfavorite==1:
                            index=info.next_play_index_list[0]-1
                        else:
                            index=info.next_play_index_list[0]-1
                        del info.next_play_index_list[0]
                        info.Window.menu_playlist.delete(0)#削除
                        del info.canvas.second_menu[0]
                        id=0
                        while True:
                            if id==len(info.next_play_index_list):
                                break
                            else:
                                i_label=info.Window.menu_playlist.entrycget(id,"label")
                                info.canvas.second_menu[id].entryconfigure(0, command=partial(info.canvas.deletesong_fromnextplayindexlist,i=id))#更新
                                if (id+1)%10==1:
                                    ordinal_end='st'
                                elif (id+1)%10==2:
                                    ordinal_end='nd'
                                elif (id+1)%10==3:
                                    ordinal_end='rd'
                                else:
                                    ordinal_end='th'
                                info.Window.menu_playlist.entryconfigure(id,label=str(int(id)+1)+ordinal_end+'→'+i_label[i_label.find('→')+1:])
                                id+=1
                        if len(info.next_play_index_list)!=0:
                            info.Window.menu_ROOT.entryconfigure(3, label="次に再生(N)("+str(len(info.next_play_index_list))+")")#更新
                        else:
                            info.Window.menu_ROOT.entryconfigure(3, label='次に再生(N)')#更新
                    elif info.back_flag:
                        if 1 in info.favorite_songlist[:index] and info.isfavorite==1:
                            rev=info.favorite_songlist[:index]
                            rev.reverse()
                            index=index-rev.index(1)-1
                        else:
                            if info.isfavorite==0:
                                if index>=1:
                                    index-=1
                                else:
                                    print("最初の曲です")
                            else:
                                print("最初の曲です")
                        info.back_flag=False
                    elif info.one_repeat_flag:
                        pass
                    elif info.shuffle_flag:
                        indexes = [i for i, x in enumerate(info.favorite_songlist) if x == 1]
                        if len(indexes)!=0:
                            index=indexes[random.randint(0,len(indexes)-1)]
                        else:
                            index=random.randint(0,info.playlist_len-1)
                    else:
                        if index==info.playlist_len-1:
                            print("最後の曲です")
                        index+=1
                    if index ==info.playlist_len and info.directory_repeat_flag:
                        index=0
                    if index>=info.playlist_len:
                        break
        print("Playlistが終了しました")
        info.favorite_songlist.clear()
        for i in range(len(info.next_play_index_list)):
            del info.next_play_index_list[0]
            info.Window.menu_playlist.delete(0)#削除
            del info.canvas.second_menu[0]
        info.Window.menu_ROOT.entryconfigure(3, label='次に再生(N)')#更新
        info.isfavorite=0
        info.isfavoritevar.set(0)
        canvas.grid_forget()
        info.root.title("音楽再生アプリ")
        info.Window.label['text']='--s/--s'
        for i in range(len(playlist)):
            if info.playviews[i+1][1]!=0:
                info.allplayviews[info.playviews[i+1][0]]=info.playviews[i+1][1]
        if len(info.allplayviews)!=0:
            with open(info.basedirname+'/PickleData/MusicPlayApp_allplayviews.pickle','wb') as f:
                pickle.dump(info.allplayviews,f)
        info.mode=-1
        info.targetname_0=None #パス指定のentry
        info.targetname_1=None #フォルダ指定のentry
        info.targetname_2=None #ファイル指定のentry
        info.targetname_str=None #パス指定のentry
        info.thread_play=None
def start_windowthread():
    thread_window=WindowThread()
    thread_window.start()

def start_playthread():
    if info.song is not None and info.thread_play is not None:
        delflag = messagebox.askyesno('確認', '別のプレイリストを再生するには今のプレイリストを終了します。よろしいですか？')
        if delflag:
            info.next_play_index=info.playlist_len+2
            info.back_flag=False
            info.quit=True
        else:
            return
    info.Window.master.after(100,start_playthread2)
def start_playthread2():
    if info.thread_play is not None:
        print("待機")
        info.Window.master.after(100,start_playthread2)
    if info.thread_play is None :
        info.song=None
        info.thread_play=PlayThread()
        info.thread_play.start()
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
    p=pyaudio.PyAudio()
    outputdevicelist=[]
    for index in range(0,p.get_device_count()):
        if p.get_device_info_by_index(index)['hostApi']==0 and p.get_device_info_by_index(index)['maxOutputChannels']==2:
            outputdevicelist.append(p.get_device_info_by_index(index))
    help()
    r = 2**(1/12)
    info.r12=(2**(1/12))**np.float(info.Key)
    start_windowthread()
