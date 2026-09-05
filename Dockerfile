FROM ubuntu:24.04
ARG D8_TARBALL_URL=https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/1681091/chrome-linux.zip
RUN apt-get update && apt-get install -y wget unzip libglib2.0-0 libnss3 libnspr4 libexpat1 libfontconfig1 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2
WORKDIR /opt
RUN if [ -n "$D8_TARBALL_URL" ]; then \
  wget --progress=dot:giga -O /tmp/d8_archive "$D8_TARBALL_URL" || exit 1; \
  mkdir -p /opt/d8 && \
  if unzip -t /tmp/d8_archive >/dev/null 2>&1; then \
    unzip -q /tmp/d8_archive -d /opt/d8; \
  else \
    tar -xf /tmp/d8_archive -C /opt/d8; \
  fi && \
  find /opt/d8 -type f -name d8 -perm -111 -exec ln -sf {} /usr/local/bin/d8 +; \
fi
RUN d8 --sandbox-testing --version || (echo "[-] d8 binary missing or sandbox-testing flag unsupported!" && exit 1)
WORKDIR /work
ENTRYPOINT ["d8", "--sandbox-testing"]
