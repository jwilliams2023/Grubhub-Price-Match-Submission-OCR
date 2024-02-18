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
        # print("Tesseract text:")
        # print(pytesseract.image_to_string(image_file, config=tesseract_config))

        # Resize image
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
        text = (
                ' '.join(image_text) + ' ' +
                ' '.join(cont_image_text) + ' ' +
                ' '.join(bw_image_text) + ' ' +
                ' '.join(neg_image_text)
                )

        # print("Tesseract joined text: ")
        # print(text)


        # Convert the text to lowercase and remove colons and hyphens
        text = text.lower().replace(':', '').replace('-', '')
        # print("Processed text:")
        # print(text)

        text_as_list = text.split()
        text_as_set = set(text_as_list)
        price_as_float = None

        for label in total_labels:
            print(f'\nSearching for {label}...')
            if label in text_as_set:
                print(f'{label} found in string')

                price_candidates = [text_as_list[i + 1].strip('$') for i in range(len(text_as_list)) if text_as_list[i] == label]
                prices = [item for item in price_candidates if item.replace(".", "").isnumeric()]

                print(f'Price candidates = {price_candidates}')
                print(f'Prices = {prices}')

                if len(prices) == 0:
                    continue

                elif len(prices) == 1 and "." in set(prices[0]):
                    price_as_float = float(prices[0])
                    break

                elif len(prices) > 1 and "." in max(prices):
                    price_as_float = float(max(prices))
                    break

                else:
                    max_price = int(max(prices))
                    if max_price > 100:
                        price_as_float = float(max_price / 100)
                    elif max_price > 1000:
                        price_as_float = float(max_price / 1000)

                    break

        print(f'Price {price_as_float}')
        price_as_string = str(price_as_float).format(total_val, '.2f')

        return price_as_string

# Old Method
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
