import requests
from PIL import Image
from removebg import RemoveBg
import base64
import os

# 第一阶段，利用api去除背景色
img_file = r'C:\Users\wmj\Desktop\微信图片_20220810175653.jpg'  #
img_dir = r''
png_name = "no-bg.png"
import base64

BACKGROUND_COLOR = {
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
}


def remove_bg_online():
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(img_file, 'rb')},
        data={'size': '4k'},
        headers={'X-Api-Key': 'AZw5yNyvCXU131JE5UGimDTh'},
    )
    if response.status_code == requests.codes.ok:
        with open(png_name, 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)


def remove_bg_online_new():
    rmbg = RemoveBg("AZw5yNyvCXU131JE5UGimDTh", "error.log")
    with open(img_file, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    rmbg.remove_background_from_base64_img(encoded_string, size='auto')


def generate_and_save_color_bg_image(im,color):
    p = Image.new('RGBA', im.size, BACKGROUND_COLOR[color])
    p.paste(im, (0, 0, x, y), im)
    p.save(os.path.join(img_dir, f'bg_{color}.png'))


if __name__ == "__main__":
    remove_bg_online_new()
    color = "all"
    im = Image.open(png_name)
    x, y = im.size
    try:
        # (alpha band as paste mask).
        if color == "all":
            for color in BACKGROUND_COLOR.keys():
                generate_and_save_color_bg_image(im,color)
        elif color in BACKGROUND_COLOR.keys():
            generate_and_save_color_bg_image(im, color)
        else:
            print("not match")
    except:
        pass



