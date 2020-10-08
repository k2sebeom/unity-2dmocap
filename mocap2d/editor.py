import tkinter as tk
import cv2
import argparse
from glob import glob
import sys
from os import path


global rotate, curr, frame_shape


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest="file", required=True, nargs=1,
                        help="Path to the video file", type=str)
    args = parser.parse_args()

    if not glob(args.file[0]):
        print(f"Video file at {args.file[0]} not found.")
        exit(1)

    video = cv2.VideoCapture(args.file[0])
    fps = video.get(cv2.CAP_PROP_FPS)
    frames = []
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)
    video.release()

    global rotate, curr, frame_shape
    rotate = 0
    curr = 0
    frame_shape = frames[0].shape[:2][::-1]

    def get_image():
        image = frames[curr]
        image = cv2.resize(image, frame_shape)
        for _ in range(rotate % 4):
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return image

    def show_image():
        cv2.imshow(title, get_image())
        cv2.waitKey(1)

    window = tk.Tk()
    title = "Simple Video Editor"
    window.title(title)
    window.geometry("500x150")

    def change_point(val):
        global curr
        curr = int(val)
        show_image()

    tk.Label(window, text="Starting point").place(x=5, y=5)
    trim_start = tk.Scale(window, from_=0, to=len(frames) - 1,
                          orient=tk.HORIZONTAL, command=change_point,
                          showvalue=False)
    trim_start.place(x=90, y=5, width=400)

    tk.Label(window, text="Ending point").place(x=5, y=35)
    trim_end = tk.Scale(window, from_=0, to=len(frames) - 1,
                        orient=tk.HORIZONTAL, command=change_point,
                        showvalue=False)
    trim_end.place(x=90, y=35, width=400)
    trim_end.set(len(frames) - 1)

    def rotate_clock():
        global rotate
        rotate += 1
        show_image()

    def rotate_counter():
        global rotate
        rotate -= 1
        show_image()

    btn1 = tk.Button(window, text="CounterClock", command=rotate_counter)
    btn1.place(x=5, y=65)
    btn2 = tk.Button(window, text="ClockWise", command=rotate_clock)
    btn2.place(x=95, y=65)

    tk.Label(window, text="width =").place(x=185, y=65)
    w = tk.Entry(window)
    w.place(x=235, y=65, width=40)
    tk.Label(window, text="height =").place(x=285, y=65)
    h = tk.Entry(window)
    h.place(x=345, y=65, width=40)

    def resize():
        global frame_shape
        if w.get() and h.get() and int(w.get()) > 0 and int(h.get()) > 0:
            frame_shape = (int(w.get()), int(h.get()))
            show_image()

    tk.Button(window, text="Resize", command=resize).place(
        x=395, y=60, width=70)

    def save_video():
        global curr
        if int(trim_start.get()) > int(trim_end.get()):
            print("Invalid Trim points")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        filename = path.basename(args.file[0]).split('.')[0] + '.mp4'
        new_path = path.join(path.dirname(args.file[0]), 'new-' + filename)
        vid_shape = get_image().shape[:2][::-1]
        out = cv2.VideoWriter(new_path, fourcc, fps, vid_shape)
        for idx in range(int(trim_start.get()), int(trim_end.get()) + 1):
            curr = idx
            show_image()
            out.write(get_image())
        out.release()
        print(f"Generated Video at {new_path}")

    tk.Button(window, text="Save", command=save_video).place(
        x=5, y=100, width=490, height=40)

    show_image()

    window.mainloop()
