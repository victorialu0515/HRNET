
ARG BASE_IMAGE=nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04

FROM $BASE_IMAGE AS marz_lipdub

# Install lightweight tools
RUN apt-get update -yqq && apt-get -y install wget git curl vim openssh-client apt-utils unzip

# Install Python
RUN apt-get install --yes --no-install-recommends build-essential \
    python3-setuptools\
    python3-pip
RUN python3 -m pip install --upgrade pip
# required for torch compile
RUN apt update && apt-get install libpython3-dev -y --fix-missing

# Install requirements
ADD ./docker/requirements.txt /
RUN pip install --user --upgrade pip && pip install --no-cache-dir --user -r /requirements.txt

RUN git clone https://github.com/ibaiGorordo/ONNX-HRNET-Human-Pose-Estimation.git --recursive && \
cd ONNX-HRNET-Human-Pose-Estimation && \
pip install -r requirements.txt

# Create working dir
RUN mkdir /hrnet
ENV WORKING_DIR=/hrnet

# Init startup script
COPY ./docker/startup.sh /usr/src/startup.sh
ENV STARTUP_SH=/usr/src/startup.sh
RUN echo ${STARTUP_SH}
RUN chmod +x $STARTUP_SH

CMD $STARTUP_SH
