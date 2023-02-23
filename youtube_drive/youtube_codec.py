import numpy as np
from PIL import Image
import cv2

import base64
from Crypto.Cipher import AES
from . import config

ENABLE_ENCRYPTION = getattr(config, 'enable_encryption', False)
KEY = getattr(config, 'encryption_key', 'DefaultEncryptionKey').encode("ascii")[:16]


def quotient_remainder(divident, divsor):
    return divident // divsor, divident % divsor


def color_value(x):
    return x*255


def normal(x):
    return x/255


def encrypt_data_aes(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.urlsafe_b64encode(cipher.nonce + tag + ciphertext)


def decrypt_data_aes(data: bytes, key: bytes) -> bytes:
    raw = base64.urlsafe_b64decode(data)
    nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    clear_data = cipher.decrypt_and_verify(ciphertext, tag)
    return clear_data


def encode(infile_path, outvideo_path, fps=20, num_cols_per_frame=64, num_rows_per_frame=36, encrypt=ENABLE_ENCRYPTION, key=KEY):
    fd = open(infile_path, 'rb')
    raw_data_bytes = fd.read()
    if encrypt:
        raw_data_bytes = encrypt_data_aes(raw_data_bytes, key)
    data_bytes = np.frombuffer(raw_data_bytes, dtype=np.uint8)
    len_of_data = len(data_bytes)
    num_bytes_per_row = int(num_cols_per_frame * 3 / 8)
    num_bytes_per_frame = num_bytes_per_row * num_rows_per_frame

    len_bytes = np.array(bytearray(len_of_data.to_bytes(4, byteorder='big')), dtype=np.uint8)
    (num_frames, num_leftover_bytes) = quotient_remainder(4 + len_of_data, num_bytes_per_frame)

    if num_leftover_bytes > 0:
        num_bytes_last_frame_padding = num_bytes_per_frame - num_leftover_bytes
        padding_bytes = np.full((num_bytes_last_frame_padding), 0, dtype=np.uint8)
        data_bytes = np.concatenate((len_bytes, data_bytes, padding_bytes))
        num_frames += 1
    else:
        data_bytes = np.concatenate((len_bytes, data_bytes))

    # Vedio: size=(1280, 720), fps=20
    size = (num_cols_per_frame * 20, num_rows_per_frame * 20)

    video = cv2.VideoWriter(outvideo_path, cv2.VideoWriter_fourcc(
        *'mp4v'), fps, size)

    for i in range(num_frames):
        frame_bytes = data_bytes[i * num_bytes_per_frame: (i + 1) * num_bytes_per_frame]
        frame_bits = np.unpackbits(frame_bytes)
        # Reshape array to array(36， 72， 3)
        frame = color_value(frame_bits).reshape(num_rows_per_frame, num_cols_per_frame, 3)
        img = Image.fromarray(frame, mode="RGB")
        # Scale image to (1280, 720)
        newimg = img.resize(size, Image.Resampling.BOX)
        video.write(np.asarray(newimg))
    fd.close()


def decode(invideo_path, outfile_path, decrypt=ENABLE_ENCRYPTION, key=KEY):
    i = 0
    step = 20
    data_bits_list = []
    cap = cv2.VideoCapture(invideo_path)
    ret, frame = cap.read()
    while ret:
        frame_shape = np.shape(frame)
        for j in range(0, frame_shape[0], step):
            for k in range(0, frame_shape[1], step):
                piece = frame[j:j+step, k:k+step].reshape(step*step, 3)
                round = normal(piece.mean(0)).round().astype(np.uint8)
                data_bits_list.append(round)
        ret, frame = cap.read()
        i += 1
    cap.release()
    data_bits = np.array(data_bits_list).reshape(len(data_bits_list) * 3, 1)
    data_bytes = np.packbits(data_bits)
    len_of_data = int.from_bytes(data_bytes[:4], byteorder='big')
    data_bytes_retrieved = data_bytes[4:len_of_data+4].tobytes()
    if decrypt:
        data_bytes_retrieved = decrypt_data_aes(data_bytes_retrieved, key)
    fd = open(outfile_path, 'wb')
    fd.write(data_bytes_retrieved)
    fd.close()


if __name__ == '__main__':
    # encode("../examples/painting.jpg", "../examples/upload.mp4")
    # decode("../examples/upload.mp4", "../examples/painting-retrieved2.jpg")
    pass
