FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y openssh-server sudo net-tools iputils-ping \
    && mkdir /var/run/sshd

# Create user 'victim' with password 'victimpass1'
RUN useradd -m -s /bin/bash victim \
    && echo "victim:dsjadjad828328738hdhadsahu" | chpasswd \
    && usermod -aG sudo victim

# Place victim1 flag and the password for victim2 (so player must jump from victim1 -> victim2)
RUN echo "CTF{flag_on_victim1}" > /home/victim/flag.txt
RUN echo "victim2 password: victimpass2" > /home/victim/notes.txt
RUN chown -R victim:victim /home/victim

# Allow password authentication
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config || true
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config || true

EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]