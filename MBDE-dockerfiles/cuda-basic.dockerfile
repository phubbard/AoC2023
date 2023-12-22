# Attempt simplest possible dockerfile

FROM nvidia/cuda:12.2.0-devel-ubuntu20.04

# Set the default command
CMD ["/bin/bash"]

WORKDIR /app

