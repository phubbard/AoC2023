# Attempt simplest possible dockerfile

FROM busybox:1.36.1-glibc

# Set the default command
CMD ["sh"]

WORKDIR /app

