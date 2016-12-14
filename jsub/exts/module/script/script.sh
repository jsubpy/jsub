#!/bin/sh

current_dir=`pwd`

if [ -n "$JSUB_log_dir" ]; then
    logdir=$JSUB_log_dir
else
    logdir=$current_dir
fi

out="$logdir/script.out"
err="$logdir/script.err"

if [ "$JSUB_location" == 'common' ]; then
    script_path=${JSUB_input_common_dir}/${JSUB_script}
else
    script_path=${JSUB_input_dir}/${JSUB_script}
fi

# pass accepted arguments to the script
job_args=''
save_value=0
for arg in "$@"
do
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

# execution of script
(time eval \"$script_path\" $JSUB_argument $job_args) 1>"$out" 2>"$err"

# save the exit code
result=$?

sync
cat $out

if [ $result = 0 ]; then
    echo "JSUB_FINAL_EXECUTION_STATUS = Successful"
    exit 0
else
    echo "JSUB_FINAL_EXECUTION_STATUS = Failed ($result)"
    exit $result
fi
