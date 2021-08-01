import cv2
import numpy as np

stats = ["blue-eyes" , "blue-hair", "braid" , "hat", "red-eyes"]
waifus = ["waifu1", "waifu2", "waifu3", "waifu4", "waifu5", "waifu6"]

for waifu in waifus:
  matchingStats = []
  for stat in stats:
    img = cv2.imread(waifu + ".png") #main image
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    template = cv2.imread(stat + ".png") #subimage
    template = cv2.cvtColor(template,cv2.COLOR_BGR2HSV)  

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.9)

    if len(loc[0]) > 0:
      matchingStats.append(stat)
  print (waifu, "matches the following stats:", matchingStats) 