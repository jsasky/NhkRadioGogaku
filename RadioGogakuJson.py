import os
import urllib.request
import subprocess
import datetime
from os.path import expanduser
import sys
import json

def main():
    #OS(実行環境)依存のパラメータをセットする
    if sys.platform=='win32': #Windows
        path_delimiter="\\"
        today=datetime.date.today()
        download_dir=".\\download_" + "{0}_CW{1}".format(str(today.year),str(today.isocalendar()[1]).zfill(2))
        ffmpeg_bin=".\\ffmpeg.exe"
    elif sys.platform=='darwin': #Mac
        path_delimiter="/"
        today=datetime.date.today()
        download_dir=expanduser("~")+"/Downloads/NHK語学講座"+"{0}_CW{1}".format(str(today.year),str(today.isocalendar()[1]).zfill(2))
        ffmpeg_bin="/opt/homebrew/bin/ffmpeg"
    else: #Linux(Synology-NAS)
        path_delimiter="/"
        download_dir="/volume1/music/NHK語学講座"
        ffmpeg_bin="/volume1/@appstore/ffmpeg/bin/ffmpeg"

    #各語学講座のjsonのURL、講座名、ダウンロード完了済みかどうかをチェックするファイルサイズ、MP3タイトルタグから消去するプレフィックス文字列を定義する
    url_kouza_sizes  = [['https://www.nhk.or.jp/radioondemand/json/7512/bangumi_7512_01.json', 'ニュースで英会話',  7201000, 'ニュースで学ぶ「現代英語」\u3000' ]]

    # ダウンロード先のフォルダがない場合はフォルダを作成する
    os.makedirs(download_dir, exist_ok=True)

    #各語学講座のストリーミングデータをダウンロードする
    for url_kouza_size in url_kouza_sizes:
        #URL/講座名(=MP3タグ名)/ファイルサイズを格納する
        url=url_kouza_size[0]
        kouza=url_kouza_size[1]
        size=url_kouza_size[2]
        title_replace=url_kouza_size[3]
        # print(f"url:{url} / kouza:{kouza} / size:{size}")

        # listdataflv.xmlのコンテンツを読み出す
        bangumi_json = download_dir+"/bangumi.json"
        urllib.request.urlretrieve(url, bangumi_json)
        with open(bangumi_json,'r',encoding="utf-8") as f:
            json_dict = json.load(f)
        os.remove(bangumi_json)

        # 各LessonのストリーミングデータをMP3に変換してダウンロードする
        for json_element in json_dict.values():
            for json_program in json_element['detail_list']:
                #放送年月日を取得する
                month=int(json_program['file_list'][0]['aa_vinfo3'][4:6])
                day=int(json_program['file_list'][0]['aa_vinfo3'][6:8])
                year=int(json_program['file_list'][0]['aa_vinfo3'][0:4])
                if month<4:
                    nendo=year-1
                else:
                    nendo=year
                contents=json_program['file_list'][0]['file_title'].replace(title_replace, '').replace('\u3000',' ')
                print(f"year:{year} / month:{month} / day:{day} / content:{contents}")

                # MP3に埋め込むタグ情報をセットする
                tag_title=kouza+" "+"{0}年{1}月{2}日放送分「{3}」".format(year,str(month).zfill(2),str(day).zfill(2),contents)
                tag_year=nendo
                tag_album=kouza+"["+str(nendo)+"年度]"
                print(f"tag_title:{tag_title} / tag_year:{tag_year} / tag_album:{tag_album}")

                # MP3のダウンロードパスをセットする
                download_subdir=download_dir+path_delimiter+kouza+"["+str(nendo)+"年度]"
                os.makedirs(download_subdir, exist_ok=True)
                download_filename=kouza+" "+"{0}年{1}月{2}日放送分".format(year,str(month).zfill(2),str(day).zfill(2))+".mp3"
                download_path=download_subdir+path_delimiter+download_filename
                print(f"download_path:{download_path}")
                # ストリーミングファイルのURLをセットする
                download_url=json_program['file_list'][0]['file_name']
                print(f"download_url:{download_url}")

                # ffmpegのダウンロード処理用コマンドラインを生成する
                command_line=f"{ffmpeg_bin}" \
                            f" -http_seekable 0" \
                            f" -i {download_url}" \
                            f" -id3v2_version 3" \
                            f" -metadata artist=\"NHK\" -metadata title=\"{tag_title}\"" \
                            f" -metadata album=\"{tag_album}\" -metadata date=\"{tag_year}\"" \
                            f" -ar 44100 -ab 64k -c:a mp3" \
                            f" \"{download_path}\""
                print(command_line)

                # ダウンロード処理を実行する
                if( os.path.isfile(download_path)):
                    # すでにダウンロード済みファイルがある場合
                    if( os.path.getsize(download_path)<=size ):
                        #ファイルサイズが想定サイズに満たないときはダウンロード処理を行う
                        os.remove(download_path)
                        subprocess.run(command_line,shell=True)
                else:
                    # ダウンロード済みファイルがない場合
                    #  -> ダウンロード処理を行う
                    subprocess.run(command_line,shell=True)

if __name__ == "__main__":
    main()
