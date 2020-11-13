#!/bin/sh

# This action module allow user to execute code as bash script
# Attributes:
#	-code: code to run as a script

current_dir=$(pwd)

if [ -n "$JSUB_log_dir" ]; then
    logdir="$JSUB_log_dir"
else
    logdir="$current_dir"
fi

out="$logdir/exe.out"
err="$logdir/exe.err"

#get code
if [ -n "$JSUB_code_jobvar" ]; then
	eval JSUB_code='$JSUB_'$_JSUB_code_jobvar
fi

if [ -n "$JSUB_code" ]; then
	echo $JSUB_code > jsub_script.sh
	chmod +x jsub_script.sh
fi

(time eval \"./jsub_script.sh\") 1>"$out" 2>"$err"

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
