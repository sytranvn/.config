case "$TERM" in
    xterm-color|*-256color|xterm-kitty) color_prompt=yes;;
esac

export EDITOR=nvim

force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

export GIT_PS1_SHOWDIRTYSTATE=true
export GIT_PS1_SHOWUNTRACKEDFILES=true
export GIT_PS1_SHOWUPSTREAM="auto"
os="$(uname -s)"
case $os in 
    Linux*)
	PS1='${debian_chroot:+($debian_chroot)}\[\033[0;32m\]\[\033[0m\033[0;32m\]\u\[\033[0;36m\]@\[\033[0;36m\]\h:\w\[\033[0;32m\]$(__git_ps1)\n\[\033[0;32m\]└─\[\033[0m\033[0;32m\]\$\[\033[0m\] ';;
    Darwin*)
	PS1='change me \$ ';;
    *)
	PS1='\$ ';;
esac

export PATH="~/.config/bin:$PATH"
source ~/.config/bash/.aliases
