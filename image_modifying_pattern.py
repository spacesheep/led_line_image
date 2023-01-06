#!/usr/bin/env python3

############### to test ###############
# /Applications/anaconda3/bin/python /Users/gnlacaz/WORK/CODES/led_line_image/image_modifying_pattern.py  --fileName /Users/gnlacaz/PERSO/PixelBlaze_experiments/hearts04.png 
################ end to test ##########
import argparse
from PIL import Image, ImageSequence
from pixelblaze import *

if __name__ == "__main__":

    # Use the first Pixelblaze available on the network, or...
    for ipAddress in Pixelblaze.EnumerateAddresses(timeout=1500):
        print("Found Pixelblaze at ", ipAddress)
        # pb = Pixelblaze(ipAddress)
        break

    # Create the top-level parser.
    parser = argparse.ArgumentParser(prog='animate')
    # parser.add_argument("--ipAddress", required=True, help="The IP address of the Pixelblaze")
    parser.add_argument("--fileName", required=True, help="The animated GIF/PNG file to be sent to the Pixelblaze")
    # Parse the command line.
    args = parser.parse_args()

    # Open the image file and analyze it.
    with Image.open(args.fileName, mode='r') as im:
        print(f"Image : width={im.width}, height = {im.height} pixels, with {im.n_frames} frames.")

        # Connect to the Pixelblaze.
        with Pixelblaze(ipAddress) as pb:
            # Query the pixelcount of the Pixelblaze.
            pixelCount = pb.getPixelCount()
            print(f"Pixelblaze has {pixelCount} pixels")

            ###################### function rendered in binary ####################
            # // _v contains the intensity of the pixels for the entire strip
            # export var _v = array(pixelCount);
            # // _freq is the refresh frequency between each frames
            # export var _t = 0.001;
            # // _h is the hue value (basically the color) set for all LEDs in the strip
            # export var _h = 0.05;


            # for (i = 0; i < pixelCount; i++) {
            # _v[i] = 0
            # if (i == 30){
            #     _v[i]= 1
            # }

            # }

            # export function beforeRender(delta) {
            # t1 = square(time(_t),0.5)

            # // t1 = time ( max(0, cos(2 * PI * _t)) )
            # }

            # export function render(index) {
            # h = _h
            # s = 1
            # // v = _v[index] * max(0,cos(2* PI * t1))
            # v = _v[index] * t1
            # hsv(h, s, v)
            # }
            ##################### end function rendered in binary ####################
            pb.setActivePatternByName("Copy of flying fish")
            pb.setActiveVariables({"_t": 0.00004})

            # Convert the image into an grey scale sequence (i.e. remove the GIF palette).
            convertedFrame = im.convert(mode='L') #< 'L' = grey scale, 'RGB' also possible
            # Rescale this frame to match the Pixelblaze's dimensions.
            # width , height 
            resizedFrame = convertedFrame.resize((int(im.width * pixelCount / im.height), pixelCount), resample=Image.Resampling.NEAREST)
            #resizedFrame = convertedFrame.resize((100, pixelCount), resample=Image.Resampling.NEAREST)
            print(f"resized Image : width={resizedFrame.width}, height = {resizedFrame.height} pixels")

            # pre-compute the pixel mapping
            w = resizedFrame.width
            h = resizedFrame.height
            
            pixMatrix = []
            for col in range(w):   
                # extract intensity val of each pixel col 
                pixVal = []
                for row in range(h):
                    localVal = resizedFrame.getdata()[row * w +  col]
                    pixVal.append(localVal/255)
                pixMatrix.append(pixVal)

            # Set an exception handler to catch [Ctrl-C].
            try:
                print("Rendering image...press [Ctrl]-[C] to exit.")
                # Loop through the image frames.
                while True:
                    for col in range(w):
                      pb.setActiveVariables({"_v": pixMatrix[col]})
                        # time.sleep(0.1)
            except KeyboardInterrupt:
                # Clear the frame and exit.
                clearFrame = []
                for pixel in range(pixelCount): clearFrame.append(0)
                pb.setActiveVariables({ "_v": clearFrame})
                print("")