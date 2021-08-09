import cv2
import numpy as np
import re
# from matplotlib import pyplot as plt
import os
from PIL import Image
import copy
from io import BytesIO
import base64

colors = [
    "Black",
    "Blonde",
    "Blue",
    "Brown",
    "Green",
    "Pink",
    "Purple",
    "Red",
    "Violet",
    "Yellow",
    "White",
]

def isColorfulStat(stat):
    for color in colors:
        if stat["name"].startswith(color):
            return True

    return False

def calculateImagesDifference(imageA, imageB):
    A = list(imageA.convert(r"RGB").getdata())
    B = list(imageB.convert(r"RGB").getdata())

    diff = []
    for i in range(0, len(A)):
        diff += [abs(A[i][0] - B[i][0]), abs(A[i][1] - B[i][1]), abs(A[i][2] - B[i][2])]
    return sum(diff) / len(diff)

def hasCurrentColorfulStat(waifu, stat):
  coords = (444, 0, 512, 512)
  image_obj = Image.open(BytesIO(base64.b64decode(waifu["data"])))
  current_stat = Image.open(BytesIO(base64.b64decode(stat["data"])))
  cropped_image = image_obj.crop(coords)

  for i in range(7):
      cropped_stat = cropped_image.crop((0, 66 * i, 68, 66 * (i + 1)))

      gray_stats = cropped_stat.convert("L")
      colors = gray_stats.getcolors()

      if gray_stats.getextrema() == (0, 0) or len(colors) < 50:
          break

      difference = calculateImagesDifference(cropped_stat, current_stat)
      #print("DIFFERENCE", difference)

      if difference < 14:
          return True
  return False

def searchWaifus(waifus, stats):
  waifus_stats = []
  for waifu in waifus:
      #print("-------------WAIFU ", waifu)
      matchingStats = []
      for stat in stats:
          #print("TESTING ", stat)

          if isColorfulStat(stat):
              if hasCurrentColorfulStat(waifu, stat):
                matchingStats.append(stat["name"])
          else:
              convertColor = cv2.COLOR_BGRA2GRAY
              method = cv2.TM_CCOEFF_NORMED
              threshold = 0.94

              waifu_original = base64.b64decode(waifu["data"])
              waifu_np = np.frombuffer(waifu_original, dtype=np.uint8)
              img = cv2.imdecode(waifu_np, flags=1)  # main image
              img = cv2.cvtColor(img, convertColor)

              stat_original = base64.b64decode(stat["data"])
              stat_np = np.frombuffer(stat_original, dtype=np.uint8)
              template = cv2.imdecode(stat_np, flags=1)  # subimage
              template = cv2.cvtColor(template, convertColor)

              result = cv2.matchTemplate(img, template, method)

              #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
              loc = np.where(result >= threshold)

              if len(loc[0]) > 0:
                  #(startX, startY) = max_loc
                  #endX = startX + template.shape[1]
                  #endY = startY + template.shape[0]
                  matchingStats.append(stat["name"])

                  #cv2.rectangle(img, (startX, startY), (endX, endY), (255, 0, 0), 3)

                  ## show the output image
                  #cv2.imshow("Output", img)
                  #cv2.waitKey(0)
      obj = {}
      obj["name"] = waifu["name"]
      obj["data"] = waifu["data"].decode("utf-8")
      obj["stats"] = matchingStats
      waifus_stats.append(obj)
  return waifus_stats
