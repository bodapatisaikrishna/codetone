#!/bin/sh
alias ll='ls -l'
src=$1
dest=$2

function DoBackup {
    stamp=`date +%Y%m%d`
    name=$src-$stamp.tar.gz
    if [ $src == "" ]; then
        echo "no source given"
        exit 1
    fi
    cd $dest
    tar -czf $name $src
    count=$(expr $count + 1)
}

cleanup() {
    eval "rm -rf $dest/*.tmp"
    let total=total+1
}

for f in $*; do
    echo "arg: $f"
done

DoBackup
cleanup
echo "done"
