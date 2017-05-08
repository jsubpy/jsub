#!/bin/sh

for arg in "$@"
do
    case $arg in
        -a|--)
    if [ "$save_value" == 1 ]; then
        job_args="${job_args} \"$arg\""
        save_value=0
        continue
    fi

    for accepted_arg in $JSUB_accepted_args
    do
        if [ "--$accepted_arg" == "$arg" ]; then
            job_args="${job_args} \"$arg\""
            save_value=1
            break
        fi
    done
done

cd $(dirname "$0")
work_root=$(pwd)

tar xzf jsub_main.tar.gz

task_sub_id=$(get_sub_id "$sub_id_args")

if [ $# != 1 ]; then
    echo 'Need 1 arguments!'
    exit 1
fi

task_sub_id="$1"

cd $(dirname "$0")
work_root=$(pwd)

job_root="${work_root}/job/${task_sub_id}"

mkdir -p "${job_root}"
cd "${job_root}"

log_root="${job_root}/log"
mkdir -p "${log_root}"
launcher_log="${log_root}/launcher.log"

bootstrap_exe=$(cat "${work_root}/main/bootstrap/executable")

"${work_root}/main/bootstrap/${bootstrap_exe}" "${task_sub_id}" "${job_root}" > "${launcher_log}" 2>&1
