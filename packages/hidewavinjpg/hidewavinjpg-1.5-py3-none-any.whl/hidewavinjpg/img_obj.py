import numpy as np
from PIL import Image


class ImageObj:
    def binary(self, i):
        bnr = bin(i).replace("0b", "")
        x = bnr[::-1]  # this reverses an array
        while len(x) < 8:
            x += "0"
        bnr = x[::-1]
        return bnr

    def encode(self, file, b_str):

        # load the image
        image = file
        # convert image to numpy array
        data = np.asarray(image).copy()

        if len(b_str) < data.size:
            index = 0
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    for k in range(0, 3):
                        if index < len(b_str):
                            data[i][j][k] = int(
                                str(self.binary(data[i][j][k])[:7]) + b_str[index], 2
                            )
                            index += 1

            # data = data.astype("uint8")
            # print(dataout)
            dataout = Image.fromarray(data)
            return dataout
        else:
            raise ValueError("Audio File is too big.")

    def decode(self, file, leng):

        # load the image
        image = file
        # convert image to numpy array
        data1 = np.asarray(image)
        # summarize shape
        # print(data1.shape)

        imglist = []
        index = 0
        for i in range(data1.shape[0]):
            for j in range(data1.shape[1]):
                for k in range(0, 3):
                    if index < leng:
                        imglist.append(self.binary(data1[i][j][k])[-1])
                        index += 1

        return "".join(imglist)
