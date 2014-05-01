" File:         Travis.vim - View Travis CI status in Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.0

if exists('g:loaded_travis') && g:loaded_travis
  finish
endif
let g:loaded_travis = 1

" Don't yell unless the user tries to run the command without python
if !has('python')
  command! Travis :echohl ErrorMsg |
        \ echo "Travis.vim requires Vim compiled with +python" |
        \ echohl None<CR>
  finish
endif

command! Travis call travis#Travis()
