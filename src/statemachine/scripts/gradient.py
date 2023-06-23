import numpy as np
from matplotlib import pyplot as plt
import cv2

def gaussuian_filter(kernel_size, sigma=0.2, muu=0):

    x, y = np.meshgrid(np.linspace(-1, 1, kernel_size),
                       np.linspace(-1, 1, kernel_size))
    dst = np.sqrt(x**2+y**2)
    normal = 1/(2.0 * np.pi * sigma**2)
    gauss = np.exp(-((dst-muu)**2 / (2.0 * sigma**2))) * normal

    return gauss


Cx = 190
Cy = 220

gauss = gaussuian_filter(201)
img1 = cv2.imread("/home/deveshdatwani/capstone/src/statemachine/robot_map/ground_truth_map.jpeg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.imread("/home/deveshdatwani/capstone/src/statemachine/robot_map/current_map.jpeg")
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
 
cost = 0

def cal(img, gauss):
    cost = 0
    for i in range(90, 201):
        for j in range(120, 201):
            if img[i][j] < 50:
                cost += img[i][j] * gauss[i-90][j-90]
    return cost

cost1 = cal(img1, gauss)
cost2 = cal(img2, gauss)
print(cost2/cost1)

