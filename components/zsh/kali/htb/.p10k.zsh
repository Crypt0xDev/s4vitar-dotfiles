# Powerlevel10k — Tema HTB (verde #9FEF00)
# Para instalar p10k: git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
# Agrega a .zshrc: source ~/powerlevel10k/powerlevel10k.zsh-theme

# Instant prompt (debe estar al inicio del .zshrc)
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Elementos del prompt
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  os_icon
  dir
  vcs
  newline
  prompt_char
)

typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
  status
  command_execution_time
  background_jobs
  direnv
  virtualenv
  context
  time
)

# Colores principales HTB
typeset -g POWERLEVEL9K_DIR_FOREGROUND=0
typeset -g POWERLEVEL9K_DIR_BACKGROUND=2  # verde HTB

typeset -g POWERLEVEL9K_PROMPT_CHAR_OK_{VIINS,VICMD,VIVIS,VIOWR}_FOREGROUND=2
typeset -g POWERLEVEL9K_PROMPT_CHAR_ERROR_{VIINS,VICMD,VIVIS,VIOWR}_FOREGROUND=1

# Git
typeset -g POWERLEVEL9K_VCS_CLEAN_FOREGROUND=0
typeset -g POWERLEVEL9K_VCS_CLEAN_BACKGROUND=2
typeset -g POWERLEVEL9K_VCS_MODIFIED_FOREGROUND=0
typeset -g POWERLEVEL9K_VCS_MODIFIED_BACKGROUND=3
typeset -g POWERLEVEL9K_VCS_UNTRACKED_FOREGROUND=0
typeset -g POWERLEVEL9K_VCS_UNTRACKED_BACKGROUND=3

# Estilo
typeset -g POWERLEVEL9K_MODE='nerdfont-complete'
typeset -g POWERLEVEL9K_ICON_PADDING=moderate
typeset -g POWERLEVEL9K_BACKGROUND=236
typeset -g POWERLEVEL9K_LEFT_SUBSEGMENT_SEPARATOR='%244F\uE0B1'
typeset -g POWERLEVEL9K_RIGHT_SUBSEGMENT_SEPARATOR='%244F\uE0B3'
typeset -g POWERLEVEL9K_LEFT_SEGMENT_SEPARATOR='\uE0B0'
typeset -g POWERLEVEL9K_RIGHT_SEGMENT_SEPARATOR='\uE0B2'
typeset -g POWERLEVEL9K_LEFT_PROMPT_LAST_SEGMENT_END_SYMBOL='\uE0B0'
typeset -g POWERLEVEL9K_RIGHT_PROMPT_FIRST_SEGMENT_START_SYMBOL='\uE0B2'

# Time
typeset -g POWERLEVEL9K_TIME_FOREGROUND=0
typeset -g POWERLEVEL9K_TIME_BACKGROUND=2
typeset -g POWERLEVEL9K_TIME_FORMAT='%D{%H:%M}'

# Transient prompt (limpia líneas anteriores)
typeset -g POWERLEVEL9K_TRANSIENT_PROMPT=always
typeset -g POWERLEVEL9K_INSTANT_PROMPT=verbose
