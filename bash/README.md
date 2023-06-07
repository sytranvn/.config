# Setup for Mac M1
## Script
Run `install-bash-macos` script.
## Setup manual
Install bash new version

```shell
brew install bash
```

Add bash path into list of shells

```shell
echo /opt/homebrew/bin/bash | sudo tee -a /etc/shells
```
Change default user shell

```shell
chsh -s /opt/homebrew/bin/bash
```

Create default bash profile for Mac
```shell 
echo '[ -f ~/.config/bash/.bashrc ] && . ~/.config/bash/.bashrc' | tee -a ~/.profile
```

Quit all terminals and reopen. Check result.

```shell
echo $BASH_VERSION
```

