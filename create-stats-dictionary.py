from os import listdir
from os.path import isfile, join
import base64
import json

stats_folder = './stats/'
stats_filenames = [f for f in listdir(stats_folder) if isfile(join(stats_folder, f))]
stats = []
for stat_filename in stats_filenames:
    obj = {}
    with open(stats_folder + stat_filename, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    obj["name"] = stat_filename[:-5]
    obj["data"] = data.decode("utf-8")

    stats.append(obj)

file = open("stats.json", "w")

stats_obj = {}
stats_obj["stats"] = stats
file.write(json.dumps(stats_obj))
file.close()