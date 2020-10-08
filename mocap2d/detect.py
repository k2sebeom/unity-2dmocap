import argparse
from glob import glob
import json
import warnings
import socket

import cv2

from mocap2d import BoneDetector


def main():
    warnings.filterwarnings("ignore", category=UserWarning)
    parser = argparse.ArgumentParser(
        description="Unity extension for 2D motion capture asset"
    )
    parser.add_argument('-f', '--file', dest="file", required=True, nargs=1,
                        help="Path to the video file", type=str)
    parser.add_argument('-g', '--gpu', dest="gpu", action="store_true",
                        help="Run on gpu instance")
    parser.add_argument('-i', '--interval', dest='interval', type=float,
                        help="Interval between key frames in seconds",
                        default=0.2)
    parser.add_argument('-s', '--show', dest='show', action="store_true",
                        help="Show the result of analysis during the process.")
    args = parser.parse_args()

    if not glob(args.file[0]):
        print(f"Video file at {args.file[0]} not found.")
        exit(1)
    print('==' * 50)
    print('''
        #####    #####         ##       ##               #####       
       #######   ##  ###       ####   ####              ####        
            ##   ##    ##      ## ## ## ##             ##             
           ##    ##     ##     ##  ###  ##    ###     ##             
          ##     ##    ##      ##       ##   #   #     ##         ######     ######
        ##       ### ###       ##       ##   #   #      ####     ##    ##    ##   ##
       #######   #####         ##       ##    ###        #####    ####  ##   #####
                                                                             ##
                                                                             ##    by k2sebeom''')
    print("==" * 50 + '\n')
    print("Initializing pose detector...")
    detector = BoneDetector(gpu=args.gpu)
    print()
    print(f"Reading video file at {args.file[0]}")
    video = cv2.VideoCapture(args.file[0])
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = args.interval
    fpi = int(interval * fps + 1)
    print(f"{args.file[0]}: FPS = {fps}, FRAME COUNT = {frame_count}")
    print('--' * 50)
    print("Start processing the motion capture")
    bone_list = []
    print(f"[>{'.'*50}] 0%\r", end='')
    for idx in range(frame_count):
        ret, frame = video.read()

        if idx % fpi == 0:
            bones = detector.extract_bone(frame, args.show)
            bones["timestamp"] = round(idx / fps, 3)
            bone_list.append(json.dumps(bones))
            curr = 50 * idx // frame_count
            print(f"[{'=' * curr}>{'.' * (50 - curr)}] "
                  f"{round(100 * idx / frame_count, 2)}%\r", end='')
    print(f"[{'=' * 50}>] 100%")
    cv2.destroyAllWindows()
    video.release()
    print('--' * 50)
    print("Motion Capture complete")
    print('Receive data at Unity by hitting "Connect to Detector" button')

    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            app_name = conn.recv(1024).decode()
            print(f'Connected to Unity project [{app_name}]')
            for bone in bone_list:
                conn.sendall(bone.encode())
                conn.recv(1024)
        print("Transfer Successful")
