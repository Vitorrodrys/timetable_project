#!/bin/bash
set -eu pipefail


project_name="timetable"
env_file="test.env"

usage(){
    cat <<EOF
Usage: $0 [-p <project-name>]"
    -p The optional nome of the project. Default is 'timetable'.
EOF
}

if [[ $1 == "-h" || $1 == "--help" ]]; then
    usage
    exit 0
fi

while getopts ":p:e:" opt; do
  case $opt in
    p) project_name="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
        usage
        exit 1
    ;;
  esac
done

if [[ ! -f $env_file ]]; then
    echo "Error: Environment file '$env_file' not found."
    exit 1
fi
export $(grep -v '^#' test.env | xargs)
docker build -t api -f dockerfile ../
docker compose -f compose.yaml -p $project_name up -d
