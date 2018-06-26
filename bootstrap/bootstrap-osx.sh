#!/bin/bash
set -euo pipefail

# This script needs to be standalone to be run like this:
# bash <(curl -fsSL https://raw.githubusercontent.com/request-yo-racks/api/master/bootstrap/bootstrap-osx.sh)
# Therefore cannot import other scripts.

echo "# If the script fails, run the following command and re-try: "
echo "#    export RYR_BS_SILENT=0"

: ${RYR_BS_SILENT:=1}
if [ "${RYR_BS_SILENT}" -eq "1" ]; then
  exec &>/dev/null
fi

# Install brew if needed.
brew --version || /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Update brew.
brew update

# Install brew formulas.
brew install \
  brew-cask-completion \
  bash-completion \
  docker-completion \
  editorconfig \
  pip-completion \
  python 3 \
  shellcheck

# Install cask formulas.
brew cask install \
  docker \
  virtualbox \
  virtualbox-extension-pack
