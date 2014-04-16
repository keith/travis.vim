" File:         Travis.vim - View Travis CI status in Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.0

if exists('g:loaded_travis') && g:loaded_travis
  finish
endif
let g:loaded_travis = 1
let s:travis_ran = 0
let s:plug = expand("<sfile>:p:h:h")

function! s:Travis()
  if !s:travis_ran
    let s:script = s:plug . '/python/travis.py'
    execute 'pyfile ' . s:script
    let s:travis_ran = 1
  endif

  redir => output
    silent! execute 'python main()'
  redir END
  " redraw!

  call s:ClearWindow()
  call s:PrintOutput(output)
endfunction

function! s:PrintOutput(output)
  " Remove null bytes
  let output = substitute(a:output, '\%x00', '', 'g')
  call append(0, output)
  silent! g/^$/d
  " silent! %s/\n^$\n//
  " silent put =output
endfunction

function! s:ClearWindow()
  let bname = ('Travis')
  let winnr = bufwinnr('^' . bname . '$')
  " echom winnr
  if winnr < 0
    call CreateWindow(bname)
  else
    " silent! execute winnr . 'wincmd w'
    " echom "Here"
    wincmd P
  endif
  " redraw!
  silent! normal! ggdG
endfunction

function! CreateWindow(name)
  execute 'pedit ' . a:name
  wincmd P
  " TODO: Set window size and fix it
  " TODO: setup text changing
  " setlocal noro modifiable
  setlocal buftype=nowrite bufhidden=wipe nobuflisted noswapfile nowrap nonumber
  nnoremap <buffer> <silent> q    :<C-U>bdelete<CR>
  nnoremap <buffer> r :Travis<CR>
  nnoremap <buffer> <CR> :call LineURL()<CR>
  nnoremap <buffer> s :call SourceURL()<CR>
  " setlocal ro nomodifiable
endfunction

function! SourceURL()
  " TODO: get url from git, make sure it's not ssh url
  echom "hi"
endfunction

function! LineURL()
  let text = split(getline('.'), ' ')
  let url = text[-1]
  echom url
  call OpenURL(url)
endfunction

function! OpenURL(url)
  " TODO: More executables
  let cmd = 'call system("open ' . a:url . '")'
  execute cmd
endfunction

command! Travis call s:Travis()
