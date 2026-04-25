# ═══════════════════════════════════════════════════════════
#  components/zsh/shared/.zshrc — s4vitar style
# ═══════════════════════════════════════════════════════════

# Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting z sudo)
[[ -f "$ZSH/oh-my-zsh.sh" ]] && source "$ZSH/oh-my-zsh.sh"

# ── Alias ────────────────────────────────────────────────────
alias ll='ls -lah --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias cat='bat --style=plain' 2>/dev/null || alias cat='cat'
alias ls='lsd'               2>/dev/null || alias ls='ls --color=auto'

# ── Variables de entorno ─────────────────────────────────────
export EDITOR='nvim'
export VISUAL='nvim'
export BROWSER='firefox'
export TERM='xterm-256color'

# ── Historial ────────────────────────────────────────────────
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY

# ── PATH ─────────────────────────────────────────────────────
export PATH="$HOME/.local/bin:$PATH"
