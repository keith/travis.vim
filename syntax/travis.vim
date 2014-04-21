if has('conceal')
  syntax region travisURL start=/|/ end=/|/ conceal
endif

syntax keyword travisSuccessStatus Passed
syntax keyword travisFailedStatus Failed
syntax keyword travisErroredStatus Errored
syntax keyword travisPendingStatus Started

highlight link travisURL Comment
highlight link travisSuccessStatus String
highlight link travisFailedStatus Error
highlight link travisErroredStatus Comment
highlight link travisPendingStatus Type

let b:current_syntax = 'travis'
