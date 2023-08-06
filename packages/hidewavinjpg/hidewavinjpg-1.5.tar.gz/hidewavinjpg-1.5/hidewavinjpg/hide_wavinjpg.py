import numpy as np
from PIL import Image


class AudioObj:
    def binary(self, i):
        bnr = bin(i).replace("0b", "")
        x = bnr[::-1]  # this reverses an array
        while len(x) < 8:
            x += "0"
        bnr = x[::-1]
        return bnr

    def openaudio(self, filename):
        with open(filename, "rb") as f:

            while f.readable():
                if f.read(1):
                    print(f.read(1))
                else:
                    break

    def wavtobits(self, file):
        data, samplerate = file

        if data.ndim == 1:
            nddata = np.transpose(data)
            nddata = nddata + 32768
            nddata = nddata / 256
            nddata = nddata.astype("uint8")
            binary_d = []
            for i in nddata:

                binary_d.append(self.binary(i))

            samplerate = int(samplerate / 256)
            b_str = "".join(binary_d)
            b_str = str(self.binary(samplerate)) + b_str
            print("The key is", len(b_str))
            return b_str, len(b_str)

        elif data.shape[1] == 2:
            data = data.flatten()
            nddata = np.transpose(data)
            nddata = nddata + 32768
            nddata = nddata / 256
            nddata = nddata.astype("uint8")
            binary_d = []
            for i in nddata:

                binary_d.append(self.binary(i))

            samplerate = int(samplerate / 256)
            b_str = "".join(binary_d)
            b_str = str(self.binary(samplerate)) + b_str
            test = b_str
            print("The key is", len(test))
            return b_str, len(test)

        else:
            raise ValueError("The File is unsupported.")

    def bitstowav(self, st, channel=1):

        if channel == 1:
            h_bits = [st[i : i + 8] for i in range(0, len(st), 8)]
            i = [int(j, 2) for j in h_bits]
            samplerate = i[0] * 256
            data = np.array(i[1:]) * 256
            data = data - 32768
            npdata = data.astype("int16")
            # sf.write("DecodedSamples/Decode.wav",npdata, samplerate)
            return npdata, samplerate

        elif channel == 2:
            h_bits = [st[i : i + 8] for i in range(0, len(st), 8)]
            i = [int(j, 2) for j in h_bits]

            samplerate = i[0] * 256
            data = np.array(i[1:]) * 256
            data = data - 32768
            data = data.astype("int16")
            data = data.reshape(data.shape[0] // 2, 2)
            # sf.write("DecodedSamples/Decode.wav",data, samplerate)
            return data, samplerate

        else:
            raise ValueError("The File is unsupported.")


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



class HideWAVinJPG():
    """This algorithm allows to conceal audio files inside png images, using a well
    known steganographic method: hide the data in the least significant bits of an image
    pixels. This produces little changes to the image that usually aren't noticed by
    just looking at the image.

    * Created by: QiuYu
    * Created time: 2022/10/17

    Originally implemented in
    [AmanKardam/Image-Steganography-Hiding-Audio-](https://github.com/AmanKardam/Image-Steganography-Hiding-Audio-)
    """

    def __init__(self) -> None:
        super().__init__()
        self.img =ImageObj()
        self.conv = AudioObj()

    def encode(self, carrier: Image.Image, payload):
        """Encoder requires carrier image to be JPG and payload to be a WAV audio.

        Args:
            carrier: Carrier image in format JPG. Read with 'stegobox.io.image.read()'.
            payload: Payload (secret message) to be encoded.Payload in format WAV. Read
                with `stegobox.io.soundfile.read()`.

        Returns:
            Encoded image in format JPG with the payload embeded.
        """
        bits_array, payload_len = self.conv.wavtobits(payload)
        imgout = self.img.encode(carrier, bits_array)
        return imgout, payload_len

    def decode(self, _):
        raise NotImplementedError("This codec does not support decoding without length")

    def decode_with_length(
        self, carrier: Image.Image, payload_len: int
    ):
        """Decode the secret payload from the carrier image.

        Args:
            carrier: Encoded carrier image.
            payload_len: The length of secret message

        Returns:
            The decoded payload (secret message).
        """
        wavdata = self.img.decode(carrier, payload_len)
        data, samplerate = self.conv.bitstowav(wavdata)
        return data, samplerate
