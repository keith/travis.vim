" Travis.vim - View Travis CI status in Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.0

if exists('g:loaded_travis') && g:loaded_travis
  finish
endif
let g:loaded_travis = 1
let s:plug = expand("<sfile>:p:h:h")

function! s:Travis()
  echom "Foo"
  let script = s:plug . '/python/travis.py'
  execute 'pyfile ' . script
  execute 'python main([None, None])'
endfunction

command! Travis call s:Travis()
