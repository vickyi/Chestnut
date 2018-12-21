#!/bin/bash
# A small example program for using the new getopt(1) program.
# This program will only work with bash(1)
# Note that we use `"$@"' to let each command-line parameter expand to a
# separate word. The quotes around `$@' are essential!
# We need ARGS as the `eval set --' would nuke the return value of getopt.

function usage(){
    echo "Usage: `basename $0` 参数说明："
    echo "-I|--instence,"
    echo ": 数据库实例"
    echo "-D|--database,"
    echo ": 数据库"
    echo "-T|--table,"
    echo ": 数据库表"
    echo "-e|--excute,"
    echo ": 待执行的 sql 脚本"
    echo "-k|--key,"
    echo ": 主键"
    echo ": --------------------examples：----------------------------"
    echo "eg1: sh getopt_sample.sh -database dw -table dim_date"
    echo "eg2: sh getopt_sample.sh -D dw -T dim_date"
}

if [ $# -lt 4 ]
then
    usage
    exit 55
fi

ARGS=`getopt -a -o I:D:T:e:k:LMSsth -l instence:,database:,table:,excute:,key:,list,master,slave,status,tableview,help -- "$@"`
[ $? -ne 0 ] && usage
#set -- "${ARGS}"
eval set -- "${ARGS}"
while true
do
        case "$1" in
        -I|--instence)
                instence="$2"
                echo $instence
                shift
                ;;
        -D|--database)
                database="$2"
                echo $database
                shift
                ;;
        -T|--table)
                table="$2"
                echo $table
                shift
                ;;
        -e|--excute)
                excute="yes"
                shift
                ;;
        -k|--key)
                key="$2"
                shift
                ;;
        -L|--list)
                LIST="yes"
                ;;
        -M|--master)
                MASTER="yes"
                ;;
        -S|--slave)
                SLAVE="yes"
                ;;
        -A|--alldb)
                ALLDB="yes"
                ;;
        -s|--status)
                STATUS="yes"
                ;;
        -t|--tableview)
                TABLEVIEW="yes"
                ;;
        -h|--help)
                usage
                ;;
        --)
                shift
                break
                ;;
        esac
shift
done