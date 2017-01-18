#!/bin/sh

if [ -n "$JSUB_log_dir" ]; then
    logdir="$JSUB_log_dir"
else
    logdir='.'
fi

out="$logdir/cmd.out"
err="$logdir/cmd.err"

# execution of command
cmd="$JSUB_cmd"
(time eval $cmd) 1>"$out" 2>"$err"

# save the exit code
result=$?

exit $result
