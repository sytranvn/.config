# only use vi key binding for normal terminal
if [ -z "$NVIM" ] && [ -z "$VIM" ] && [ -z "$VI" ]; then
    set -o vi
fi

# remove previous duplicated lines or ignore lines starting with space
export HISTCONTROL=erasedups,ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
export HISTSIZE=-1
export HISTFILESIZE=-1

export EDITOR=nvim
export GIT_PS1_SHOWDIRTYSTATE=true
export GIT_PS1_SHOWUNTRACKEDFILES=true
export GIT_PS1_SHOWUPSTREAM="auto"

# MAILPATH="/var/mail/$USER?You have mail"
export MAILCHECK=30

os="$(uname -s)"
if [ "$os" = Darwin ];then
    macos=yes
fi

case $os in 
    Linux*)
	PS1='\[\033[0;32m\]\[\033[0m\033[0;32m\]\u\[\033[0;36m\]@\[\033[0;36m\]\h:\w\[\033[0;32m\]$(__git_ps1)\n\[\033[0;32m\]└─\[\033[0m\033[0;32m\]\$\[\033[0m\] ';;
    Darwin*)
	PS1='\[\e[0;32m\]\[\e[0m\e[0;32m\]\u\[\e[0;36m\]@\[\e[0;36m\]\h:\w\[\e[0;32m\]$(__git_ps1)\n\[\e[0;32m\]└─\[\e[0m\e[0;32m\]\$\[\e[0m\] ';;

    *)
	PS1='\h:\w:\u \$ ';;
esac

if [ "$macos" = yes ]; then
    . $HOME/.config/bash/.macrc
else
    . $HOME/.config/bash/.linuxrc
fi

if [ -d $HOME/go/bin ]; then
    export PATH="$PATH:$HOME/go/bin"
fi

export PATH="$HOME/.config/bin:$HOME/.local/bin:$PATH"
source ~/.config/bash/.aliases
source ~/.config/bash/.git-prompt.sh

for f in $(ls $HOME/.config/bash/aliases.d); do
    if [ -f $HOME/.config/bash/aliases.d/$f ]; then
	    source "$HOME/.config/bash/aliases.d/$f"
    fi
done
export GPG_TTY=$(tty)
# direnv hook
if which direnv >/dev/null; then
    eval "$(direnv hook bash)"
fi
# gcloud hook
[ -f ~/.gcrc ] && source ~/.gcrc

if [ -f "$HOME/.${USER}rc" ]; then
	source "$HOME/.${USER}rc"
fi

changes="$(myconf status -s)"
if [ ! -z "$changes" ]; then
	echo "You have changes in your config"
	myconf status -s
else
	echo "Your config is up to date"
fi

export JQ_COLORS="2;33:2;33:0;33:0;36:1;32:0;35:1;35:2;34"
