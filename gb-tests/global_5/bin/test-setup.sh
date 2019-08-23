#!/bin/bash

# USERNAME=someUser
HOSTS="node1 node2 node3 node4 node5 node6"
if [ "$1" == "run" ]; then

    SCRIPT="cd ~/local/bin; ./run-node.sh 0 0"
    REPLICAS=$2
    GROUPS=$3
    ssh -t ${HOSTNAME} "${SCRIPT}"
for ((i=1;i<=GROUPS;i++)); do
    echo $i
done
    for HOSTNAME in ${HOSTS} ; do
        ssh -t ${HOSTNAME} "cd ~/local/bin"
        for ((i=0;i<=GROUPS;i++)); do
            for ((j=0;j<=REPLICAS;j++)); do
            ssh -t ${HOSTNAME} "./run-node.sh $i $j"
        done
    done
if [ "$1" == "exit" ]; then
    SCRIPT="cd ~/local/bin; tmux kill-session -t mcast"
    for HOSTNAME in ${HOSTS} ; do
        ssh -t ${HOSTNAME} "${SCRIPT}"
    done