import matplotlib.image as img

file = "data/01.jpg"

images = [None] * 12

for i in range(1, 12): 
    if i < 10:
        file = "data/0" + str(i) + ".jpg"
    else : 
        file = "data/" + str(i) + ".jpg"

    images[i] = img.imread(file)


# Feature Vector 
# 1. Colour content
# 2. Colour distribution around the central point
# 3. Colour distribution around several points
# 4. Luminance distributions around one or several points 5. Edge positions and orientations





