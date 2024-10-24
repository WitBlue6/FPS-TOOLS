# FPS-TOOLS
# FPS辅助工具 
# （注：仅限单机游戏使用，请勿用于其他用途） 
## 说明  
本项目参考了https://gitee.com/taylorandtony/swm-auto-tool  
开发的沙威玛辅助工具，具有两项功能，需要自行提供目标图片，未使用YOLO等神经网络实现动态监测  

### 1.单目标瞄准  
按住Ctrl键鼠标准心持续锁向识别到的目标，目标参考图片由自己提供。  
### 2.多目标连杀  
按下N切换模式，此时按住Ctrl会自动瞄准所有识别到的目标并按下鼠标左键，实现多目标连杀，具体参数可自行调整。  

## 使用方法  
### 1.目标图片提供  
在main.py中的img_enemies列表中append你想要识别的目标即可，若有视角差异可以提供多角度  
    img_enemies = []  
    img_enemies.append(cv2.imread('./swm.png'))  
### 2.功能完善  
可自行在keyboard监听中添加其他功能 

## 更新日志  
2024-10-24 开源


 
