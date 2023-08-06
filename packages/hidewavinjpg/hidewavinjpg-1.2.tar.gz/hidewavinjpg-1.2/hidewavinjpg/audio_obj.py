import numpy as np


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
