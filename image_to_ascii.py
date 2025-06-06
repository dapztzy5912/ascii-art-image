import requests
from PIL import Image
from io import BytesIO
import shutil
import os

ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 to adjust font height ratio
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel // 25] for pixel in pixels)
    return ascii_str

def image_to_ascii(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        img = resize_image(img)
        img = grayify(img)

        ascii_str = pixels_to_ascii(img)
        img_width = img.width
        ascii_img = "\n".join(
            ascii_str[i:i + img_width] for i in range(0, len(ascii_str), img_width)
        )
        return ascii_img
    except Exception as e:
        return f"[!] Error: {e}"

def main():
    os.system("clear")
    print("=== Gambar ke ASCII ===\n")
    url = input("Masukkan URL gambar (JPG/PNG): ").strip()
    ascii_art = image_to_ascii(url)
    print("\n\n" + ascii_art)

if __name__ == "__main__":
    main()
