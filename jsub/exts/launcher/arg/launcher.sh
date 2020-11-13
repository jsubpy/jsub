#!/bin/sh

if [ $# != 1 ]; then
    echo 'Need 1 argument!'
    exit 1
fi


task_sub_id="$1"

cd $(dirname "$0")
work_root=$(pwd)

job_root="${work_root}/subjobs/${task_sub_id}"

mkdir -p "${job_root}"
cd "${job_root}"

runtime_log_root="${job_root}/log"
mkdir -p "${runtime_log_root}"
launcher_log="${runtime_log_root}/launcher.log"

bootstrap_exe=$(cat "${work_root}/main/bootstrap/executable")

"${work_root}/main/bootstrap/${bootstrap_exe}" "${task_sub_id}" "${job_root}" > "${launcher_log}" 2>&1

exit_code=$?
exit $exit_code
