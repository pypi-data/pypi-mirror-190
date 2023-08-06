import numpy as np
from PIL import Image

from base import BaseCodec
from audio_obj import AudioObj
from img_obj import ImageObj


class HideWAVinJPG(BaseCodec):
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
        self.img = ImageObj()
        self.conv = AudioObj()

    def encode(
        self, carrier: Image.Image, payload: tuple[np.ndarray, int]
    ) -> tuple[Image.Image, int]:
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
    ) -> tuple[np.ndarray, int]:
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
