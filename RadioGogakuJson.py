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
        download_dir=".\\download"
        ffmpeg_bin=".\\win\\ffmpeg.exe"
    elif sys.platform=='darwin': #Mac
        path_delimiter="/"
        today=datetime.date.today()
        download_dir=expanduser("~")+"/Downloads/NHK語学講座"
        ffmpeg_bin="./mac/ffmpeg"
    else: #Linux(Synology-NAS)
        path_delimiter="/"
        download_dir="/volume1/music/NHK語学講座"
        ffmpeg_bin="/volume1/@appstore/ffmpeg/bin/ffmpeg"

    #各語学講座のjsonのURL、講座名、ダウンロード完了済みかどうかをチェックするファイルサイズ、MP3タイトルタグから消去するプレフィックス文字列を定義する
    url_kouza_size_prefix_filters  = []
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=6805&corner_site_id=01', '小学生の基礎英語',           4800000, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=6806&corner_site_id=01', '中学生の基礎英語レベル1',     7200000, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=6807&corner_site_id=01', '中学生の基礎英語レベル2',     7200000, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=6808&corner_site_id=01', '中高生の基礎英語inEnglish',  7200000, '中高生の基礎英語 in English ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=6809&corner_site_id=01', 'ラジオビジネス英語',         7200000, 'ラジオビジネス英語 ', '' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0916&corner_site_id=01', 'ラジオ英会話',              7200000, 'ラジオ英会話 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=2331&corner_site_id=01', '英会話タイムトライアル',      4800000, '英会話タイムトライアル', '' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=77RQWQX1L6&corner_site_id=01', 'ニュースで学ぶ「現代英語」',   7200000, 'ニュースで学ぶ「現代英語」 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=4121&corner_site_id=01', 'ボキャブライダー',           2400000, '', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0915&corner_site_id=01', 'まいにち中国語',             7200000, 'まいにち中国語 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=6581&corner_site_id=01', 'ステップアップ中国語',        7200000, 'ステップアップ中国語', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0951&corner_site_id=01', 'まいにちハングル講座',        7200000, 'まいにちハングル講座 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=6810&corner_site_id=01', 'ステップアップハングル講座',   7200000, 'ステップアップ ハングル講座 ', '' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0946&corner_site_id=01', 'まいにちイタリア語【初級編】', 7200000, 'まいにちイタリア語 初級編 ', 'まいにちイタリア語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0946&corner_site_id=01', 'まいにちイタリア語【応用編】',  7200000, 'まいにちイタリア語 応用編 ', 'まいにちイタリア語　応用編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0943&corner_site_id=01', 'まいにちドイツ語【初級編】',    7200000, 'まいにちドイツ語 初級編 ', 'まいにちドイツ語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0943&corner_site_id=01', 'まいにちドイツ語【応用編】',   7200000, 'まいにちドイツ語 応用編 ', 'まいにちドイツ語　応用編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0953&corner_site_id=01', 'まいにちフランス語【初級編】',  7200000, 'まいにちフランス語 初級編 ', 'まいにちフランス語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0953&corner_site_id=01', 'まいにちフランス語【応用編】', 7200000, 'まいにちフランス語 応用編 ', 'まいにちフランス語　応用編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0948&corner_site_id=01', 'まいにちスペイン語【初級編】',  7200000, 'まいにちスペイン語 初級編 ', 'まいにちスペイン語　初級編　' ]]
    url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0948&corner_site_id=01', 'まいにちスペイン語【応用編】', 7200000, 'まいにちスペイン語 応用編 ', 'まいにちスペイン語　応用編　' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0956&corner_site_id=01', 'まいにちロシア語【初級編】',    7200000, 'まいにちロシア語 初級編 ', 'まいにちロシア語　初級編　' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0956&corner_site_id=01', 'まいにちロシア語【応用編】',   7200000, 'まいにちロシア語 応用編 ', 'まいにちロシア語　応用編　' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=0937&corner_site_id=01', 'アラビア語講座',              7200000, 'アラビア語講座 ', '' ]]
    # url_kouza_size_prefix_filters += [['https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series?site_id=2769&corner_site_id=01', 'ポルトガル語講座【入門編】',     7200000, 'ポルトガル語講座 入門 ', '' ]]

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

        # ダウンロードしたファイルパスを保持する変数を初期化する
        last_download_path_only_date=""

        # 各LessonのストリーミングデータをMP3に変換してダウンロードする
        for json_element in json_dict['episodes']:

            #放送年月日を取得する
            datetime_string=json_element['aa_contents_id'].split(";")[3]
            month=int(datetime_string[4:6])
            day=int(datetime_string[6:8])
            year=int(datetime_string[0:4])
            if month<4:
                nendo=year-1
            else:
                nendo=year
            contents=json_element['aa_contents_id'].split(";")[1]
            # print(f"year:{year} / month:{month} / day:{day} / content:{contents}")

            #フィルタが定義されており、かつfile_titleがフィルタと一致しない場合はスキップする
            if filter!='' and contents.find(filter) != 0:
                continue

            # MP3に埋め込むタグ情報をセットする
            content=unicodedata.normalize('NFKC', contents).replace(title_replace, '').replace('\u3000',' ')
            tag_title="{0}年{1}月{2}日放送分「{3}」".format(year,str(month).zfill(2),str(day).zfill(2),content).replace('「「','「').replace('」」','」')
            tag_year=nendo
            tag_album=kouza+"["+str(nendo)+"年度]"
            #print(f"tag_title:{tag_title} / tag_year:{tag_year} / tag_album:{tag_album}")

            # MP3のダウンロードパスをセットする
            download_subdir=download_dir+path_delimiter+kouza+"["+str(nendo)+"年度]"
            os.makedirs(download_subdir, exist_ok=True)
            download_filename=kouza+" "+"{0}年{1}月{2}日放送分".format(year,str(month).zfill(2),str(day).zfill(2))+".mp3"
            download_path=download_subdir+path_delimiter+download_filename

            # 同日に放送された番組は特別番組と判断してダウンロードファイルのファイル名にコンテンツ名を付与する
            if download_path == last_download_path_only_date :
                download_filename=kouza+" "+"{0}年{1}月{2}日放送分".format(year,str(month).zfill(2),str(day).zfill(2))+"_"+content+".mp3"
                download_path=download_subdir+path_delimiter+download_filename
            else:
                last_download_path_only_date = download_path
            #print(f"download_path:{download_path}")

            # ストリーミングファイルのURLをセットする
            download_url=json_element['stream_url']
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
    
