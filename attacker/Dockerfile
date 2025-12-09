FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Install tools.
RUN apt-get update && apt-get install -y \
    openssh-server openssh-client \
    sudo net-tools iputils-ping nmap curl procps \
    && mkdir -p /var/run/sshd

# Create user 'ctf' with restricted shell (rbash)
RUN useradd -m -s /bin/rbash ctf \
    && echo "ctf:djuliscool" | chpasswd

# --- NMAP WRAPPER SCRIPT START ---
RUN echo '#!/bin/bash' > /opt/nmap_wrapper.sh \
    && echo 'MAX_SCANS=100' >> /opt/nmap_wrapper.sh \
    # ---------------------------------------------------- \
    # 1. CONCURRENCY CHECK \
    # ---------------------------------------------------- \
    && echo 'CURRENT_SCANS=$(/usr/bin/pgrep -x nmap | /usr/bin/wc -l)' >> /opt/nmap_wrapper.sh \
    && echo 'if [ "$CURRENT_SCANS" -ge "$MAX_SCANS" ]; then' >> /opt/nmap_wrapper.sh \
    && echo '  echo "SYSTEM LOAD HIGH: Too many people are scanning right now."' >> /opt/nmap_wrapper.sh \
    && echo '  echo "Please wait 10 seconds and try again."' >> /opt/nmap_wrapper.sh \
    && echo '  exit 1' >> /opt/nmap_wrapper.sh \
    && echo 'fi' >> /opt/nmap_wrapper.sh \
    && echo '' >> /opt/nmap_wrapper.sh \
    # ---------------------------------------------------- \
    # 2. MANUAL SYNTAX CHECKS \
    # ---------------------------------------------------- \
    && echo 'for arg in "$@"; do' >> /opt/nmap_wrapper.sh \
    && echo '  # CASE 1: Check for CIDR (e.g. /16)' >> /opt/nmap_wrapper.sh \
    && echo '  if [[ "$arg" =~ /([0-9]+)$ ]]; then' >> /opt/nmap_wrapper.sh \
    && echo '    PREFIX=${BASH_REMATCH[1]}' >> /opt/nmap_wrapper.sh \
    && echo '    if [ "$PREFIX" -lt 24 ]; then' >> /opt/nmap_wrapper.sh \
    && echo '      echo "RESTRICTION: CIDR /$PREFIX is too large. Max allowed is /24."' >> /opt/nmap_wrapper.sh \
    && echo '      exit 1' >> /opt/nmap_wrapper.sh \
    && echo '    fi' >> /opt/nmap_wrapper.sh \
    && echo '  fi' >> /opt/nmap_wrapper.sh \
    && echo '' >> /opt/nmap_wrapper.sh \
    && echo '  # CASE 2: Check for Ranges (e.g. 10.0.0.1-50)' >> /opt/nmap_wrapper.sh \
    && echo '  if [[ "$arg" == *"-"* && ! "$arg" =~ ^- ]]; then' >> /opt/nmap_wrapper.sh \
    && echo '      echo "RESTRICTION: Custom ranges (hyphens) are disabled to prevent abuse."' >> /opt/nmap_wrapper.sh \
    && echo '      echo "Please use standard CIDR notation (e.g., 192.168.1.0/24)."' >> /opt/nmap_wrapper.sh \
    && echo '      exit 1' >> /opt/nmap_wrapper.sh \
    && echo '  fi' >> /opt/nmap_wrapper.sh \
    && echo 'done' >> /opt/nmap_wrapper.sh \
    && echo '' >> /opt/nmap_wrapper.sh \
    # ---------------------------------------------------- \
    # 3. EXECUTE REAL SCAN \
    # ---------------------------------------------------- \
    && echo 'exec /usr/bin/nmap "$@"' >> /opt/nmap_wrapper.sh \
    && chmod 755 /opt/nmap_wrapper.sh \
    && chown root:root /opt/nmap_wrapper.sh

# --- NMAP WRAPPER SCRIPT END ---

# Create a whitelist command directory
RUN mkdir -p /home/ctf/bin

# Allowed commands (whitelisted)
RUN ln -s /opt/nmap_wrapper.sh /home/ctf/bin/nmap \
    && ln -s /usr/bin/curl /home/ctf/bin/curl \
    && ln -s /usr/bin/ssh /home/ctf/bin/ssh \
    && ln -s /bin/ls /home/ctf/bin/ls \
    && ln -s /bin/cat /home/ctf/bin/cat \
    && ln -s /bin/ping /home/ctf/bin/ping

# Configure .bash_profile to source .bashrc
RUN echo 'if [ -f ~/.bashrc ]; then . ~/.bashrc; fi' > /home/ctf/.bash_profile \
    && echo 'export PATH=$HOME/bin' >> /home/ctf/.bash_profile

# --- HISTORY CONFIGURATION (FIXED) ---
# 1. Point HISTFILE to /dev/null so it never writes to disk.
# 2. Set HISTSIZE to 1000 so "Arrow Up" works in RAM.
# 3. Disable 'kill' and 'enable' builtins.
RUN echo 'export HISTFILE=/dev/null' >> /home/ctf/.bashrc \
    && echo 'export HISTSIZE=1000' >> /home/ctf/.bashrc \
    && echo 'export HISTFILESIZE=0' >> /home/ctf/.bashrc \
    && echo 'enable -n kill' >> /home/ctf/.bashrc \
    && echo 'enable -n enable' >> /home/ctf/.bashrc

# Hardening: Physical Symlink to /dev/null
# This is a failsafe. Even if variables change, the file on disk is a black hole.
RUN ln -sf /dev/null /home/ctf/.bash_history

# Optional attacker flag
RUN echo "You have reached the initial terminal! Information gathering is key, what else can you find? \n Maybe this is interesting: 172.28.0.0/24" > /home/ctf/attacker.txt

# --- PERMISSION LOCKDOWN ---
# Lock Home
RUN chown -R root:ctf /home/ctf \
    && chmod -R 750 /home/ctf

# Lock Tmp
RUN chmod 1755 /tmp /var/tmp /dev/shm
# ---------------------------

# SSH Config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]