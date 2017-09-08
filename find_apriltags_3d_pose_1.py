# AprilTags Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.

import sensor, image, time, math
from pyb import LED

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

# The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
# x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
# translation the units are dimensionless and you must apply a conversion function.

# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
# divided by the y sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# c_x is the image x center position in pixels.
# c_y is the image y center position in pixels.

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)


def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"

def degrees(radians):
    return (180 * radians) / math.pi

red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)
ir_led    = LED(4)

count = 0
while(True):
    status = 'none'

    if count % 30 == 0:
        status = 'ping'
        args = (count, clock.fps())
        print("st, ping, frameCount: %d, fps: %f, ed" % args)

    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(families=image.TAG16H5): # defaults to TAG36H11
        status = 'detect'
        # img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        # img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print_args = (tag.id(), tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
        # Translation units are unknown. Rotation units are in degrees.
        print("st, position, ID: %d, Tx: %f, Ty: %f, Tz: %f, Rx: %f, Ry: %f, Rz: %f, ed" % print_args)

    count+=1

    if status == 'none':
        red_led.off()
        green_led.off()
        blue_led.off()
    elif status == 'detect':
        red_led.off()
        blue_led.on()
        green_led.off()
    elif status == 'ping':
        red_led.off()
        blue_led.off()
        green_led.on()

