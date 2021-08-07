from PIL import Image
import glob

def crop(image_path, coords, offset):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)

    for i in range(7):
        filepath = './stats/stat' + str(i + offset) + '.webp'
        cropped_stat = cropped_image.crop((0, 66 * i, 68, 66 * (i + 1)))

        gray_stats = cropped_stat.convert('L')
        colors = gray_stats.getcolors()

        if gray_stats.getextrema() == (0, 0) or len(colors) < 50:
            break
        cropped_stat.save(filepath)
    return i


def main():
    offset = 0
    for filename in glob.glob('waifus/*.webp'): 
        offset += crop(filename, (444, 0, 512, 512), offset)

main()