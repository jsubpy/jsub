#!/bin/sh

# This action module allow user to execute a script
# Attributes:
#	-exe: the name of the script to execute
#	-argument: can be a jobvar

current_dir=$(pwd)

if [ -n "$JSUB_log_dir" ]; then
    logdir="$JSUB_log_dir"
else
    logdir="$current_dir"
fi

out="$logdir/exe.out"
err="$logdir/exe.err"

if [ "$JSUB_location" == 'common' ]; then
    exe_path="${JSUB_input_common_dir}/${JSUB_exe}"
else
    exe_path="${JSUB_input_dir}/${JSUB_exe}"
fi


# pass accepted arguments to the exe
if [ -n "$JSUB_argumentJobvar" ]; then
	eval JSUB_argument='$JSUB_'$JSUB_argumentJobvar
fi
if [ -n "$JSUB_argument_jobvar" ]; then
	eval JSUB_argument='$JSUB_'$JSUB_argument_jobvar
fi

#execution
chmod +x $exe_path
(time eval \"$exe_path\" $JSUB_argument $job_args) 1>"$out" 2>"$err"

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
