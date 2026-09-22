#!/usr/bin/env bash 
set -euo pipefail

touch ${HOME:-/root}/.bash_history

# Note: `bsdmainutils` contains `colrm`
apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    bsdmainutils \
    hstr \
    \
    direnv \
    \
    fd-find \
    sd \
    bat \
    ripgrep \
    fzf \
    && rm -rf /var/lib/apt/lists/*

cat > "${HOME:-/root}/.bashrc" <<- 'EOM'
# ensure synchronization between bash memory and history file
export PROMPT_COMMAND="history -a; history -n; export HISTFILE=${HOME:-/root}/.bash_history"

shopt -s histappend # history list is appended to the file named by the value of the HISTFILE variable when the shell exits, rather than overwriting the file
shopt -s cmdhist # Saves multi-line commands in the history as a single entry, instead of splitting them into multiple lines.
shopt -s checkwinsize # checks the window size after each external (non-builtin) command and, if necessary, updates the values of LINES and COLUMNS
shopt -s globstar # Enables the ** globbing operator
shopt -s checkjobs # Check if background jobs have completed before exiting the shell
shopt -s nullglob # When a pattern like *.txt doesn’t match any files, it expands to an empty list instead of the literal string *.txt
shopt -s dotglob # Globbing matches dotfiles (hidden files), no need for 'mv * .* <>' just 'mv * <>'
shopt -s globstar # Enable ** to match directories recursively
shopt -s extglob # Enables extended pattern matching features in globbing
shopt -s nocaseglob # Makes globing is case insenstive
shopt -s nocasematch  # Enable case-insensitive matching, e.g. `[[ $filename == *.pdf ]]` also matches `.PDF`
shopt -s expand_aliases # Allow aliases in non-interactive (scripts)
# shopt -s sourcepath # Allow searching PATH for `source ...` when a script cannot be found

jj_or_git() {
    local name=""

    # 1. Check if jj is installed AND if we are inside a jj root
    if command -v jj >/dev/null 2>&1 && jj root >/dev/null 2>&1; then
        name=$(jj log -r @ --no-graph --template '
            coalesce(
                self.local_bookmarks().map(|b| b.name()).join("\n"),
                self.change_id().shortest().prefix()
            )
        ' 2>/dev/null | head -n1)
        
        # Use \001 (start non-printing) and \002 (end non-printing) for prompt colors
        printf " \001\033[35m\002(%s)\001\033[00m\002" "$name"
        return
    fi

    # 2. Fallback: Check if git is installed AND inside a git work tree
    if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        # Modern way to get branch name (cleaner than colrm)
        name=$(git branch --show-current 2>/dev/null)
        
        # If detached head (no branch name), get the short hash
        if [ -z "$name" ]; then
            name=$(git rev-parse --short HEAD 2>/dev/null)
        fi

        printf " \001\033[32m\002(%s)\001\033[00m\002" "$name"
        return
    fi
}

# Prompt (e.g. "user@📦:directory (branch)$ ")
export PS1="\[\033[36m\]\u@\[📦\]\[\033[00m\]:\[\033[33m\]\w\[\033[32m\]\$(jj_or_git)\[\033[00m\]\$ "

### For hstr
alias hh=hstr                    # hh to be alias for hstr
export HSTR_CONFIG=hicolor       # get more colors
export HISTCONTROL=ignorespace   # leading space hides commands from history
export HISTFILESIZE=10000        # increase history file size (default is 500)
export HISTSIZE=${HISTFILESIZE}  # increase history size (default is 500)
# if this is interactive shell, then bind hstr to Ctrl-r (for Vi mode check doc)
if [[ $- =~ .*i.* ]]; then bind '"\C-r": "\C-a hstr -- \C-j"'; fi
# if this is interactive shell, then bind 'kill last command' to Ctrl-x k
if [[ $- =~ .*i.* ]]; then bind '"\C-xk": "\C-a hstr -k \C-j"'; fi
export HSTR_TIOCSTI=y

alias l='ls -lah'
alias fd=fdfind

eval "$(direnv hook bash)"
EOM
