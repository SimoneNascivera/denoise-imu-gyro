# To start this docker (you need CUDA installed in your host machine):
# docker build -t denoise-imu-gyro .
# docker run -it --rm --gpus all -v $(pwd):/home/docker/denoise-imu-gyro denoise-imu-gyro
FROM ubuntu:16.04

ARG USERNAME=docker
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

RUN sudo apt-get update && sudo apt-get install -y \
    vim \
    nano \
    tmux \
    git \
    python3 \
    python3-dev \
    python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/docker/denoise-imu-gyro
ADD ./requirements.txt /home/docker/denoise-imu-gyro/requirements.txt

WORKDIR /home/docker
RUN sudo python3 -m pip install --upgrade "pip < 19.2"
RUN sudo python3 -m pip install --upgrade pip

RUN sudo python3 -m pip install --pre torch  -f https://download.pytorch.org/whl/nightly/cu101/torch_nightly.html
RUN sudo python3 -m pip install -r denoise-imu-gyro/requirements.txt
