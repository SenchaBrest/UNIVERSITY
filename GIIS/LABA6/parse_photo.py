from PIL import Image


def save_pixel_data(image_path, output_file):
    img = Image.open(image_path)
    width, height = img.size

    with open(output_file, 'w') as f:
        for y in range(height):
            for x in range(width):
                pixel_color = img.getpixel((x, y))

                rgb_color = pixel_color[:3]
                f.write(f"({x}, {y}):{rgb_color}\n")

    print(f"Данные о пикселях сохранены в файл {output_file}")


if __name__ == "__main__":
    image_path = "icons8-чатgpt-240.png"
    output_file = "pixel_data.txt"
    save_pixel_data(image_path, output_file)
