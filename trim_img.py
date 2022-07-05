"""trim_image.py"""
import cv2

size = 16

# 画像読み込み
img = cv2.imread("images/48-488312_blockcss-minecraft-terrain-png-1-0-0.png" -1)

# img[top : bottom, left : right]
for i in range(36):
    for j in range(24):
        print(i, j)
        trim_img = img[i * size: (i + 1) * size, j * size: (j + 1) * size]
        cv2.imwrite(f"textures/{i}-{j}.png", trim_img)
