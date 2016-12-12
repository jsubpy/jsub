#!/bin/sh

logging() {
    echo "[`date '+%Y-%m-%d %H:%M:%S.%N %z %Z'`] $1" >> $log_file
}


cd `dirname $0`

job_root=`pwd`
runtime_root="${job_root}/runtime"
config_root="${job_root}/config"
log_root="${job_root}/log"
module_root="${job_root}/module"
work_root="${job_root}/work"
input_root="${job_root}/input"
output_root="${job_root}/output"

mkdir -p "$log_root"


log_file="${log_root}/bootstrap.log"
err_file="${log_root}/bootstrap.err"

logging '================================================================================'
logging "Current directory: ${job_root}"


# Check python version
python_version_major=`python -c "import sys;print(sys.version_info[0])"`
python_version_minor=`python -c "import sys;print(sys.version_info[1])"`
logging "Python version: ${python_version_major}.${python_version_minor}"


logging "Search for valid runtime..."
for runtime_dir in ${runtime_root}/*
do
    ${runtime_dir}/run --validate >/dev/null 2>&1
    if [ $? = 0 ]; then
        runtime=$runtime_dir
        break
    fi
done

if [ -z "$runtime" ]; then
    logging 'ERROR: No available runtime found!'
    exit 1
fi

logging "Using runtime: `basename ${runtime}`"

logging 'Running the main program...'

"${runtime}/run" "--job_root=${job_root}" "--config_root=${config_root}" "--log_root=${log_root}" "--module_root=${module_root}" \
    "--work_root=${work_root}" "--input_root=${input_root}" "--output_root=${output_root}"
exit_code=$?

logging "Finished the runtime program with exit code $exit_code"
exit $exit_code
