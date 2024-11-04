import numpy as np
from Pyfhel import Pyfhel
from PIL import Image

img = Image.open("Input/small_image.jpg") #wczytujemy obraz pil-em

HE = Pyfhel()
HE.contextGen(scheme='bfv', n=2**15, t_bits=20)
HE.keyGen()

np_img = np.array(img) # obraz do macierzy
print(np_img.shape)
red_channel = np_img[:, :, 0].flatten()
green_channel = np_img[:, :, 1].flatten()
blue_channel = np_img[:, :, 2].flatten()
print(red_channel.shape)

one_row_matrix = np.stack((red_channel, green_channel, blue_channel), axis=1)
print("one_row_matrix.shape:", one_row_matrix.shape)

# Spłaszczenie macierzy do wektora jednowymiarowego
integer1 = one_row_matrix.flatten().astype(np.int64)

print("integer1.shape:", integer1.shape)

ctxt1 = HE.encryptInt(integer1) # Encryption makes use of the public key

print("3. Integer Encryption, ")
print("    int ",integer1,'-> ctxt1 ', type(ctxt1))

print(ctxt1)

# %%
# 4. Operating with encrypted integers
# --------------------------------------
# Relying on the context defined before, we will now operate
# (addition, substaction, multiplication) the two ciphertexts:
#ctxtSum = ctxt1 + ctxt2         # `ctxt1 += ctxt2` for inplace operation
#ctxtSub = ctxt1 - ctxt2         # `ctxt1 -= ctxt2` for inplace operation
#ctxtMul = ctxt1 * ctxt2         # `ctxt1 *= ctxt2` for inplace operation
#print("4. Operating with encrypted integers")
#print(f"Sum: {ctxtSum}")
#print(f"Sub: {ctxtSub}")
#print(f"Mult:{ctxtMul}")

# %%
# 5.  Decrypting integers
# ---------------------------
# Once we're finished with the encrypted operations, we can use
# the Pyfhel instance to decrypt the results using `decryptInt`:
#resSum = HE.decryptInt(ctxtSum) # Decryption must use the corresponding function
                                #  decryptInt.
#resSub = HE.decryptInt(ctxtSub)
#resMul = HE.decryptInt(ctxtMul)
#print("#. Decrypting result:")
#print("     addition:       decrypt(ctxt1 + ctxt2) =  ", resSum)
#print("     substraction:   decrypt(ctxt1 - ctxt2) =  ", resSub)
#print("     multiplication: decrypt(ctxt1 + ctxt2) =  ", resMul)



# sphinx_gallery_thumbnail_path = 'static/thumbnails/helloworld.png'