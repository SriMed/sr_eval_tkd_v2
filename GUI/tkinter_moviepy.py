import time
import tkinter as tk
import imageio
from PIL import Image, ImageTk

global pause_video

video_name = '../xy_Static/front_kick_side2.mp4'
video = imageio.get_reader(video_name)


def video_frame_generator():
    def current_time():
        return time.time()

    start_time = current_time()
    _time = 0
    for frame, image in enumerate(video.iter_data()):

        # turn video array into an image and reduce the size
        image = Image.fromarray(image)
        image.thumbnail((750, 750), Image.ANTIALIAS)

        # make image in a tk Image and put in the label
        image = ImageTk.PhotoImage(image)

        # introduce a wait loop so movie is real time -- asuming frame rate is 24 fps
        # if there is no wait check if time needs to be reset in the event the video was paused
        _time += 1 / 50
        run_time = current_time() - start_time
        while run_time < _time:
            run_time = current_time() - start_time
        else:
            if run_time - _time > 0.1:
                start_time = current_time()
                _time = 0

        yield frame, image

def _stop():
    global pause_video
    pause_video = True

def _start():
    global pause_video
    pause_video = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Video in tkinter')

    my_label = tk.Label(root)
    my_label.pack()
    tk.Button(root, text='start', command=_start).pack(side=tk.LEFT)
    tk.Button(root, text='stop', command=_stop).pack(side=tk.LEFT)

    pause_video = False
    movie_frame = video_frame_generator()

    while True:
        if not pause_video:
            frame_number, frame = next(movie_frame)
            my_label.config(image=frame)
        root.update()
