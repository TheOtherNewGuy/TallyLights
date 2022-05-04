from datetime import datetime
#import time
import board
import busio
import digitalio
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

#FAFO with this tomorrow
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 2

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 16)
fontLarge = ImageFont.truetype('PixelOperatorMono.ttf', 54)
#font = ImageFont.load_default()

def displayStatus(oscPath, status):
    print(oscPath)
    print(status)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # Status is the string sent from Bitfocus Companion
    draw.text((10, 18), status, font=fontLarge, fill=255)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    # Displays IP and Current time
    draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((0, 11), datetime.now().strftime("%H:%M:%S"), font=font, fill=255)
    draw.text((64, 11), "Camera 1", font=font, fill=255)


    #make OSC command to show poop because Sam.
    #image = Image.open("LYw4POpF_normal.jpeg")
    #image = image.convert(mode="1")
    #image = image.resize((128, 64))
    # Display image
    oled.image(image)
    oled.show()      

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/status", displayStatus)

server =  osc_server.BlockingOSCUDPServer(("0.0.0.0", 3456), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

# example syntax: displayStatus("LIVE")
