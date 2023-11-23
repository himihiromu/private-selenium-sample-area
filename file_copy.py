import os
import shutil
import glob

from dmm_myliblary_download import DOWNLOAD_COMPLETE_DIR


MOVE_FILE_PATH = r'\\RASPBERRY\rasp_public1\動画\fanza'


def main():
    files = glob.glob(f"{DOWNLOAD_COMPLETE_DIR}/*")
    for file in files:
        print(file)
        if os.path.getsize(file):

            if(file in [r'E:\hiromu\動画\fanza\「シャワーだけ貸してあげるよ」終電なくなり同僚女子社員の部屋に… 無防備すぎるおっぱいと生脚に興奮した僕はチラつく妻の存在が吹き飛ぶほど一晩中モウレツにハメ狂った… 伊藤舞雪.dcv', r'E:\hiromu\動画\fanza\水泳部JDまいなちゃん 20歳☆腹筋ビクンビクン♪細ガリマッチョなスポーツ少女はナマ姦大好き3年生◆性欲凝縮されたアスリートBODY大暴走で生ちんぽ馬乗りパイパンまんこ打ち付けイキまくる☆.dcv', r'E:\hiromu\動画\fanza\湘南の海で出会った水着ギャルがデカチン童貞君と「素股オイルマッサージ」に挑戦！ 生マンにヌルヌルこすれるデカマラに発情しちゃって『おま○こに入れてみるw』そのまま筆おろし生ハメ中出しSEX！！.dcv']):
                continue
            shutil.move(file, MOVE_FILE_PATH)
            with open(file, mode='w') as f:
                f.write("")


if __name__ == "__main__":
    main()
