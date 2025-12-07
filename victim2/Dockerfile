FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y openssh-server \
    && mkdir -p /var/run/sshd

# Create elf user with normal bash shell
RUN useradd -m -s /bin/bash elf \
    && echo "elf:movement" | chpasswd

# Remove sudo
RUN deluser elf sudo || true

# ---------------------------
# Restrict to ONLY ls and cat
# ---------------------------
RUN mkdir -p /home/elf/bin \
    && ln -s /bin/cat /home/elf/bin/cat \
    && ln -s /bin/ls /home/elf/bin/ls \
    && echo 'PATH=$HOME/bin' >> /home/elf/.profile \
    && echo 'export PATH=$HOME/bin' >> /home/elf/.bashrc \
    && echo 'enable -n cd' >> /home/elf/.bashrc \
    && echo 'unset HISTFILE' >> /home/elf/.bashrc \
    && echo 'HISTSIZE=0' >> /home/elf/.bashrc \
    && echo 'HISTFILESIZE=0' >> /home/elf/.bashrc \
    && chown -R elf:elf /home/elf

# Fix HOME permissions (SSH requires these)
RUN chmod 750 /home/elf

# Final flag (owned by user elf)
RUN echo "Congratz! The word is: snowman" > /home/elf/final_flag.txt \
    && chown elf:elf /home/elf/final_flag.txt

# SUID reveal binary
RUN printf '#!/bin/sh\ncp /home/elf/final_flag.txt /tmp/revealed_flag.txt\n' > /usr/local/bin/revealflag \
    && chmod 755 /usr/local/bin/revealflag \
    && chown root:root /usr/local/bin/revealflag \
    && chmod 4755 /usr/local/bin/revealflag

EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]