import cv2
import numpy as np
#from matplotlib import pyplot as plt
import os


stats = ["Pointy Ears (Rare)", "Black Hair", "Purple Hair", "School Uniform", "Stockings", "Cute Little Fang (Rare)", "Glasses (Rare)"]
colors = ["Black", "Blonde", "Blue", "Brown", "Green", "Pink", "Purple", "Red", "Violet", "Yellow"]

waifus = []

def isColorfulStat(stat):
  for color in colors:
    if stat.startswith(color):
      return True
    
  return False

path, dirs, files = next(os.walk("./waifus"))
file_count = len(files)
for i in range(file_count):
  waifus.append("waifus/waifu" + str(i))

for waifu in waifus:
  matchingStats = []
  for stat in stats:

    if isColorfulStat(stat): 
      convertColor = cv2.COLOR_BGR2HSV
      threshold = 0.9
    else:
      convertColor = cv2.COLOR_BGR2GRAY
      threshold = 0.95

    img = cv2.imread(waifu + ".webp") #main image
    img = cv2.cvtColor(img, convertColor)

    template = cv2.imread("stats/" + stat + ".webp") #subimage
    template = cv2.cvtColor(template, convertColor)  

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
      #(startX, startY) = max_loc
      #endX = startX + template.shape[1]
      #endY = startY + template.shape[0]
      matchingStats.append(stat)

      #cv2.rectangle(img, (startX, startY), (endX, endY), (255, 0, 0), 3)

      # show the output image
      #cv2.imshow("Output", img)
      #cv2.waitKey(0)

  if (len(matchingStats) > 0):
    print (waifu, "matches the", len(matchingStats), " stats:", matchingStats) 