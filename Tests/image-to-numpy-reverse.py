from PIL import Image
import numpy as np

img = Image.open("Input/small_image.jpg") #wczytujemy obraz pil-em

np_img = np.array(img) # obraz do macierzy
print(np_img.shape)

server_image = np.zeros((719,719,3), dtype=np.uint8)
print(server_image.shape)

for i in range(np_img.shape[1]):
    row_before_flatten = np_img[:, i, :]

    row = np_img[:, i, :].flatten() # R G B repeat
    #

    #server side

    new_row = row.reshape(719, 3)

    server_image[:,i,:] = new_row




'''

import numpy as np
ini_array = np.array([[1, 2, 3], [45, 4, 7], [9, 6, 10]])
# printing initial array
print("initial_array : ", str(ini_array));
# Array to be added as column
column_to_be_added = np.array([[1], [2], [3]])
# Adding column to array using append() method
arr = np.append(ini_array, column_to_be_added, axis=1)
# printing result
print ("resultant array", str(arr))
'''



#pilImage = Image.fromarray(combined_matrix) #macierz do pil-a
#pilImage.save('Output/kicius-z-tablicy.png') #zapis pila do pliku
