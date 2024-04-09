import os
import urllib.request
import subprocess
import datetime
from os.path import expanduser
import sys
import json
import unicodedata

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

    #各語学講座のjsonのURL、講座名、ダウンロード完了済みかどうかをチェックするファイルサイズ、MP3タイトルタグから消去するプレフィックス文字列を定義する
    url_kouza_size_prefix_filters  = []
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/6805/bangumi_6805_01.json', '小学生の基礎英語',           4801000, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/6806/bangumi_6806_01.json', '中学生の基礎英語レベル1',     7201000, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/6807/bangumi_6807_01.json', '中学生の基礎英語レベル2',     7201000, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/6808/bangumi_6808_01.json', '中高生の基礎英語inEnglish',  7201000, '中高生の基礎英語 in English ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/6809/bangumi_6809_01.json', 'ラジオビジネス英語',         7201000, 'ラジオビジネス英語 ', '' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0916/bangumi_0916_01.json', 'ラジオ英会話',              7201000, 'ラジオ英会話 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/2331/bangumi_2331_01.json', '英会話タイムトライアル',      4801300, '英会話タイムトライアル', '' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/7512/bangumi_7512_01.json', 'ニュースで学ぶ「現代英語」',          7201000, 'ニュースで学ぶ「現代英語」 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/4121/bangumi_4121_01.json', 'ボキャブライダー',           2407200, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0915/bangumi_0915_01.json', 'まいにち中国語',             7201000, 'まいにち中国語 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/6581/bangumi_6581_01.json', 'ステップアップ中国語',        7201000, 'ステップアップ中国語', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0951/bangumi_0951_01.json', 'まいにちハングル講座',        7201000, 'まいにちハングル講座 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/6810/bangumi_6810_01.json', 'ステップアップハングル講座',   7201000, 'ステップアップ ハングル講座 ', '' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0946/bangumi_0946_01.json', 'まいにちイタリア語【初級編】', 7201000, 'まいにちイタリア語 初級編 ', 'まいにちイタリア語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0946/bangumi_0946_01.json', 'まいにちイタリア語【応用編】',  7201000, 'まいにちイタリア語 応用編 ', 'まいにちイタリア語　応用編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0943/bangumi_0943_01.json', 'まいにちドイツ語【初級編】',    7201000, 'まいにちドイツ語 初級編 ', 'まいにちドイツ語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0943/bangumi_0943_01.json', 'まいにちドイツ語【応用編】',   7201000, 'まいにちドイツ語 応用編　', 'まいにちドイツ語　応用編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0953/bangumi_0953_01.json', 'まいにちフランス語【初級編】',  7201000, 'まいにちフランス語 初級編 ', 'まいにちフランス語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0953/bangumi_0953_01.json', 'まいにちフランス語【応用編】', 7201000, 'まいにちフランス語 応用編 ', 'まいにちフランス語　応用編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0948/bangumi_0948_01.json', 'まいにちスペイン語【初級編】',  7201000, 'まいにちスペイン語 初級編 ', 'まいにちスペイン語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0948/bangumi_0948_01.json', 'まいにちスペイン語【応用編】', 7201000, 'まいにちスペイン語 応用編 ', 'まいにちスペイン語　応用編　' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0956/bangumi_0956_01.json', 'まいにちロシア語【初級編】',    7201000, 'まいにちロシア語 初級編 ', 'まいにちロシア語　初級編　' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0956/bangumi_0956_01.json', 'まいにちロシア語【応用編】',   7201000, 'まいにちロシア語 応用編 ', 'まいにちロシア語　応用編　' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/0937/bangumi_0937_01.json', 'アラビア語講座',              7201000, 'アラビア語講座 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radioondemand/json/2769/bangumi_2769_01.json', 'ポルトガル語講座【入門編】',     7201000, 'ポルトガル語講座 入門 ', '' ]]

    # ダウンロード先のフォルダがない場合はフォルダを作成する
    os.makedirs(download_dir, exist_ok=True)

    #各語学講座のストリーミングデータをダウンロードする
    for url_kouza_size_prefix_filter in url_kouza_size_prefix_filters:
        #URL/講座名(=MP3タグ名)/ファイルサイズを格納する
        url=url_kouza_size_prefix_filter[0]
        kouza=url_kouza_size_prefix_filter[1]
        size=url_kouza_size_prefix_filter[2]
        title_replace=url_kouza_size_prefix_filter[3]
        filter=url_kouza_size_prefix_filter[4]
        # print(f"url:{url} / kouza:{kouza} / size:{size} / title_replace:{title_replace} / filter:{filter}")

        # JSONコンテンツを読み出す
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
                contents=json_program['file_list'][0]['file_title']
                # print(f"year:{year} / month:{month} / day:{day} / content:{contents}")

                #フィルタが定義されており、かつfile_titleがフィルタと一致しない場合はスキップする
                if filter!='' and contents.find(filter) != 0:
                    continue

                # MP3に埋め込むタグ情報をセットする
                tag_title="{0}年{1}月{2}日放送分「{3}」".format(year,str(month).zfill(2),str(day).zfill(2),unicodedata.normalize('NFKC', contents).replace(title_replace, '').replace('\u3000',' ')).replace('「「','「').replace('」」','」')
                tag_year=nendo
                tag_album=kouza+"["+str(nendo)+"年度]"
                #print(f"tag_title:{tag_title} / tag_year:{tag_year} / tag_album:{tag_album}")

                # MP3のダウンロードパスをセットする
                download_subdir=download_dir+path_delimiter+kouza+"["+str(nendo)+"年度]"
                os.makedirs(download_subdir, exist_ok=True)
                download_filename=kouza+" "+"{0}年{1}月{2}日放送分".format(year,str(month).zfill(2),str(day).zfill(2))+".mp3"
                download_path=download_subdir+path_delimiter+download_filename
                #print(f"download_path:{download_path}")

                # ストリーミングファイルのURLをセットする
                download_url=json_program['file_list'][0]['file_name']
                #print(f"download_url:{download_url}")

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
