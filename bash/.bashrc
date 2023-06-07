export EDITOR=nvim
export GIT_PS1_SHOWDIRTYSTATE=true
export GIT_PS1_SHOWUNTRACKEDFILES=true
export GIT_PS1_SHOWUPSTREAM="auto"
os="$(uname -s)"

case $os in 
    Linux*)
	PS1='\[\033[0;32m\]\[\033[0m\033[0;32m\]\u\[\033[0;36m\]@\[\033[0;36m\]\h:\w\[\033[0;32m\]$(__git_ps1)\n\[\033[0;32m\]└─\[\033[0m\033[0;32m\]\$\[\033[0m\] ';;
    Darwin*)
	PATH="/opt/homebrew/bin:$PATH"
	PS1='\[\e[0;32m\]\[\e[0m\e[0;32m\]\u\[\e[0;36m\]@\[\e[0;36m\]\h:\w\[\e[0;32m\]$(__git_ps1)\n\[\e[0;32m\]└─\[\e[0m\e[0;32m\]\$\[\e[0m\] ';;
    *)
	PS1='\h:\w:\u \$ ';;
esac

export PATH="~/.config/bin:$PATH"
source ~/.config/bash/.aliases
source ~/.config/bash/.git-prompt.sh
