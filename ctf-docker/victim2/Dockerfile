FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y openssh-server \
    && mkdir -p /var/run/sshd

# Create victim2 user with normal bash shell
RUN useradd -m -s /bin/bash victim2 \
    && echo "victim2:movement" | chpasswd

# Remove sudo
RUN deluser victim2 sudo || true

# ---------------------------
# Restrict to ONLY ls and cat
# ---------------------------
RUN mkdir -p /home/victim2/bin \
    && ln -s /bin/cat /home/victim2/bin/cat \
    && ln -s /bin/ls /home/victim2/bin/ls \
    && echo 'PATH=$HOME/bin' >> /home/victim2/.profile \
    && echo 'export PATH=$HOME/bin' >> /home/victim2/.bashrc \
    && echo 'enable -n cd' >> /home/victim2/.bashrc \
    && echo 'unset HISTFILE' >> /home/victim2/.bashrc \
    && echo 'HISTSIZE=0' >> /home/victim2/.bashrc \
    && echo 'HISTFILESIZE=0' >> /home/victim2/.bashrc \
    && chown -R victim2:victim2 /home/victim2

# Fix HOME permissions (SSH requires these)
RUN chmod 750 /home/victim2

# Final flag
RUN echo "Congratz! The word is: snowman" > /root/final_flag.txt

# SUID reveal binary
RUN printf '#!/bin/sh\ncp /root/final_flag.txt /tmp/revealed_flag.txt\n' > /usr/local/bin/revealflag \
    && chmod 755 /usr/local/bin/revealflag \
    && chown root:root /usr/local/bin/revealflag \
    && chmod 4755 /usr/local/bin/revealflag

# SSH settings
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]