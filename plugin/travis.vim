" File:         Travis.vim - View Travis CI status in Vim
" Maintainer:   Keith Smiley <http://keith.so>
" Version:      0.1.0

if exists('g:loaded_travis') && g:loaded_travis
  finish
endif
let g:loaded_travis = 1
let s:travis_ran = 0
let s:plug = expand("<sfile>:p:h:h")
let s:bname = 'Travis'

function! s:Travis()
  call s:Setup()
  call s:ClearWindow(s:bname)

  redir => output
    silent! execute 'python main()'
  redir END

  call s:SelectWindow(s:bname)
  call s:PrintOutput(output)
endfunction

function! s:Setup()
  if !s:travis_ran
    let s:script = s:plug . '/python/travis.py'
    execute 'pyfile ' . s:script
    let s:travis_ran = 1
  endif
endfunction

function! s:PrintOutput(output)
  let output = substitute(a:output, '\%x00', '', 'g') " Remove null bytes
  setlocal modifiable
  call append(0, output)
  silent! g/^$/d
  setlocal nomodifiable
endfunction

" Window setup ------ {{{
function! s:CreateWindow(name)
  silent execute 'pedit ' . a:name
  wincmd P

  call s:SetupWindow()
  call s:MapKeys()
endfunction

function! s:SetupWindow()
  setlocal buftype=nowrite bufhidden=wipe nobuflisted
  setlocal noswapfile nowrap nonumber nomodifiable
endfunction

function! s:MapKeys()
  nnoremap <buffer> <silent>   q  :<C-U>bdelete<CR>
  nnoremap <buffer>            r  :Travis<CR>
  nnoremap <buffer> <CR>          :call <SID>OpenLineURL()<CR>
  if exists(":Gbrowse") == 2
    nnoremap <buffer>          gt :call <SID>OpenSourceURL()<CR>
  endif
endfunction

function! s:ClearWindow(name)
  if bufwinnr('^' . a:name . '$') < 0
    return
  endif

  setlocal modifiable
  silent! normal! ggdG
  setlocal nomodifiable
  redraw!
endfunction

function! s:SelectWindow(name)
  if bufwinnr('^' . a:name . '$') < 0
    call s:CreateWindow(a:name)
  else
    wincmd P
  endif
endfunction
" }}}

" URL Opening functions ------ {{{
function! s:OpenLineURL()
  let text = split(getline('.'), '|')
  let url = text[-1]
  echom url
  call s:OpenURL(url)
endfunction

function! s:OpenSourceURL()
  if exists(":Gbrowse") == 2
    execute ':Gbrowse .'
  else
    " Could manually parse this stuff but only crazy
    " people aren't using fugitive anyways
    echom "Opening the source URL requires fugitive.vim"
  endif
endfunction

function! s:OpenURL(url)
  " TODO: More executables
  let executable = s:Executable()
  let cmd = 'call system("' . executable . ' ' . a:url . '")'
  execute cmd
endfunction
" }}}

" Get the executable tool based on the OS ------ {{{
function! s:Executable()
  if has("mac")
    if executable("open")
      return "open "
    elseif executable("/usr/bin/open")
      " Return full path if Vim's path isn't setup correctly
      return "/usr/bin/open "
    else
      echomsg "Missing `open` command"
      return ""
    endif
  elseif has("unix")
    if executable("xdg-open")
      return "xdg-open "
    elseif executable("gvfs-open")
      return "gvfs-open "
    elseif executable("gnome-open")
      return "gnome-open "
    endif
  elseif has("win32unix")
    return "cygstart "
  elseif has("win32")
    return "explorer "
  endif

  return ""
endfunction
" }}}

command! Travis call <SID>Travis()
