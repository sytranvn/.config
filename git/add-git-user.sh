if [[ "$1" = "" ]]; then
	echo $1
	echo "$(basename $0) <username> <email>"
	exit 1
fi

USERNAME=$1
EMAIL=$2

cat << EOF > ~/.config/git/${USERNAME}_config

[user]
	name = Other
	email = $EMAIL
	signingkey = ~/.ssh/$USERNAME

[url "git@github.com:"]
	insteadOf = git@github.com:

EOF

echo New config file created at "~/.config/git/${USERNAME}_config"
