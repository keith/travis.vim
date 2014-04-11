" Travis.vim - View Travis CI status in Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.0

if exists('g:loaded_travis') && g:loaded_travis
  finish
endif
let g:loaded_travis = 1
let s:plug = expand("<sfile>:p:h:h")

function! s:Travis()
  " echom "Foo"
  let script = s:plug . '/python/travis.py'
  execute 'pyfile ' . script
  redir => output
  silent! execute 'python main()'
  redir END
  redraw!

  " Remove null bytes
  let output = substitute(output, '\%x00', '', 'g')
  let bname = ('Travis')
  let winnr = bufwinnr('^' . bname . '$')
  " echom winnr
  if winnr < 0
    call CreateWindow()
  else
    " silent! execute winnr . 'wincmd w'
    " echom "Here"
    wincmd P
  endif
  redraw!
  silent! normal! ggdG
  " echom output
  call append(0, output)
  " silent put =output
endfunction

function! CreateWindow()
  " silent! execute 'botright new __Travis__'
  pedit Travis
  wincmd P
  " TODO: Set window size and fix it
  " TODO: setup text changing
  " setlocal noro modifiable
  setlocal buftype=nowrite bufhidden=wipe nobuflisted noswapfile nowrap nonumber
  nnoremap <buffer> <silent> q    :<C-U>bdelete<CR>
  nnoremap <buffer> r :Travis<CR>
  nnoremap <buffer> <CR> :call LineURL()<CR>
  " setlocal ro nomodifiable
endfunction

function! LineURL()
  let text = split(getline('.'), ' ')
  let url = text[1]
  let cmd = 'call system("open ' . url . '")'
  execute cmd
endfunction

command! Travis call s:Travis()
