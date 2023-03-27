# Main level Dockerfile for ubuntu18
# Markus Peura  fmi.fi

# Install environment & dependencies for rack

# FROM ubuntu:18.04
FROM ubuntu:jammy

RUN apt-get update && apt-get -y install pip

RUN pip install Pillow tifffile imagecodecs

COPY src/ /pile/
RUN ln -s /pile/pile3.py /usr/local/bin

ENV PYTHONPATH=/pile
# CMD ["pile3.py", "--help"]
# CMD ["python3","-m pile3", "--help"]
CMD ["python3","/pile/pile3.py", "--help"]