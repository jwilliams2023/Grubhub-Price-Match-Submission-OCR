import os
from PIL import Image, ImageOps, ImageEnhance
from pytesseract import pytesseract


def get_total_price(last_download_name, download_dir, path_to_tesseract):
    pytesseract.tesseract_cmd = path_to_tesseract
    tesseract_config = r'--oem 1 --psm 4'
    total_val = 0.0
    total_labels = ['total', 'checkout', 'pay now']
    if last_download_name.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(download_dir, last_download_name)

        # Open the image
        image_file = Image.open(image_path)

        #print raw tessereact text
        print("Tesseract text:")
        print(pytesseract.image_to_string(image_file, config=tesseract_config))

        # Resize image to 50% bigger
        width, height = image_file.size
        new_width = int(width // 3)
        new_height = int(height // 3)
        resized_image = image_file.resize((new_width, new_height))

        # contrast improved image
        contrast_filter = ImageEnhance.Contrast(resized_image)
        contrast_image_file = contrast_filter.enhance(2)

        # convert the contrasted image to black and white values
        bw_image_file = contrast_image_file.convert('1', dither=Image.NONE)

        # create a negative of the image
        inverted_image = ImageOps.invert(bw_image_file)

        # Update image_file to the final processed image
        image_file = inverted_image

        # Use Tesseract to do OCR on the image
        image_text = pytesseract.image_to_string(image_file, config=tesseract_config).split()
        cont_image_text = pytesseract.image_to_string(contrast_image_file, config=tesseract_config).split()
        bw_image_text = pytesseract.image_to_string(bw_image_file, config=tesseract_config).split()
        neg_image_text = pytesseract.image_to_string(inverted_image, config=tesseract_config).split()


        # Concatenate the text from all images
        text = ' '.join(image_text) + ' ' + ' '.join(cont_image_text) + ' ' + ' '.join(bw_image_text) + ' ' + ' '.join(neg_image_text)

        print("Tesseract joined text: ")
        print(text)
        print()

        # Convert the text to lowercase and remove colons and hyphens
        text = text.lower().replace(':', '').replace('-', '')

        print("Processed text:")
        print(text)

        # Process the text, assuming the total is listed as 'Total: $xx.xx'
        lines = text.split('\n')
        for line in lines:
            words = line.split()
            for label in total_labels:
                if label in words:
                    total_index = words.index(label)
                    if total_index + 1 < len(words):
                        total_value_str = words[total_index + 1]
                        if total_value_str.startswith('$'):
                            total_value_str = total_value_str.replace('$', '')  # remove dollar sign
                            total_val = float(total_value_str)  # convert to float
                            if total_val > 1000:
                                total_val /= 1000
                            elif total_val > 100:
                                total_val /= 100
                    break
        total_val = format(total_val, '.2f')
        print()
        print(f"Total is  {total_val}")
    return total_val


# def get_total_price(last_download_name, download_dir, path_to_tesseract):
#     pytesseract.tesseract_cmd = path_to_tesseract
#     tesseract_config = r'--oem 1 --psm 4'
#
#     if last_download_name.endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(download_dir, last_download_name)
#
#         # original image
#         image_file = Image.open(image_path)
#
#         # Resize image to 50% bigger
#         width, height = image_file.size
#         new_width = int(width // 3)
#         new_height = int(height // 3)
#         resized_image = image_file.resize((new_width, new_height))
#
#         # contrast improved image
#         contrast_filter = ImageEnhance.Contrast(resized_image)
#         contrast_image_file = contrast_filter.enhance(2)
#
#         # convert the contrasted image to black and white values
#         bw_image_file = contrast_image_file.convert('1', dither=Image.NONE)
#
#         # create a negative of the image
#         inverted_image = ImageOps.invert(bw_image_file)
#
#         # Update image_file to the final processed image
#         image_file = inverted_image
#
#         # show images
#         # image_file.show()
#         # contrast_image_file.show()
#         # bw_image_file.show()
#         # inverted_image.show()
#
#         image_text_list = pytesseract.image_to_string(image_file, config=tesseract_config).split()
#         cont_image_text_list = pytesseract.image_to_string(contrast_image_file, config=tesseract_config).split()
#         bw_image_text_list = pytesseract.image_to_string(bw_image_file, config=tesseract_config).split()
#         neg_image_text_list = pytesseract.image_to_string(inverted_image, config=tesseract_config).split()
#
#         image_text_list = list(set(image_text_list + cont_image_text_list + bw_image_text_list + neg_image_text_list))
#
#         image_text_list_processed = process_tokens(image_text_list)
#         image_text_set = set(image_text_list_processed)
#         print(image_text_set)
#
#
#         # If Tesseract can find the total in the image
#         if "total" in image_text_set:
#             print("Total Found")
#             image_prices = []
#             for elem in image_text_list_processed:
#                 if elem == "$":
#                     continue
#                 elif "$" in set(elem):
#                     price = elem.strip("$")
#                     image_prices.append(float(price))
#                 elif len(elem) == 4 and elem[1] == ".":
#                     if elem.replace('.', '', 1).isdigit():
#                         image_prices.append(float(elem))
#
#             max_price = 30.0
#             filtered_image_prices = [k for k in image_prices if k <= max_price]
#
#             if len(filtered_image_prices) > 0:
#                 total = sorted(filtered_image_prices)[-1]
#             else:
#                 raise Exception("No prices found")
#
#             print(f'Price Found: {filtered_image_prices}')
#             print("Total: ", format(total, '.2f'))
#
#         elif "checkout" in image_text_set:
#             total = float(image_text_list[image_text_list_processed.index("checkout") + 1].strip("$"))
#
#         else:
#             total = 0.0
#             print("ERROR: No Total Price Found in Image")
#
#     else:
#         raise Exception("No Image Found in Directory")
#
#     return format(total, '.2f')
#
#
# def process_tokens(strings_list):
#     punctuation = set("'-?!,:;&#%*()_/")
#     output_list = []
#
#     for token in strings_list:
#         token = token.lower()
#         for char in token:
#             if char in punctuation:
#                 token = token.replace(char, '')
#
#         output_list.append(token)
#
#     return output_list

# def resize_img(img, scale):
#
#     width = int(img.shape[1] * scale / 100)
#     height = int(img.shape[0] * scale / 100)
#
#     dsize = (width, height)
#
#     return cv2.resize(img, dsize=dsize)