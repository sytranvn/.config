# Usage
```
cp ~/.config/git/.gitconfig ~/.gitconfig
```
# References

## git.includeIf
https://git-scm.com/docs/git-config

## Sign commit with ssh
https://github.com/settings/ssh/new
Add with Key type: Signing key

## Multiple accounts
```
Host github.com
  Hostname github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/default
Host github.com-otheruser
  Hostname github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/otheruser
```

Use with `includeIf`
```
[url "git@github.com-otheruser:"]
	insteadOf = git@github.com:
```
