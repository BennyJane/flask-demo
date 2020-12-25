import os
import sys

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def isWin():
    windows = False
    plat = sys.platform
    if plat.startswith('win'):
        windows = True
    return windows


win = isWin()


def modifyPath(relativePath: str) -> str:
    """
    :param relativePath:  目标文件的相对路径,默认输入linux下路径: logs/api; 开头不能有斜杠
    :return:
    """
    if win:
        path = '\\'.join(relativePath.split('\/'))
    else:
        path = '/'.join(relativePath.split('\\'))
    return path


def get_key_form_env(key):
    target_key = os.getenv(key, None)
    return target_key
