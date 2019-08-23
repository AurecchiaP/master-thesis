#!/bin/bash

ID=$1
GROUP=$2

tmux new-session -d -s mcast
tmux split -t mcast
tmux select-layout -t mcast tiled
tmux send-keys -t mcast.1 " ./proposer-acceptor $ID paxos-2g3p-group$GROUP.conf &" C-m
tmux send-keys -t mcast.1 "./node-simple -n $ID -g $GROUP -c mcast-2g3p.conf -s famcast -p paxos-2g3p-group$GROUP.conf " C-m
