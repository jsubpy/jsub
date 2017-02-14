#!/bin/sh

logging() {
    echo "[`date '+%Y-%m-%d %H:%M:%S.%N %z %Z'`] $1" >> $log_file
}


cd $(dirname "$0")/..
main_root=$(pwd)

task_sub_id="$1"
job_root="$2"

navigator_root="${main_root}/navigator"
scenario_root="${main_root}/scenario"
action_root="${main_root}/action"
input_root="${main_root}/input"

log_root="${job_root}/log"
run_root="${job_root}/run"
output_root="${job_root}/output"

mkdir -p "$log_root"
mkdir -p "$run_root"
mkdir -p "$output_root"


log_file="${log_root}/bootstrap.log"

logging '================================================================================'
logging "Current directory: ${main_root}"


logging "Search for valid navigator..."
for navigator_dir in "${navigator_root}"/*
do
    navigator_exe=$(cat "${navigator_dir}/executable")
    navigator_ok=$(${navigator_dir}/${navigator_exe} --validate 2>>$log_file)
    if [ $? = 0 -a "$navigator_ok" = 'JSUB navigator OK' ]; then
        navigator="$navigator_dir"
        break
    fi
done

if [ -z "$navigator" ]; then
    logging 'ERROR: No available navigator found!'
    exit 1
fi

logging "Running the navigator: `basename ${navigator}`..."

"${navigator}/${navigator_exe}" "--task_sub_id=${task_sub_id}" \
    "--main_root=${main_root}" "--scenario_root=${scenario_root}" "--log_root=${log_root}" "--action_root=${action_root}" \
    "--run_root=${run_root}" "--input_root=${input_root}" "--output_root=${output_root}"
exit_code=$?

logging "Finished the navigator with exit code $exit_code"
exit $exit_code
