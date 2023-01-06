# Simple Pixelblaze run-time control example

from pixelblaze import *

if __name__ == "__main__":

    # Use the first Pixelblaze available on the network, or...
    for ipAddress in Pixelblaze.EnumerateAddresses(timeout=1500):
        print("Found Pixelblaze at ", ipAddress)
        pb = Pixelblaze(ipAddress)
        break

# ... uncomment the line below (and comment out the "for ipAddress..." block above)
# to specify the IP address of the Pixelblaze you want
# pb = Pixelblaze("192.168.4.1")

# select a pattern (use a pattern name you know is
# available on your Pixelblaze. It must be spelled exactly
# as it appears in the Pixelblaze web UI
pb.setActivePatternByName("fireflies")

pixel_count = pb.getPixelCount()
print("pixel count =", pixel_count)

# see if the selected pattern has a color control, and
# attempt to set the color to blue.  Note that the library
# does not currently attempt to provide HSV<->RGB conversion,
# so you must use the format appropriate for your pattern.
col = pb.getColorControlName()
print("Color control name is: ", col)

# following is useless if col = None
# # using HSV color if the pattern has an HSV picker
# pb.setColorControl(col,[0.6667,1,1])
# pb.setColorControl(col,[0.6,0,0])
# using RGB color if the color has an RGB picker
pb.setColorControl(col, [0, 0, 1])

# get the current brightness level, then
# set brightness to 80%
bri = pb.getBrightnessSlider()
print("Brightness was ", bri)

pb.setBrightnessSlider(0.8)
print("now Brightness is ", bri)
