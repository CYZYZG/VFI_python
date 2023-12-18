import numpy as np
import gc


class Frame():
    width, height, uv_w, uv_h = 0
    pix_fmt = ''
    BitDepth = 0
    Yt = 0
    Ut = 0
    Vt = 0

    def __init__(self, width, height, pix_fmt, BitDepth):
        self.width = width
        self.height = height
        self.pix_fmt = pix_fmt
        self.BitDepth = BitDepth
        if self.pix_fmt == '444':
            self.uv_w = self.width
            self.uv_h = self.height
        elif self.pix_fmt == '422':
            self.uv_w = self.width//2
            self.uv_h = self.height
        else:
            self.uv_w = self.width//2
            self.uv_h = self.height//2

    def init_buff(self):
        if self.pix_fmt == '444':
            self.uv_w = self.width
            self.uv_h = self.height
        elif self.pix_fmt == '422':
            self.uv_w = self.width//2
            self.uv_h = self.height
        else:
            self.uv_w = self.width//2
            self.uv_h = self.height//2

        if self.BitDepth == 8:
            self.Yt = np.zeros(
                shape=(1, self.width, self.height), dtype='uint8', order='C')
            self.Ut = np.zeros(shape=(1, self.uv_w, self.uv_h),
                               dtype='uint8', order='C')
            self.Vt = np.zeros(shape=(1, self.uv_w, self.uv_h),
                               dtype='uint8', order='C')
        else:
            self.Yt = np.zeros(
                shape=(1, self.width, self.height), dtype='uint16', order='C')
            self.Ut = np.zeros(shape=(1, self.uv_w, self.uv_h),
                               dtype='uint16', order='C')
            self.Vt = np.zeros(shape=(1, self.uv_w, self.uv_h),
                               dtype='uint16', order='C')


class Field():
    width = 0
    height = 0
    MV_field = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def init_buff(self):
        self.MV_field = np.zeros(
            shape=(1, self.width, self.height), dtype='uint8', order='C')

# 读取YUV图像


def load_yuv(yuv_file, frame):
    # 读取Y分量
    if frame.BitDepth == 16:
        frame.Yt = np.frombuffer(yuv_file.read(frame.width * frame.height),
                                 dtype=np.uint16).reshape(frame.width, frame.height)
        frame.Ut = np.frombuffer(yuv_file.read(frame.uv_h*frame.uv_w),
                                 dtype=np.uint16).reshape(frame.uv_w, frame.uv_h)
        frame.Vt = np.frombuffer(yuv_file.read(frame.uv_h*frame.uv_w),
                                 dtype=np.uint16).reshape(frame.uv_w, frame.uv_h)
    else:
        frame.Yt = np.frombuffer(yuv_file.read(frame.width * frame.height),
                                 dtype=np.uint8).reshape(frame.width, frame.height)
        frame.Ut = np.frombuffer(yuv_file.read(frame.uv_h*frame.uv_w),
                                 dtype=np.uint8).reshape(frame.uv_w, frame.uv_h)
        frame.Vt = np.frombuffer(yuv_file.read(frame.uv_h*frame.uv_w),
                                 dtype=np.uint8).reshape(frame.uv_w, frame.uv_h)


def write_yuv(yuv_file, frame):
    yuv_file.write(bytes(frame.Yt.flatten()))
    yuv_file.write(bytes(frame.Ut.flatten()))
    yuv_file.write(bytes(frame.Vt.flatten()))
