from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Import and resize images 

images = [None] * 12

for i in range(0, 12): 
    if i < 9:
        file = "data/0" + str(i + 1) + ".jpg"
    else : 
        file = "data/" + str(i + 1) + ".jpg"

    im = Image.open(file)
    resized_image = im.resize((100, 100))
    images[i] = np.array(resized_image)


# Find and create features 

RGB_Data = [None] * 11
RGB_Middle_Data = [None] * 11
RGB_Middle_Several_Data = [None] * 11
Luminance_Data = [None] * 11
Edge_Data = [None] * 11

for i in range(0,11):
    
    # Color content - average RGB values
    image_rgb = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
    avg_rgb = np.mean(image_rgb, axis=(0, 1))
    RGB_Data[i] = avg_rgb
    
    # Color distribution around the central point
    top_left_x = (100 - 20) // 2
    top_left_y = (100 - 20) // 2
    bottom_right_x = top_left_x + 20
    bottom_right_y = top_left_y + 20

    region_of_interest = images[i][top_left_y:bottom_right_y, top_left_x:bottom_right_x]
    avg_rgb_middle = np.mean(region_of_interest, axis=(0, 1))
    RGB_Middle_Data[i] = avg_rgb_middle
    
    # Color distribution around several points
    quadrant_width = 50
    quadrant_height = 50
    sum = 0
    sum2 = 0

    for j in range(4):

        if j == 0:
            top_left_x = 0
            top_left_y = 0
        elif j == 1:
            top_left_x = quadrant_width
            top_left_y = 0
        elif j == 2:
            top_left_x = 0
            top_left_y = quadrant_height
        else:
            top_left_x = quadrant_width
            top_left_y = quadrant_height

        bottom_right_x = top_left_x + 20
        bottom_right_y = top_left_y + 20

        region_of_interest = images[i][top_left_y:bottom_right_y, top_left_x:bottom_right_x]
        avg_rgb_middle = np.mean(region_of_interest, axis=(0, 1))
        
        sum = avg_rgb_middle + sum 
        
        # Luminance distributions around one or several points
        gray_image = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
        histogram, bins = np.histogram(gray_image.flatten(), bins=256, range=[0, 256])
        cdf = histogram.cumsum()
        cdf_normalized = cdf * histogram.max() / cdf.max()
        sum2 = sum2 + cdf_normalized
        
    RGB_Middle_Several_Data[i] = sum / 4
    Luminance_Data[i] = sum2 / 4
    
    # Edge positions and orientations
    image_grey = cv2.cvtColor(images[i], cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image_grey, threshold1=100, threshold2=200)  # Adjust threshold values as needed
    edge_count = np.count_nonzero(edges)
    edge_density = edge_count / (edges.shape[0] * edges.shape[1])
    mean_edge_intensity = np.mean(image_grey[edges != 0])
    std_edge_intensity = np.std(image_grey[edges != 0])
    orientation_hist, _ = np.histogram(np.arctan2(cv2.Sobel(image_grey, cv2.CV_64F, 0, 1, ksize=3), cv2.Sobel(image_grey, cv2.CV_64F, 1, 0, ksize=3))[edges != 0], bins=10, range=(-np.pi, np.pi))

    Edge_Data[i] = (edge_density + mean_edge_intensity + std_edge_intensity + orientation_hist) / 4


# Calculate distance matrix 

feature_vector = [None] * 11
counter = 0

for i in range(0,11): 
    
    feature_vector[i] = [RGB_Data[i], RGB_Middle_Data[i], RGB_Middle_Several_Data[i], Luminance_Data[i], Edge_Data[i]]
    

def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    cosine_similarity = dot_product / (norm_a * norm_b)
    
    return cosine_similarity

distance_matrix = np.zeros((11, 11))

for i in range(0,11):
    for j in range(0,11):
        if i != j:
            rbs_similarity = cosine_similarity(RGB_Data[i], RGB_Data[j])
            rbsm_similarity = cosine_similarity(RGB_Middle_Data[i], RGB_Middle_Data[j])
            rbsms_similarity = cosine_similarity(RGB_Middle_Several_Data[i], RGB_Middle_Several_Data[j])
            lum_similarity = cosine_similarity(Luminance_Data[i], Luminance_Data[j])
            edge_similarity = cosine_similarity(Edge_Data[i], Edge_Data[j])
            
            tot = (rbs_similarity + rbsm_similarity + rbsms_similarity + lum_similarity + edge_similarity)/5
            distance_matrix[i][j] = tot
        else :
            distance_matrix[i][j] = 1
        

choose_image = 5

choose_matrix = distance_matrix[choose_image]

fig = plt.figure(figsize=(10, 10))
for i in range(0,12):
    fig.add_subplot(3, 4, i+1)
    fig.add_title = plt.title("Image " + str(i) + " - " + "{:.3f}".format(round(choose_matrix[i-1], 3)))
    plt.imshow(images[i])

plt.show()





            