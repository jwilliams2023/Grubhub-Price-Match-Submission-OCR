import os
from PIL import Image
from PIL import ImageOps
from pytesseract import pytesseract


def get_total_price(last_download_name, download_dir, path_to_tesseract):
    pytesseract.tesseract_cmd = path_to_tesseract
    tesseract_config = r'--oem 1 --psm 4'

    if last_download_name.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(download_dir, last_download_name)
        image_file = Image.open(image_path).convert('1', dither=Image.NONE)

        # inverted_image = ImageOps.invert(image_file)
        # image_file.show()
        # inverted_image.show()

        # pos_image_text_list = pytesseract.image_to_string(image_file, config=tesseract_config).split()
        # neg_image_text_list = pytesseract.image_to_string(image_file, config=tesseract_config).split()
        # image_text_list = list(set(pos_image_text_list + neg_image_text_list))

        image_text_list = pytesseract.image_to_string(image_file, config=tesseract_config).split()
        image_text_list_lower = [token.lower() for token in image_text_list]
        image_text_set = set(image_text_list_lower)
        # print(image_text_list)

        # If Tesseract can find the total in the image
        if "total" in image_text_set:
            print("Total Found")
            image_prices = []
            for elem in image_text_list:
                if elem == "$":
                    continue
                elif "$" in set(elem):
                    image_prices.append(float(elem.strip("$")))
                elif len(elem) == 4 and elem[1] == ".":
                    if elem.replace('.', '', 1).isdigit():
                        image_prices.append(float(elem))

            max_price = 30.0
            filtered_image_prices = [k for k in image_prices if k <= max_price]
            if len(filtered_image_prices) > 0:
                total = sorted(filtered_image_prices)[-1]
            else:
                raise Exception("No prices found")

            print("Prices Found: ", image_prices)
            print("Total: ", format(total, '.2f'))

        elif "checkout" in image_text_set:
            total = float(image_text_list[image_text_list_lower.index("checkout") + 1].strip("$"))

        # Code to check for subtotal and tax

        # elif "subtotal" in image_text_set:
        #     subtotal = float(image_text_list[image_text_list_lower.index("subtotal") + 1].strip("$"))
        # else:
        #     raise Exception("No subtotal found in Image")
        #
        # elif "tax" in image_text_set:
        #     tax = float(image_text_list[image_text_list_lower.index("tax") + 1].strip("$"))
        # else:
        #     raise Exception("No tax found in Image")
        #
        # total = subtotal + tax
        #
        else:
            total = 0.0
            print("ERROR: No Total Price Found in Image")

    else:
        raise Exception("No Image Found in Directory")

    return format(total, '.2f')