from PIL import Image

# read image (in the future, read from network socket)
image = Image.open("Input/small_image.jpg")

# (black and white))
bw_image = image.convert("L")
# bw_image.show()  # image display

# rotate 90 deg right
rotated_image = image.rotate(-90, expand=True)
# rotated_image.show()

# mirror
flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
# flipped_image.show()

bw_image = bw_image.convert("RGB")
rotated_image = rotated_image.convert("RGB")
flipped_image = flipped_image.convert("RGB")

# save output (in the future, write to network socket)
bw_image.save("Output/BW.jpg")
rotated_image.save("Output/Rotated.jpg")
flipped_image.save("Output/Fliped.jpg")
