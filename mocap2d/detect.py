import argparse
from glob import glob
import json
import warnings
import socket
from os import path

import cv2

from mocap2d import BoneDetector


def detect(args):
    if args.out and not path.isdir(args.out):
        print(f"Output path {args.out} is not a directory")
        exit(2)

    if not glob(args.file[0]):
        print(f"Video file at {args.file[0]} not found.")
        exit(1)

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
    print(f"[>{'.' * 50}] 0%\r", end='')

    pos0 = None
    for idx in range(frame_count):
        ret, frame = video.read()

        if idx % fpi == 0:
            bones, pos = detector.extract_bone(frame, args.show)
            if pos0 is None:
                pos0 = pos
            print(f"{pos[0] - pos0[0]}, {pos[1] - pos0[1]}")
            bones["timestamp"] = round(idx / fps, 3)
            bone_list.append(json.dumps(bones))
            curr = 50 * idx // frame_count
            print(f"[{'=' * curr}>{'.' * (50 - curr)}] "
                  f"{round(100 * idx / frame_count, 2)}%\r", end='')
    print(f"[{'=' * 50}>] 100%     ")
    cv2.destroyAllWindows()
    video.release()

    if args.out:
        with open(path.join(args.out, "result.json"), 'w') as out_file:
            out_file.writelines([bone + '\n' for bone in bone_list])

    print('--' * 50)
    print("Motion Capture complete")
    return bone_list


def send(args):
    if '.json' not in args.file[0]:
        print("Please provide the json file with the pose data")
        exit(4)

    print(f"Retrieving data from {args.file[0]}")
    bone_list = []
    with open(args.file[0], 'r') as json_file:
        line = json_file.readline()
        while line:
            bone_list.append(line)
            line = json_file.readline()
    print("Pose data is ready\n")
    return bone_list


def main():
    warnings.filterwarnings("ignore", category=UserWarning)
    parser = argparse.ArgumentParser(
        description="Unity extension for 2D motion capture asset"
    )
    parser.add_argument('command', metavar='{ detect, send }',
                        help="detect: analyze video file and send / "
                             "send: send json result without analyzing",
                        type=str)

    parser.add_argument('-f', '--file', dest="file", required=True, nargs=1,
                        help="Path to the video file", type=str)
    parser.add_argument('-g', '--gpu', dest="gpu", action="store_true",
                        help="Run on gpu instance")
    parser.add_argument('-i', '--interval', dest='interval', type=float,
                        help="Interval between key frames in seconds",
                        default=0.2)
    parser.add_argument('-s', '--show', dest='show', action="store_true",
                        help="Show the result of analysis during the process.")
    parser.add_argument('-o', '--output', dest='out', type=str,
                        help="Directory to save the result in a json format")
    args = parser.parse_args()

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

    bone_list = []
    if args.command == "detect":
        bone_list = detect(args)
    elif args.command == "send":
        bone_list = send(args)
    else:
        print("Please enter a valid commad of either 'send' or 'detect'")
        exit(3)

    print('Receive data at Unity by hitting "Connect to Detector" button')

    host = "127.0.0.1"
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            app_name = conn.recv(1024).decode()
            print(f'Connected to Unity project [{app_name}]')
            for bone in bone_list:
                conn.sendall(bone.encode())
                conn.recv(1024)
        print("Transfer Successful")


if __name__ == '__main__':
    main()
