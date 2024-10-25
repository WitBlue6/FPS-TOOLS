from time import sleep
from typing import Union, Tuple
from pynput.mouse import Controller
from pyperclip import copy
import numpy as np

import win32api
import win32con
import asyncio

FAILSAFE = False
mouse = Controller()
WIDTH = 1920
HEIGHT = 1080

def move_to(pos: Tuple[int, int]) -> None:
    win32api.SetCursorPos(pos)

def click_only(sleep_time=0.03) -> None:
    """
    在鼠标当前位置点击
    :param sleep_time: 鼠标松开间隔时间
    :return:
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(sleep_time)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def click(pos: Tuple[int, int], cnt=1, sleep_time=0.03, cnt_sleep=0.04) -> None:
    """
    将鼠标移动至pos,然后点击鼠标
    :param pos:
    :param cnt: 连点次数
    :param sleep_time: 鼠标点击间隔时间
    :param cnt_sleep: 连点间隔时间
    :return:
    """
    for i in range(cnt):
        move_to(pos)
        click_only(sleep_time)
        if FAILSAFE:
            print('**FAILSAFE**')
            break
        if cnt > 1 and i != cnt - 1:  # 连点模式
            sleep(cnt_sleep)

def swipe(pos1: Tuple[int, int], pos2: Tuple[int, int], sleep_time=0.03) -> None:
    """
    按住拖动鼠标从pos1至pos2
    :param pos1:
    :param pos2:
    :param sleep_time:
    :return:
    """
    move_to(pos1)
    sleep(sleep_time)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    move_to(pos2)
    sleep(sleep_time)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 ,0 ,0 ,0)

def move_mouse(pos: Tuple[int, int]) -> None:
    """
    利用相对位移特性实现鼠标移动，适用于鼠标锁定的FPS游戏
    :param pos:  目标点位置
    :return:
    """
    x, y = pos[0] - WIDTH // 2, pos[1] - HEIGHT // 2
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)

def click_fps(pos: Tuple[int, int], cnt=1, sleep_time=0.03, cnt_sleep=0.04) -> None:
    """
    用相对移动将鼠标移动至pos,然后点击鼠标
    :param pos:
    :param cnt: 连点次数
    :param sleep_time: 鼠标点击间隔时间
    :param cnt_sleep: 连点间隔时间
    :return:
    """
    for i in range(cnt):
        move_mouse(pos)
        click_only(sleep_time)
        if FAILSAFE:
            print('**FAILSAFE**')
            break
        if cnt > 1 and i != cnt - 1:  # 连点模式
            sleep(cnt_sleep)

def print_mouse() -> None:
    print('Mouse position: {0}'.format(
        mouse.position))
    copy(str(mouse.position))

if __name__ == '__main__':
    move_mouse((10, 10))
