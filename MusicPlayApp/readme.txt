音程と速度を自由に変更しながら音楽を再生します。
音源ファイルは.wav,.mp3,.mp4,.m4aに対応しています。
(注意!:エクスプローラーの名前変更等で拡張子を変更するとフォーマットが対応していないためエラーになります。)

MusicPlayApp_WithLibrosaフォルダの中のMusicPlayApp_WithLibrosa.exeを実行することでプレイヤーを開始できます。(フォルダ構造はそのままにしてください。ライブラリが参照できません)

操作方法
1.キーと速度の入力
再生するキーと速度を入力してください。この設定は後からでも変更できます。
標準再生ボタンをクリックするとキーが0、速度が1にセットされ標準再生になります。
×ボタンで閉じると標準再生と見なして次のステップへ行きます。

2.出力デバイスの選択
ユーザーの出力デバイス一覧が表示されます。使用したい出力デバイスを選択してください。
最初にチェックが入っている項目はデフォルトで使われているデバイスです。
×ボタンで閉じるとデフォルトだと見なして次のステップへ行きます。

3.ホーム画面
ホーム画面です。ほとんどの機能はプレイヤーを開始していないと使えません。(キーや速度の変更、再生モードの変更はできます。)
プレイヤーを開始する場合は「再生」ボタンを押してください。

4.プレイリストの選択
プレイヤーを開始していない状態で再生ボタンを押すとプレイリストを選択画面に移行します。
以下の3つの方法で選択できます。
a.パス指定→再生したいフォルダやファイルのパスを指定します。絶対パス、相対パスどちらでも可能です。(相対パスの場合はMusicPlayApp_WithLibrosaからの相対パスです)
カレントボタンを押すとカレントディレクトリを画面にセットします。
b.フォルダ参照→ファイルエクスプローラーを開いてフォルダを指定できます。
c.ファイル参照→ファイルエクスプローラーを開いてファイルを指定できます。
いずれの方法もその横にある再生ボタンを押すと再生できます。(同じ行の再生ボタンが対応しています。)

プレイリストとして
b.フォルダを指定した場合→そのフォルダの中にMusicPlayApp_Playlistというフォルダを作成しプレイリストを作成します。
c.ファイルを指定した場合→ MusicPlayApp_WithLibrosaフォルダの中にMusicPlayApp_Playlist_{曲名}というフォルダを作成し、プレイリストを作成します。
予めこのような名前のフォルダが作成されているとうまく動きません。

5.再生
再生ボタンを押すとそのパスの中のチェックが始まります。(最初は対象ファイルの変換等の作業があるので多少処理が長くなります。)
ボタンやバーの操作の仕方は基本的にボタンに書いてあるとおりです。
下のバーは再生位置を示していて動かすとその地点までジャンプします。
右には再生リストが並んでいて曲名をクリックするとその曲を再生します。
左上のチェック項目に関して
librosa:高性能オーディオライブラリlibrosaを用いてピッチシフト、タイムストレッチを行います。応答時間が多少かかります(1s弱)。
愚直アルゴリズム:numpyを使ってバイナリを操作するフルスクラッチでの実装です。応答時間が非常に速いです。

6.終了
exitボタンで終了します。
exitボタンはプレイリスト再生中に押すとプレイリストが終了し、プレイリストを再生していないときに押すとプログラムが終了します。
→再生中にプログラムを終了させたいときはexitボタンを2回押す必要があります。
