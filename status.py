import subprocess
import spidev as SPI
import logging
import ST7789
import time

from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)
# 240x240 display with hardware SPI:
disp = ST7789.ST7789()

# Initialize library.
disp.Init()

# Clear display.
disp.clear()

#Set the backlight to 100
disp.bl_DutyCycle(100)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = 240  # we swap height/width to rotate it to landscape!
width =  240
#image = Image.new("RGB", (width, height))
image = Image.new("RGB", (disp.width, disp.height), "WHITE")
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
im_r=image.rotate(rotation)
disp.ShowImage(im_r)
#disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
#Font0 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
Font0 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",21)
Font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",24)
Font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",32)
Font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",35)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = 'df -h | awk \'$NF=="/mnt/data"{printf "M.2: %d/%d GB  %s", $3,$2,$5}\''
    M2 = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    #cmd = "nvme list | awk 'NR==3{printf \"NVMe: %.1f/%.1f %s \",$8,$10,$11}'"
    cmd = "lsblk | awk '/nvme0n1/{printf \"NVME: %d GB         \", $4}'"
    NVMe = subprocess.check_output(cmd, shell=True).decode("utf-8")

    cmd = "cat /sys/devices/platform/cooling_fan/hwmon/*/fan1_input |  awk '{printf \"FAN Speed: %d RPM\", $(NF-0)}'"
    FAN = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.
    y = top
    draw.text((x,y),'Raspi M.2 HAT',font=Font2,fill="WHITE")

    y = y + 40
    draw.text((x, y), IP, font=Font1, fill="RED")

    # y += Font1.getsize(IP)[1]
    y = y + 30
    draw.text((x, y), CPU, font=Font1, fill="YELLOW")

    # y += Font1.getsize(CPU)[1]
    y = y + 30
    draw.text((x, y), MemUsage, font=Font1, fill="#00FF00")

    # y += Font1.getsize(MemUsage)[1]
    y = y + 30
    draw.text((x, y), Disk, font=Font1, fill="BLUE")

    # y += Font1.getsize(Disk)[1]
    # y = y + 30
    # draw.text((x, y), M2, font=Font1, fill="#00FFFF")

    # y += Font1.getsize(M2)[1]
    y = y + 30
    draw.text((x, y), Temp, font=Font1, fill="#FF00FF")

    # y += Font1.getsize(Temp)[1]
    y = y + 30
    draw.text((x, y), NVMe, font=Font1, fill="#F0F0F0")

    # y += Font0.getsize(NVMe)[1]
    y = y + 30
    draw.text((x, y), FAN, font=Font0, fill="#FFF000")
    # y += Font0.getsize(FAN)[1]
 

    # Display image.
    im_r=image.rotate(0)
    disp.ShowImage(im_r)
    #disp.image(image, rotation)
    time.sleep(0.1)
