import numpy as np
import cv2
import math
import mss
from typing import Tuple, List


def is_center_too_close_to(points_list: List[Tuple[int, int]], center: Tuple[int, int], threshold: int = 10) -> bool:
    """
    判断 center 是否和 points_list 中的任意一个点太近，用于过滤重复识别的点
    :param points_list: 已有的点列表
    :param center: 新的点
    :param threshold: 阈值
    :return: 是否太近
    """
    for p in points_list:
        if math.sqrt((p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2) < threshold:
            return True
    return False

def match_many_object_on_image(whole_img: np.ndarray,
                               obj_img: np.ndarray,
                               threshold=0.8,
                               draw_rect=False,
                               save_file=False,
                               output_name='output.png'):
    """
    在整张图片上找到所有的目标物体
    :param whole_img: 整张图片
    :param obj_img: 目标物体
    :param threshold: 阈值
    :param draw_rect: 是否画出矩形
    :param save_file: 是否保存到文件
    :param output_name: 输出文件名
    :return: 所有目标物体的中心坐标
    """
    res = cv2.matchTemplate(whole_img, obj_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # loc = (array([150, 200]), array([100, 300])) 表示两个匹配点的坐标分别是 (150, 100) 和 (200, 300)。
    match = []
    center_points = []
    final_points = []
    # go through all the points
    for pt in zip(*loc[::-1]):
        # pt 将会是 (100, 150) 和 (300, 200)  一个元组里分别代表横坐标(left2right)和纵坐标(up2down)
        center = (pt[0] + obj_img.shape[1] // 2, pt[1] + obj_img.shape[0] // 2)
        # if the center is too close to the existing points, skip
        if is_center_too_close_to(center_points, center):
            continue
        center_points.append(center)
        # add to the final points
        final_points.append(pt)
        match.append(pt)
        # draw rect?
        if draw_rect:
            cv2.rectangle(whole_img, pt, (pt[0] + obj_img.shape[1], pt[1] + obj_img.shape[0]), (0, 255, 0), 2)
    if save_file:
        # save to test/output.png
        if not os.path.exists('test'):
            os.mkdir('test')
        cv2.imwrite('test/' + (output_name or 'output.png'), whole_img)
    return final_points, center_points

def fast_screen_shot(left_up: Tuple[int, int], right_down: Tuple[int, int], save=True) -> np.ndarray:
    """
    快速截图
    :param left_up:  左上角坐标
    :param right_down:  右下角坐标
    :param save:  是否保存到文件
    :return:  截图
    """
    with mss.mss() as sct:
        # Define the monitor area to capture
        monitor = {'top': left_up[1], 'left': left_up[0], 'width': right_down[0] - left_up[0],
                   'height': right_down[1] - left_up[1]}
        # Capture the screen
        img = np.array(sct.grab(monitor))
        if save:
            # Save the captured image to a file
            cv2.imwrite('img/capture.png', img)
        # Convert the image from BGRA to BGR format
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

if __name__ == '__main__':
    res, center = match_many_object_on_image(img_full_screen, img_swm, draw_rect=True, output_name='111a.png')