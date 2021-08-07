import cv2
import numpy as np
import re
# from matplotlib import pyplot as plt
import os
from PIL import Image

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

waifus = []


def isColorfulStat(stat):
    for color in colors:
        if stat.startswith(color):
            return True

    return False


def imagesDifference(imageA, imageB):
    A = list(imageA.convert(r"RGB").getdata())
    B = list(imageB.convert(r"RGB").getdata())

    diff = []
    for i in range(0, len(A)):
        diff += [abs(A[i][0] - B[i][0]), abs(A[i][1] - B[i][1]), abs(A[i][2] - B[i][2])]
    return sum(diff) / len(diff)


def hasCurrentColorfulStat(waifu, stat):
  coords = (444, 0, 512, 512)
  image_obj = Image.open(waifu)
  current_stat = Image.open(stat)
  cropped_image = image_obj.crop(coords)

  for i in range(7):
      cropped_stat = cropped_image.crop((0, 66 * i, 68, 66 * (i + 1)))

      gray_stats = cropped_stat.convert("L")
      colors = gray_stats.getcolors()

      if gray_stats.getextrema() == (0, 0) or len(colors) < 50:
          break

      difference = imagesDifference(cropped_stat, current_stat)
      #print("DIFFERENCE", difference)

      if difference < 14:
          return True
  return False


def searchWaifus(stats):
  path, dirs, files = next(os.walk("./waifus"))
  file_count = len(files)

  for i in range(file_count):
      waifus.append("waifus/waifu" + str(i))

  for waifu in waifus:
      #print("-------------WAIFU ", waifu)
      matchingStats = []
      for stat in stats:
          #print("TESTING ", stat)

          if isColorfulStat(stat):
              if hasCurrentColorfulStat(waifu + ".webp", "stats/" + stat + ".webp"):
                matchingStats.append(stat)
          else:
              convertColor = cv2.COLOR_BGRA2GRAY
              method = cv2.TM_CCOEFF_NORMED
              threshold = 0.94

              img = cv2.imread(waifu + ".webp")  # main image
              img = cv2.cvtColor(img, convertColor)

              template = cv2.imread("stats/" + stat + ".webp")  # subimage
              template = cv2.cvtColor(template, convertColor)

              result = cv2.matchTemplate(img, template, method)

              #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
              loc = np.where(result >= threshold)

              if len(loc[0]) > 0:
                  #(startX, startY) = max_loc
                  #endX = startX + template.shape[1]
                  #endY = startY + template.shape[0]
                  matchingStats.append(stat)

                  #cv2.rectangle(img, (startX, startY), (endX, endY), (255, 0, 0), 3)

                  ## show the output image
                  #cv2.imshow("Output", img)
                  #cv2.waitKey(0)

      #print("-------------")
      if len(matchingStats) > 0:
          print(waifu, "matches the", len(matchingStats), " stats:", matchingStats)
          #input()

def main():
  stat_hunt = ""
  print("Please paste the message from Stat Hunt. Type 0 to finish. ")
  while True:
    current_line = input()
    stat_hunt += current_line + "\n"
    if current_line == "0":
      break
  
  print(stat_hunt)
  stats = re.findall('(?:- )([^\n]+)', stat_hunt)
  search_stats = list(filter(lambda stat: stat.find("✅") == -1, stats))
  clean_stats = list(map(lambda stat: stat[:-1], search_stats))
  
  searchWaifus(clean_stats)

main()