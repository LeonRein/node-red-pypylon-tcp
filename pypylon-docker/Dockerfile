#Deriving the latest base image
FROM python:3.9-slim-bullseye

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install numpy
RUN python3 -m pip install pillow
RUN python3 -m pip install pylon
RUN python3 -m pip install pypylon

WORKDIR /usr/src/

COPY camera.py ./
COPY horse.png ./

EXPOSE 64746

CMD [ "python3", "-u", "camera.py"]