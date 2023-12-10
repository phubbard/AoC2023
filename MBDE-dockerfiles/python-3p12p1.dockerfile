# Attempt simplest possible dockerfile

# As per README.md notes, there are three options; picking smallest

FROM python:3.13-rc-alpine
# FROM python:3.12.1-slim-bookworm
# FROM python:3.12.1-bookworm

# Set the default command (/bin/sh for ALPINE, /bin/bash for ubuntu)
CMD ["/bin/sh"]

WORKDIR /app


