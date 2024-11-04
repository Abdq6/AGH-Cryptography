from PIL import Image
import numpy

img = Image.open("Input/small_image.jpg") #wczytujemy obraz pil-em

np_img = numpy.array(img) # obraz do macierzy
print(np_img.shape)

for i in range(np_img.shape[1]):
    row = np_img[:, i, :].flatten() # R G B repeat
    print(row)

'''
one_row_matrix = numpy.column_stack((red_channel, green_channel, blue_channel))
print(one_row_matrix.shape)
combined_matrix = one_row_matrix.reshape(719, 719, 3)
print(combined_matrix.shape)
'''

pilImage = Image.fromarray(combined_matrix) #macierz do pil-a
pilImage.save('Output/kicius-z-tablicy.png') #zapis pila do pliku
