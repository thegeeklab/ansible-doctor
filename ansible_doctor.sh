#!/usr/bin/env bash
set -euo pipefail

main() {
  parse_cmdline_ "$@"
  ansible_doctor_ "${ARGS[*]}" "${FILES[@]}"
}


parse_cmdline_() {
  declare argv
  argv=$(getopt -o a: --long args: -- "$@") || return
  eval "set -- $argv"

  for argv; do
    case $argv in
      -a | --args)
        shift
        ARGS+=("$1")
        shift
        ;;
      --)
        shift
        FILES=("$@")
        break
        ;;
    esac
  done
}

ansible_doctor_() {
  local -r args="$1"
  shift
  local -a -r files=("$@")

  local hack_ansible_doctor
  hack_ansible_doctor=$(ansible --version | sed -n 1p | cut -d ' ' -f 2) || true

  if [[ ! $(command -v ansible-doctor) ]]; then
    echo "ERROR: ansible-doctor is required by terraform_docs pre-commit hook but is not installed or in the system's PATH."
    exit 1
  fi

    ansible-doctor "$args" "${files[@]}"

}


# global arrays
declare -a ARGS=()
declare -a FILES=()

[[ ${BASH_SOURCE[0]} != "$0" ]] || main "$@"
