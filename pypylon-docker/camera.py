import socket
import pypylon.pylon as py
import os
from io import BytesIO
from PIL import Image

HOST = "python" # this docker alias from docker-compose
PORT = 64746

# init camera

os.environ["PYLON_CAMEMU"] = "1"
cam = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
cam.Open()
cam.ImageFilename = "horse.png"
cam.ImageFileMode = "On" # enable image file test pattern
cam.TestImageSelector = "Off" # disable testpattern [ image file is "real-image"]
cam.PixelFormat = "RGB8Packed"
cam.AcquisitionFrameRateAbs = 60
cam.StartGrabbing()

# init socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print(s)

while cam.IsGrabbing():
    conn, addr = s.accept()
    print(f"(new connection from {addr[0]} port {addr[1]}")
    try:
        while cam.IsGrabbing():
            res = cam.RetrieveResult(1000)
            pil_img = Image.fromarray(res.Array)
            res.Release()
            buff = BytesIO()
            pil_img.save(buff, format="JPEG")
            conn.sendall(buff.getvalue())
        conn.close()
    except socket.timeout:
        pass
    except BrokenPipeError:
        # client stoped recieving during transmission
        pass
