# Main level Dockerfile for ubuntu18
# Markus Peura  fmi.fi

# Install environment & dependencies for rack

FROM ubuntu:18.04 

#RUN apt-get update && apt-get -y install pip3
RUN pip3 install tifffile
RUN pip3 install imagecodecs
