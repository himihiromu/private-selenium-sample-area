from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importlib.util import spec_from_file_location, module_from_spec
import time
import threading
import subprocess
import shutil
import os


from dmm_myliblary_download import TEMP_DOWNLOAD_DIR


class FlagManagement:
    __pricate_object = None

    def __init__(self):
        self.file_move_flag = False
        self.is_restart = False

    @staticmethod
    def get_object():
        if FlagManagement.__pricate_object:
            return FlagManagement.__pricate_object
        else:
            FlagManagement.__pricate_object = FlagManagement()
            return FlagManagement.__pricate_object

    def get_file_move_flag(self):
        return self.file_move_flag

    def set_file_move_flag(self, b):
        self.file_move_flag = b

    def get_is_restart(self):
        return self.is_restart

    def set_is_restart(self, b):
        self.is_restart = b


cmd = r'C:\Users\himih\Documents\gityo\private-selenium-sample-area\.venv\Scripts\python.exe C:\Users\himih\Documents\gityo\private-selenium-sample-area\dmm_myliblary_download.py'


def pyfile_run(filepath):
    module_name = '__main__'
    spec = spec_from_file_location(module_name, filepath)
    foo = module_from_spec(spec)
    spec.loader.exec_module(foo)


# ファイル／フォルダの変化があった時に呼ばれるイベントハンドラ
class EventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.flag_management = FlagManagement.get_object()

    def on_any_event(self, e):
        print('更新有り')
        self.flag_management.set_file_move_flag(True)


def process_kill(p):
    p.kill()
    shutil.rmtree(TEMP_DOWNLOAD_DIR)
    print('fileに動きがないのでプロセスをキルします。')
    flag_management = FlagManagement.get_object()
    flag_management.set_is_restart(True)


def main():
    if not os.path.exists(TEMP_DOWNLOAD_DIR):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(TEMP_DOWNLOAD_DIR)
    flag_management = FlagManagement.get_object()
    # ファイル／フォルダの監視を開始
    observer = Observer()
    observer.schedule(EventHandler(), path=TEMP_DOWNLOAD_DIR, recursive=True)
    observer.start()

    while True:

        flag_management.set_file_move_flag(False)

        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
        t = threading.Timer(60*60*4, process_kill, args=(p, ))
        t.start()

        # 監視のためのループ処理
        while True:
            if flag_management.get_file_move_flag():
                t.cancel()
                t = threading.Timer(60*60*4, process_kill, args=(p, ))
                t.start()
                flag_management.set_file_move_flag(False)
                print('fileに動きがあったよう。')

            if flag_management.get_is_restart():
                flag_management.set_is_restart(False)
                break
            time.sleep(3)
            print('file確認中')


if __name__ == '__main__':
    main()
