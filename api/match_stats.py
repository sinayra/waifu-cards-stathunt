import cv2
import numpy as np
# from matplotlib import pyplot as plt
from PIL import Image
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

def hasCurrentStat(waifu, stat):
  for i in range(7):
      cropped_stat = waifu.crop((0, 66 * i, 68, 66 * (i + 1)))

      gray_stats = cropped_stat.convert("L")
      colors = gray_stats.getcolors()

      if gray_stats.getextrema() == (0, 0) or len(colors) < 50:
          break

      difference = calculateImagesDifference(cropped_stat, stat)
      #print("DIFFERENCE", difference)

      if difference < 14:
          return True
  return False

def cropStats(waifu):
    coords = (444, 0, 512, 512)
    image_obj = Image.open(BytesIO(base64.b64decode(waifu["data"])))

    return image_obj.crop(coords)

def addStatsImages(stats):
    for stat in stats:
        stat["image"] = Image.open(BytesIO(base64.b64decode(stat["data"])))

def searchWaifus(waifus, stats):
  waifus_stats = []
  addStatsImages(stats)

  for waifu in waifus:
      #print("-------------WAIFU ", waifu["name"])
      cropped_waifu = cropStats(waifu)
      matchingStats = []
      totalStats = 0
      for stat in stats:
        if hasCurrentStat(cropped_waifu, stat["image"]):
            matchingStats.append(stat["name"])
            totalStats = totalStats + 1
        if totalStats == 7:
            break
        
      obj = {}
      obj["name"] = waifu["name"]
      obj["data"] = waifu["data"].decode("utf-8")
      obj["stats"] = matchingStats
      waifus_stats.append(obj)
  return waifus_stats
