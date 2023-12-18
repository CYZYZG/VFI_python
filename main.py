import cv2
import numpy as np
import argparse
from util import *

parser = argparse.ArgumentParser()
parser.add_argument('--in_file', type=str,
                    default='F:\\test.yuv', help='in_file')
parser.add_argument('--out_file', type=str,
                    default='F:\outYUV1.yuv', help='out_file')
parser.add_argument('--width', type=int, default=1920, help='width')
parser.add_argument('--height', type=int, default=1080, help='height')
parser.add_argument('--startfrm', type=int, default=0, help='startfrm')
parser.add_argument('--endfrm', type=int, default=1, help='endfrm')
parser.add_argument('--BitDepth', type=int, default=8, help='BitDepth')
parser.add_argument('--pix_fmt', type=str, default='420', help='pix_fmt')
args = parser.parse_args()


def main(args):
    BitDepth = args.BitDepth
    width = args.width
    height = args.height
    yuv_file = open(args.in_file, 'rb')
    outyuv_file = open(args.out_file, 'wb')
    framesize = width*height
    yuv_file.seek(0, 2)  # 设置文件指针到文件流的尾部
    ps = yuv_file.tell()  # 当前文件指针位置
    numfrm = ps//framesize  # 计算输出帧数
    yuv_file.seek(framesize*args.startfrm, 0)
    input_frame = Frame(width, height, args.pix_fmt, BitDepth)
    endfrm = numfrm if args.endfrm > numfrm else args.endfrm
    for i in range(args.startfrm, endfrm):
        load_yuv(yuv_file, input_frame)

        write_yuv(outyuv_file, input_frame)
    print(input_frame.width)

    yuv_file.close
    outyuv_file.close


if __name__ == "__main__":
    main(args)
