chcp 65001

C:\LegacyApp\Python36\python.exe RadioGogaku.py

@REM @REM @REM https://cgi2.nhk.or.jp/gogaku/st/xml/english/kaiwa/listdataflv.xml
@REM SET SERVER=https://nhks-vh.akamaihd.net/i/gogaku-stream/mp4/22-er-4235-525.mp4/master.m3u8
@REM SET FILENAME=ラジオ英会話 2022年11月11日放送分
@REM ffmpeg -http_seekable 0 -i %SERVER% -id3v2_version 3 -metadata artist="NHK" -metadata title="%FILENAME%" -metadata album="ラジオ英会話[2022年度]" -metadata date="2022" -ar 44100 -ab 64k -c:a mp3 -c:a mp3 "%FILENAME%.mp3"

pause
