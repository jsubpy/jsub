#!/bin/sh

logging() {
    echo "[`date '+%Y-%m-%d %H:%M:%S.%N %z %Z'`] $1" >> $log_file
}


cd `dirname $0`
main_root=`pwd`

task_sub_id=$1
work_root=$2

director_root="${main_root}/director"
config_root="${main_root}/config"
module_root="${main_root}/module"
input_root="${main_root}/input"

log_root="${work_root}/log"
run_root="${work_root}/run"
output_root="${work_root}/output"

mkdir -p "$log_root"
mkdir -p "$run_root"
mkdir -p "$output_root"


log_file="${log_root}/bootstrap.log"
err_file="${log_root}/bootstrap.err"

logging '================================================================================'
logging "Current directory: ${main_root}"


# Check python version
python_version_major=`python -c "import sys;print(sys.version_info[0])"`
python_version_minor=`python -c "import sys;print(sys.version_info[1])"`
logging "Python version: ${python_version_major}.${python_version_minor}"


logging "Search for valid director..."
for director_dir in ${director_root}/*
do
    ${director_dir}/run --validate >/dev/null 2>&1
    if [ $? = 0 ]; then
        director=$director_dir
        break
    fi
done

if [ -z "$director" ]; then
    logging 'ERROR: No available director found!'
    exit 1
fi

logging "Running the director: `basename ${director}`..."

"${director}/run" "--task_sub_id=${task_sub_id}" \
    "--main_root=${main_root}" "--config_root=${config_root}" "--log_root=${log_root}" "--module_root=${module_root}" \
    "--run_root=${run_root}" "--input_root=${input_root}" "--output_root=${output_root}"
exit_code=$?

logging "Finished the director with exit code $exit_code"
exit $exit_code
