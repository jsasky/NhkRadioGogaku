import os
import re
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
import datetime
from enum import auto
from os.path import expanduser
import sys

def main():
    #OS(実行環境)依存のパラメータをセットする
    if sys.platform=='win32': #Windows
        path_delimiter="\\"
        today=datetime.date.today()
        download_dir=".\\download_" + "{0}_CW{1}".format(str(today.year),str(today.isocalendar()[1]).zfill(2))
        ffmpeg_bin=".\\win\\ffmpeg.exe"
    elif sys.platform=='darwin': #Mac
        path_delimiter="/"
        today=datetime.date.today()
        download_dir=expanduser("~")+"/Downloads/NHK語学講座"+"{0}_CW{1}".format(str(today.year),str(today.isocalendar()[1]).zfill(2))
        ffmpeg_bin="./mac/ffmpeg"
    else: #Linux(Synology-NAS)
        path_delimiter="/"
        download_dir="/volume1/music/NHK語学講座"
        ffmpeg_bin="/volume1/@appstore/ffmpeg/bin/ffmpeg"

    #各語学講座のlistdataflv.xmlのURL、講座名、ダウンロード完了済みかどうかをチェックするファイルサイズを定義する
    url_kouza_sizes = []
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/basic0/listdataflv.xml',     '小学生の基礎英語',             4801300 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/basic1/listdataflv.xml',     '中学生の基礎英語【レベル1】',   7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/basic2/listdataflv.xml',     '中学生の基礎英語【レベル2】',   7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/basic3/listdataflv.xml',     '中高生の基礎英語 in English',  7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/kaiwa/listdataflv.xml',      'ラジオ英会話',                 7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/vr-radio/listdataflv.xml',   'ボキャブライダー',             2407200 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/enjoy/listdataflv.xml',      'エンジョイ・シンプル・イングリッシュ', 7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/timetrial/listdataflv.xml',  '英会話タイムトライアル',       4801300 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/english/business1/listdataflv.xml',  'ラジオビジネス英語',           7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/french/kouza/listdataflv.xml',       'まいにちフランス語【入門編】',  7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/french/kouza2/listdataflv.xml',      'まいにちフランス語【応用編】',  7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/italian/kouza/listdataflv.xml',      'まいにちイタリア語【入門編】',  7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/italian/kouza2/listdataflv.xml',     'まいにちイタリア語【応用編】',  7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/german/kouza/listdataflv.xml',       'まいにちドイツ語【初級編】',    7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/german/kouza2/listdataflv.xml',      'まいにちドイツ語【応用編】',    7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/spanish/kouza/listdataflv.xml',      'まいにちスペイン語【入門編】',  7201000 ]]
    url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/spanish/kouza2/listdataflv.xml',     'まいにちスペイン語【応用編】',  7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/russian/kouza/listdataflv.xml',      'まいにちロシア語【入門編】',    7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/russian/kouza2/listdataflv.xml',     'まいにちロシア語【応用編】',    7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/chinese/kouza/listdataflv.xml',      'まいにち中国語',               7201000 ]]
    # url_kouza_sizes += [['https://www.nhk.or.jp/gogaku/st/xml/hangeul/kouza/listdataflv.xml',      'まいにちハングル講座',          7201000 ]]

    # ダウンロード先のフォルダがない場合はフォルダを作成する
    os.makedirs(download_dir, exist_ok=True)

    #各語学講座のストリーミングデータをダウンロードする
    for url_kouza_size in url_kouza_sizes:
        #URL/講座名(=MP3タグ名)/ファイルサイズを格納する
        url=url_kouza_size[0]
        kouza=url_kouza_size[1]
        size=url_kouza_size[2]
        # print(f"url:{url} / kouza:{kouza} / size:{size}")

        # listdataflv.xmlのコンテンツを読み出す
        listdataflv_xml = download_dir+"/listdataflv.xml"
        urllib.request.urlretrieve(url, listdataflv_xml)
        xml_tree = ET.parse(listdataflv_xml)
        os.remove(listdataflv_xml)

        # 各LessonのストリーミングデータをMP3に変換してダウンロードする
        for xml_element_music in xml_tree.findall("music"):

            # 放送年月日と年度を取得する
            month=int(re.findall(r'\d+', xml_element_music.get("hdate"))[0])
            day=int(re.findall(r'\d+', xml_element_music.get("hdate"))[1])
            nendo=int(xml_element_music.get("nendo"))
            year=datetime.date.today().year

            if (12==month):
                # 放送日が12月の場合は放送日の年を年度年に設定する
                year=nendo
            # print(f"nendo:{nendo} / year:{year} / month:{month} / day:{day}")

            # MP3に埋め込むタグ情報をセットする
            tag_title=kouza+" "+"{0}年{1}月{2}日放送分".format(year,str(month).zfill(2),str(day).zfill(2))
            tag_year=nendo
            tag_album=kouza+"["+str(nendo)+"年度]"
            # print(f"tag_title:{tag_title} / tag_year:{tag_year} / tag_album:{tag_album}")

            # MP3のダウンロードパスをセットする
            download_subdir=download_dir+path_delimiter+kouza+"["+str(nendo)+"年度]"
            os.makedirs(download_subdir, exist_ok=True)
            download_filename=kouza+" "+"{0}年{1}月{2}日放送分".format(year,str(month).zfill(2),str(day).zfill(2))+".mp3"
            download_path=download_subdir+path_delimiter+download_filename
            # print(f"download_path:{download_path}")
            # ストリーミングファイルのURLをセットする
            download_url="https://vod-stream.nhk.jp/gogaku-stream/"
            if len(xml_element_music.get("dir"))>0:
                download_url+=xml_element_music.get("dir")+"/"
            download_url+=os.path.splitext(os.path.basename(xml_element_music.get("file")))[0]+"/index.m3u8"
            # print(f"download_url:{download_url}")

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
