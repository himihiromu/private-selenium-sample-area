import subprocess
import os
import glob
import shutil


def main():
    print(len('水泳部JDまいなちゃん 20歳☆腹筋ビクンビクン♪細ガリマッチョなスポーツ少女はナマ姦大好き3年生◆性欲凝縮されたアスリートBODY大暴走で生ちんぽ馬乗りパイパンまんこ打ち付けイキまくる☆.dcv'.encode()))
    files = glob.glob("./sample1/*")
    for file in files:
        print(file)
        print(os.path.getsize(file))
        new_path = shutil.move(file, "./sample2")
        with open(file, mode='w') as f:
            f.write("")


if __name__=='__main__':
    main()
