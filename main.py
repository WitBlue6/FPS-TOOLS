import shubiao
import asyncio
import cv2
import threading
from time import sleep
from shubiao import cv as cv
from pynput import keyboard, mouse

ctrl_pressed = False
FIRE = False
SINGLE = True


img_enemies = []
img_enemies.append(cv2.imread('./swm.png'))
def aim_to_enemy(left_up=(0, 0), right_down=(1919, 1079), threshold=0.8, single=True, fire=False):
    """
    自瞄以及是否连杀
    :param left_up: 屏幕截图左上
    :param right_down: 右下
    :param threshold: 检测是否存在敌人的阈值
    :param single: 是否开启连杀
    :param fire: 是否开火 只有连杀且开火才是允许的 否则只自瞄
    :return:
    """
    img = cv.fast_screen_shot(left_up, right_down)
    for img_enemy in img_enemies:  # 遍历所有敌人图片
        res, centers = cv.match_many_object_on_image(img, img_enemy, threshold=threshold)
        if len(res) == 0:  # 未找到该类型敌人
            continue
        centers = [(x + left_up[0], y + left_up[1]) for x, y in centers]
        if not single and fire:  # 向所有目标开火
            for center in centers:
                shubiao.click(center)
                sleep(0.3)
            return
        else:  # 只对单个目标进行瞄准
            shubiao.move_to(centers[0])
            return

async def handle_key_press(key):
    if key in {keyboard.Key.esc}:
        # Stop listener
        return False
    global ctrl_pressed, FIRE, SINGLE
    try:
        # 如果按下了 Ctrl 键
        if key == keyboard.Key.ctrl_l:
            if not ctrl_pressed:  # 避免重复执行
                ctrl_pressed = True
                print("***开始瞄准***")
                if ctrl_pressed and SINGLE:# 启动瞄准线程
                    for i in range(3):
                        aim_to_enemy(single=SINGLE, fire=FIRE)
                else:
                    aim_to_enemy(single=SINGLE, fire=FIRE)
        elif key == keyboard.KeyCode.from_char('n'):  # N键开启和关闭单一敌人模式
            if SINGLE:
                SINGLE = False
                FIRE = True
                print('开启多人连杀模式')
            else:
                SINGLE = True
                FIRE = False
                print('关闭多人连杀模式')
    except Exception as e:
        print(f"错误: {e}")

async def handle_key_release(key):
    global ctrl_pressed, FIRE, SINGLE
    # 如果松开了 Ctrl 键
    if key == keyboard.Key.ctrl_l:
        ctrl_pressed = False
        print("***停止瞄准***")

def on_press(key):
    asyncio.run(handle_key_press(key))

def on_release(key):
    asyncio.run(handle_key_release(key))

def aim_on():
    # 创建键盘监听器
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    aim_on()

if __name__ == '__main__':
    main()