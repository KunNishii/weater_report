import RPi.GPIO as GPIO
import i2clcda as lcd
import datetime
import time
import schedule
from time import sleep
import requests
from bs4 import BeautifulSoup
import re

#スイッチ設定
OnSwitch = 18
OffSwitch = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(OnSwitch, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(OffSwitch, GPIO.IN,pull_up_down=GPIO.PUD_UP)

#時間設定
timeToGet=('6:30','12:30','17:30')

num0fTimeToGet=len(timeToGet)
currentTime=datetime.datetime.today()
currentTimeStr=currentTime.strftime('%H:%M')

#デバック用
#currentTimeStr='08:00'

#デバック用
#result = ['4月17日(日)', '晴れ', '15℃[+2]', '0℃[-2]', '時間', '0-6', '6-12', '12-18', '18-24', '降水', '---', '---', '---', '0％', '風：', '西の風後北西の風', '波：', '---', '4月18日(月)', '曇のち雨', '13℃[-2]', '2℃[+2]', '時間', '0-6', '6-12', '12-18', '18-24', '降水', '0％', '20％', '90％', '60％', '風：', '北東の風後西の風', '波：', '---']

def GetWeather(AreaCode):
  replacements={'晴れ':'\xca\xda','曇':'\xb8\xd3\xd8','雨':'\xb1\xd2','雪':'\xd5\xb7','時々':'|','一時':'|','のち':'/','か':'/'}
  
  #スクレイピング用コード_デバック時削除
  url = "https://weather.yahoo.co.jp/weather/jp/26/" + str(AreaCode) + ".html"
  #try:
  resultall = requests.get(url) #urlを変数resultallに格納
  soup = BeautifulSoup(resultall.text, 'html.parser') #HTMLからBeautifulSoupオブジェクトを作成
  result = soup.find(class_='forecastCity')

  result = [i.strip() for i in result.text.splitlines()] #splitlines()で改行コードで分割 strip()で空白削除
  result = [i for i in result if i != ""]

  for data, kana in replacements.items():
    result[19] = result[19].replace(data, kana)

  for data, kana in replacements.items():
    result[1] = result[1].replace(data, kana)

  #日付の置き換え
  ex_today = result[0].split('日')[0] #日で分割して0番目を抽出する
  today = ex_today.replace('月','/')#list2に格納した配列の０番の月を/に置換

  ex_tomorrow = result[18].split('日')[0] #日で分割して0番目を抽出する
  tomorrow = ex_tomorrow.replace('月','/')#list2に格納した配列の０番の月を/に置換
  lcd.lcd_string(today + ' ' + result[19], lcd.LCD_LINE_1)
  lcd.lcd_string(tomorrow + ' ' + result[1], lcd.LCD_LINE_2)
GetWeather(6110)

#指定時間に情報を取得
schedule.every().day.at("06:30:00").do(GetWeather,6110)
schedule.every().day.at("12:30:00").do(GetWeather,6110)
schedule.every().day.at("17:30:00").do(GetWeather,6110)
#デバック用
schedule.every().day.at("21:26:00").do(GetWeather,6110)

while True:
  lcd.lcd_init()
  lcd.lcd_string("Weather Report", lcd.LCD_LINE_1)
  lcd.lcd_string(currentTimeStr, lcd.LCD_LINE_2)
  if GPIO.input(OnSwitch) == 0:
    lcd.lcd_init()
    GetWeather(6110)
    
    time.sleep(0.3)
    
  elif GPIO.input(OffSwitch) == 0:
    lcd.lcd_init()
    lcd.lcd_string("\xba\xde\xb1\xdd\xbe\xde\xdd\xc6", lcd.LCD_LINE_2)
    time.sleep(0.3)
    
    #GPIO.cleanup()
  schedule.run_pending()
  sleep(2)
  lcd.lcd_init()





