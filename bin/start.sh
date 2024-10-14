#!/usr/bin/env bash
set -e

function print_help() {
    echo "  --help                  Print help message"
    echo "  --log-level             Set log level. Avaliable values: debug, info, exception, critical"
    echo "  --mode                  App environment. Avaliable values: devel or bench_devel"
    echo "  --is-mac                Local computer using macOS. User directory in /Users/"
}

BOLD_RED='\033[1;91m'
NO_COLOR='\033[0m'

IS_MAC=0

export LOG_LEVEL="DEBUG"
export APPLICATION_ENV="LOCAL"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --is-mac)
        IS_MAC=1;;
    --log-level)
      if [[ -n "$2" ]]; then
        case "$2" in
            debug | DEBUG)
                export LOG_LEVEL="DEBUG";;
            info | INFO)
                export LOG_LEVEL="INFO";;
            exception | EXCEPTION | error | ERROR)
                export LOG_LEVEL="EXCEPTION";;
            critical | CRITICAL)
                export LOG_LEVEL="CRITICAL";;
            *)
                echo -e "${BOLD_RED}Error: Invalid log level. Use: debug, info, exception or critical.${NO_COLOR}"
                exit 1;;
        esac
        shift
      else
        echo -e "${BOLD_RED}Error: --log-level requires a value.${NO_COLOR}"
        exit 1
      fi
      ;;
    -m | --mode)
      if [[ -n "$2" ]]; then
        case "$2" in
            local | LOCAL)
                export APPLICATION_ENV="LOCAL";;
            remote | REMOTE)
                export APPLICATION_ENV="REMOTE";;
            *)
                echo -e "${BOLD_RED}Error: Invalid APPLICATION_ENV. Use: local or remote.${NO_COLOR}"
                exit 1;;
        esac
        shift
      else
        echo -e "${BOLD_RED}Error: --mode requires a value.${NO_COLOR}"
        exit 1
      fi
      ;;
    -h | --help)
        print_help
        exit 0
        ;;
    *)
      echo -e "${BOLD_RED}Unknown option: $1${NO_COLOR}"
      print_help
      exit 1
      ;;
  esac
  shift
done

if [[ -z "${PROJECT_ROOT}" ]]
then
    if [[ $IS_MAC == 1 ]]
    then
        export PROJECT_ROOT=/home/$(whoami)/LinalEducation
    else
        export PROJECT_ROOT=/Users/$(whoami)/LinalEducation
    fi
fi

export PYTHONPATH=$PROJECT_ROOT
echo "projet in ${PYTHONPATH}"

mkdir -p /tmp/run
source $PYTHONPATH/venv/bin/activate
python3 $PYTHONPATH/bin/__main__.py --config-dir "${PROJECT_ROOT}/configs/environment" --mode "${APPLICATION_ENV}"
deactivate
