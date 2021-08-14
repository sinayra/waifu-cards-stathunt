import cv2
import numpy as np
# from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO
import base64
from concurrent.futures import as_completed, ThreadPoolExecutor

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
    "Orange",
    "Grey"
]

clothes = [
    "Japanese-style Clothes (Rare)",
    "Japanese-style Clothes",
    "Maid (Rare)",
    "School Uniform",
    "Swimsuit",
]

socks = [
    "Japanese-style Clothes (Rare)",
    "Japanese-style Clothes",
    "Maid (Rare)",
    "School Uniform",
]
shoes = [
    "Barefoot (Rare)",
    "Boots (Rare)",
    "High Heels (Rare)",
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

def hasMax2Pieces(machingStats, piece):
    stats = filter(lambda stat: piece in stat, machingStats)

    return stats == 2

def hasMax1Piece(machingStats, piece):
    return set(machingStats) & set(piece)

def cropStats(waifu_data):
    coords = (444, 0, 512, 512)
    image_obj = Image.open(BytesIO(base64.b64decode(waifu_data)))

    return image_obj.crop(coords)

def addStatsImages(stats):
    for stat in stats:
        stat["image"] = Image.open(BytesIO(base64.b64decode(stat["data"])))

def matchStats(waifu_data, stats):
    addStatsImages(stats)
    cropped_waifu = cropStats(waifu_data)
    matchingStats = []
    totalStats = 0
    for stat in stats:
        if totalStats == 7:
            break
        
        if "Eyes" in stat and hasMax2Pieces(matchingStats, "Eyes"):
            break
        
        if "Girl" in stat and hasMax2Pieces(matchingStats, "Girl"):
            break

        if stat in clothes and hasMax1Piece(matchingStats, clothes):
            break

        if stat in shoes and hasMax1Piece(matchingStats, shoes):
            break

        if stat in socks and hasMax1Piece(matchingStats, socks):
            break

        if hasCurrentStat(cropped_waifu, stat["image"]):
            matchingStats.append(stat["name"])
            totalStats = totalStats + 1

    return matchingStats
