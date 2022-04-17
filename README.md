# Title
* weater_report

### アプリケーション概要
* webスクレイピングにより天気予報情報を取得、LCDに表示します。
* ON(右)スイッチによりLCD表示、OFF(左)スイッチにより終了。
* 指定時間(6:30,12,30,17:30)にスクレイピングを定期実行します。
 
### 回路図
![Image]/weater_report/weather_report.png
#### 画像はRaspberryPi3になりますが、開発は4を使用したためピン配置が異なる場合があります。
#### LCDは実際の使用したものと異なります。
#### LCDピンはGND,VCC,SDA,SCLの4ピンのものを使用しています。

#### LCDピン配置
* PIN2:VCC
* PIN3:SDA
* PIN5:SCL
* PIN6:GND

#### Switchピン番号 
* PIN18:ON
* PIN23:OFF

### 開発環境
* python3/RaspberryPi4B/VSCode

### 注意点
#### スクレイピングは情報取得先サーバへの負荷となる恐れがあります。
#### folkして利用する場合はプログラム35~43行のコードをコメントアウトし、
#### 30行目のコメントアウトを解除、デバック用のコードを使用してください。

