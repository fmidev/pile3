# Main level Dockerfile for ubuntu18
# Markus Peura  fmi.fi

# Install environment & dependencies for rack

# FROM ubuntu:18.04
FROM ubuntu:jammy

RUN apt-get update && apt-get -y install pip

RUN pip install Pillow tifffile imagecodecs

COPY src/ /pile
ENV PYTHONPATH=

CMD ["python3","/pile/pile3.py", "--help"]