# open_mv_tags_tracking
タグ（マーカー）をトラッキングするプログラムの試作

### find_apriltags_3d_pose_1.py
OpenMV Cam側のコード，openMVカメラで実行する

### read_serial.js
OpenMV CamをマイクロUSB接続したPCで実行

`node read_serial.js`

位置情報をシリアル通信経由で取得できる

### OpenMVカメラ M7
 SwitchScience
- https://www.switch-science.com/catalog/3301/


製品情報
- https://openmv.io/products/openmv-cam-m7
   - Frame Differencing
   - Color Tracking
   - Marker Tracking
   - Face Detection
   - Eye Tracking
   - Optical Flow
   - QR Code Detection/Decoding
   - Data Matrix Detection/Decoding
   - Linear Barcode Decoding
   - AprilTag Tracking
   - Line Detection
   - Circle Detection
   - Rectangle Detection
   - Template Matching
   - Image Capture
   - Video Recording


### こんな使い方ができる　まとめ
- https://togetter.com/li/1144157
- https://twitter.com/i/web/status/900621761523269633


## 準備

OpenMV IDEをインストール
- https://openmv.io/pages/download

チュートリアルに沿ってセットアップ
- http://docs.openmv.io/openmvcam/tutorial/index.html


## OpenMV IDE

 1. ソフトウェア
	Windowsの場合
	- 必要なものは自動的にインストールされているので特に作業なし

  Mac の場合
  - OpenMV IDE .app をインストール
  - HomeBrewがある人は
    - `sudo brew install libusb python`
    - `sudo pip install pyusb`
    - pipがないよと言われる場合
      - `sudo easy_install pip`

 2. ハードウェア（カメラ）
  - マイクロUSBケーブルでPCに接続
  - カメラが青く点滅（最初の方に緑，ときどき赤が入る？）
  - USBポートに認識される
  - OpenMV IDEを起動
  - OpenMV IDEとカメラを接続
  - 左下のアイコン（ケーブル接続っぽい）を押すと接続
  - 接続できない場合はUSBポートに認識されているかチェック．マイクロUSBケーブルを接続し直すか，ケーブルを変える
  - OpenMV IDEでプログラムを実行
    - 左下の再生マークを押すとデフォルトの`helloworld_1.py`が実行される
    - 右側にカメラの映像やヒストグラムが表示される
  - ピントがずれている場合
    - カメラレンズ側面のネジを緩める
    - カメラレンズを回して，伸ばしたり縮めたりすることでピントを変える
    ネジで再度固定する
   - 動かない場合，もしかするとファームウェアが古いのでアップデートする
    - OpenMV IDE下側にFireware Versionが書いてあるところをクリックするとアップデートできる



### マーカの認識
マーカの生成
- OpenMV IDEのツールメニュー
- Machine Vision / April Tag Generator / TAG36H11 Family （Recommended）

 サンプルコード
- OpenMV IDEのファイルメニュー
- Examples / 16 - Codes / find_apriltags_3d_pose.py
  - ストリームなしで15fps（未検出時20fps），ありで13fps（未検出時15fps）ぐらい
- ３次元位置と角度取得
  - 先ほどの「TAG36H11 Family」の画像をPCで表示してカメラで映してみる
  	反応してたらマーカに合わせて赤い四角が表示される


### 使い方
Documentation for MicroPython and the OpenMV Cam
- http://docs.openmv.io/

- `pip install pyserial`

### OpenMVカメラ
- デバイスの内臓ストレージにmain.pyがある
- OpenMV IDEのツールメニュー  /  Save open script to Open MV Cam で現在のスクリプトがmain.pyに書き込まれる
- 次回デバイス起動時に自動起動する
- USBが繋がっているPCでシリアル通信を読み取るプログラムで`print( ~~ )`内の文字が読み取れる
- シリアルポート名は ターミナルで コマンド `ls /dev/tty.*`で確認できる

### Node Serial通信

通信時はOpenMV IDEは閉じる
