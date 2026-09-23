```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mcmah309/containeryard/master/src/schemas/yard-module-schema.json

description: "Google chrome browser and driver (useful for headless testing)"
requires:
    - ./wget.md
    - ./gpg.md
    - ./unzip.md
```
```Dockerfile
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && CHROME_VERSION="$(google-chrome --product-version)" \
    && CHROME_BUILD="${CHROME_VERSION%.*}" \
    && CHROMEDRIVER_VERSION="$(wget -q -O - "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_BUILD}")" \
    && wget -q -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip /tmp/chromedriver.zip -d /tmp/chromedriver \
    && install -m 0755 /tmp/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver /tmp/chromedriver.zip \
    && rm -rf /var/lib/apt/lists/*
```
