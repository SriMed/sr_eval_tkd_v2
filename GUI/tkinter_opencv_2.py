import tkinter
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name

cap = cv2.VideoCapture('../xy_Static/front_kick_side2.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


main = tkinter.Tk()
main.title = "Evaluating TKD Moves"

canvas = tkinter.Canvas(main, width=width, height=height)
canvas.pack()


def display():
    if (cap.isOpened()): # Read until video is completed
    # Capture frame-by-frame

        ret, frame = cap.read()
        if ret:
            # Display the resulting frame
            photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            canvas.create_image(0, 0, image=photo)

            main.after(15, display)

display()
main.mainloop()

cap.release()
cv2.destroyAllWindows()
