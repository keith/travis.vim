# Travis.vim

View your [Travis CI](https://travis-ci.org/) build status within Vim

## Usage

Run `:Travis` from within vim. You must be running vim from a folder
within the Git repository. Note: Travis.vim requires `+python`

Inside the Quickfix window:

`q`: closes the quickfix window

`r`: refreshes the build status

`<Enter>`: opens the build on [Travis](travis-ci.org)


With [vim-fugitive](https://github.com/tpope/vim-fugitive) installed:

`gt`: opens the source URL

`gl`: opens the last commit

### Example

![Example Build](https://raw.githubusercontent.com/Keithbsmiley/travis.vim/master/screenshot/travis.png)

###### License

MIT, see LICENSE
