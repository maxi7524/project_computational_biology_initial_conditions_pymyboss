# Create report documentation

## Download dependencies
To make this file render you need to download quarto, and dependencies:

```bash
# update apt-get
sudo apt-get update
# download quarto
sudo apt-get install ./quarto.deb -y

# install TinyTex
quarto install tool tinytex
# check version
quarto --version

# download css ieee.csl format:
wget https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl

```

## Render report
To render report run:
```shell
quarto render report.md --to pdf
```