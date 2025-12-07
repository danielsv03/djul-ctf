FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Install only tools needed for CTF
RUN apt-get update && apt-get install -y \
    openssh-server openssh-client \
    sudo net-tools iputils-ping nmap curl \
    && mkdir -p /var/run/sshd

# Create user 'ctf' with restricted shell (rbash)
RUN useradd -m -s /bin/rbash ctf \
    && echo "ctf:djuliscool" | chpasswd

# Create a whitelist command directory
RUN mkdir -p /home/ctf/bin

# Allowed commands (whitelisted)
RUN ln -s /usr/bin/nmap /home/ctf/bin/nmap \
    && ln -s /usr/bin/curl /home/ctf/bin/curl \
    && ln -s /usr/bin/ssh /home/ctf/bin/ssh \
    && ln -s /bin/ls /home/ctf/bin/ls \
    && ln -s /bin/cat /home/ctf/bin/cat \
    && ln -s /bin/ping /home/ctf/bin/ping

# Set PATH so user can *only* run allowed commands
RUN echo 'export PATH=$HOME/bin' >> /home/ctf/.bash_profile

# Disable bash history
RUN echo 'unset HISTFILE' >> /home/ctf/.bashrc \
    && echo 'export HISTSIZE=0' >> /home/ctf/.bashrc \
    && echo 'export HISTFILESIZE=0' >> /home/ctf/.bashrc \
    && chown ctf:ctf /home/ctf/.bashrc

# Optional attacker flag
RUN echo "You have reached the initial terminal! Information gathering is key, what else can you find?" > /home/ctf/attacker.txt \
    && chown ctf:ctf /home/ctf/attacker.txt

# Disallow root login
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]