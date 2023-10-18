# import selenium
import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
#result = reader.readtext('/content/3 lead ECG.jpg')
import cv2
import numpy as np
import matplotlib.pyplot as plt

#use matplotlib.pyplot.imshow() instead of cv2_imshow()
# from google.colab.patches import cv2_imshow


n = int(input("Enter the number of images: "))

image_paths = []

# Prompt the user to input the image paths
for i in range(n):
    image_path = input(f"Enter the path for image {i+1}: ")
    image_paths.append(image_path)

#defining the zoom function once to be called ahead
def zoom(img, zoom_factor=2):
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)

#stores the detected text and its bounding boxes
results = []

for i in image_paths:
    img = cv2.imread(i)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    xx, yy = img.shape[0], img.shape[1]
    img = img[250:450, 1:yy]
    img_zoomed = zoom(img, 3)
    result = reader.readtext(img_zoomed, detail=1)
    results.append(result)

    # plt.imshow(img)

    print(result)

# results = []

# for i in image_paths:
#     img = cv2.imread(i)
#     img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
#     result = reader.readtext(img, detail=1)
#     results.append(result)

#     print(result)



# Process OCR results from all images
for i in results:
    for m in range(len(result)):
        print(i[m][1])



#instead of usinf ifs multiple times, we are suing dictioanry
#for all "or" conditions we are providing the same value pairs

coord_mappings = {
    'aVR': ('avrh', 'avrw'),
    'JVR': ('avrh', 'avrw'),
    'Jaur': ('avrh', 'avrw'),
    '@VF': ('avfh', 'avfw'),
    'JVF': ('avfh', 'avfw'),
    'aVF': ('avfh', 'avfw'),
    'aVC': ('avlh', 'avlw'),
    'JVL': ('avlh', 'avlw'),
    'JL': ('avlh', 'avlw'),
    'VI': ('v1h', 'v1w'),
    'V2': ('v2h', 'v2w'),
    'VZ': ('v2h', 'v2w'),
    'V3': ('v3h', 'v3w'),
    'V4': ('v4h', 'v4w'),
    'W4': ('v4h', 'v4w'),
    'V5': ('v5h', 'v5w'),
    'VS': ('v5h', 'v5w'),
    'W5': ('v5h', 'v5w'),
    'V6': ('v6h', 'v6w'),
    'U6': ('v6h', 'v6w'),
    'W6': ('v6h', 'v6w'),
    'Pal': ('ph', 'pw'),
    'Pat': ('ph', 'pw')
}

for img_index in range(len(results)):
    img = results[img_index]
    result = result[img_index]
    # y_len, x_len, _ = img.shape


final_images = []
#this will store the final images that will be extracted from the rolls 
    
    

for m in range(len(result)):
        label = str(result[m][1])
        if label in coord_mappings:
            height, width = coord_mappings[label]
            height_val = result[m][0][0][0]
            width_val = result[m][0][0][1]

            y_len, x_len, _ = img.shape
            
            extracted_img = img[int((width_val - 10) / 3):int(x_len / 3), int(height_val / 3):int(height_val / 3) + int((width_val - 10) / 3)]
            plt.imshow(extracted_img)

             # Append the extracted image to the list
            final_images.append(extracted_img)

            # Display the extracted image (optional)
            plt.imshow(extracted_img)
            plt.show()  # Show the plot


## the code aims to process OCR results from input images, using a dictionary to map labels to coordinates, and extracts 
# regions of interest from the images based on the coordinates of the labels, and iteratively 
#store it in the final_images that will be later used to compile thesse images in one frame.





