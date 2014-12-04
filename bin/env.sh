if [ "x${BASH_ARGV[0]:-$0}" = "x" ]; then
    if [ ! -f bin/env.sh ]; then
        echo ERROR: must "cd where/root/is" before calling ". bin/env.sh" for this version of bash!
        JMSSYS=; export JMSSYS
        return
    fi
    JMSSYS="$PWD"; export JMSSYS
else
    # get param to "."
    THIS=$(dirname ${BASH_ARGV[0]:-$0})
    JMSSYS=$(cd ${THIS}/..;pwd); export JMSSYS
fi

if [ -z "${PATH}" ]; then
   PATH=$JMSSYS/bin; export PATH
else
   PATH=$JMSSYS/bin:$PATH; export PATH
fi

echo $JMSSYS
