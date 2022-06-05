# Git
## Open Git Config
- git config --global -e
## Removing deleted branches:
- git removed-branches --prune
## Revert commit:
- git uncommit
## Changing pushed commit message:
- git commit --amend
- git push --force
## Tags:
### Make a tag:
- git tag {tag}
- git tag -a {tag} {commit} -e | -m "{message}"
### Remove a tag:
- git tag -d {tag_name}
### Push tags:
- git push --tags
- git push origin {tag}
# GPG
> GitHub GPG KEY: 5870C697FC29CC52
## List Keys 
- gpg --list-secret-keys --keyid-format=long
## Edit Key
- gpg --edit-key {KeyID}
- gpg> adduid
- gpg> quit





Test code performance with 4 models
- NDVI raw
Results: 7|0 100% < - the chosen
- NDVI gry
Results: 6|1
- NDVI col
Results: 7|0 100%
- NDVI edg
Results: 3|4 allnon <- wrong
