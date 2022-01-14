import time
import board
import busio
import digitalio
import python_osc


from PIL import Image, ImageDraw, ImageFont

import subprocess

# Screen Sizes
WIDTH = 128
HEIGHT = 64
BORDER = 5

# use for i2c
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display
oled.fill(0)
oled.show()

# Crate blank image for drawing
# Make sure to create image with '1' for 1-bit colour
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0) oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.tff', 16)




while true:

    # draws a black background to clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    device_name = "Camera 1"
    device_status = ()


    draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((0, 16), device_name, font=font, fill=255)
    draw.text((0, 32), device_status, font=font, fill=255)

    oled.image(image)
    oled.show()
    time.sleep(.1)

