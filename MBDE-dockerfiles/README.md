
Notes taken while considering the below massive permutation space of potential
docker images supporting python.

https://hub.docker.com/_/python/tags

As per ...
https://forums.docker.com/t/differences-between-standard-docker-images-and-alpine-slim-versions/134973
... the following seems true:

```
Yes, there are some differences between these types of Docker images:

* Standard Docker Image: These images are typically based on a full Linux distribution like Ubuntu or Debian and include a wide range of pre-installed packages and dependencies. They tend to be larger in size than other types of images.

* Alpine Linux Docker Image: Alpine Linux is a lightweight Linux distribution that is designed to be small and secure. Alpine-based Docker images are typically much smaller than standard images, as they include only the bare essentials needed to run the application.

* Slim Docker Image: These images are similar to Alpine-based images in that they are designed to be small and efficient. However, they are not necessarily based on Alpine Linux and can use other lightweight Linux distributions like CentOS or Debian. Slim images typically include only the necessary packages and dependencies to run the application, but may still be larger than Alpine-based images.
```


