#!/bin/bash

name="amcast"

PREFIX=""
SUFFIX=""

for var in "$@"; do 
  if [ "$var" = "-d" ]; then
    PREFIX="valgrind "
  elif [ "$var" = "-v" ]; then
    SUFFIX=" -v > /tmp/log\${RANDOM}.txt"
  else 
    name="$var"
  fi
done

echo "Running $name..."
sleep 2

tmux new-session -d -s mcast
#tmux new-window -t mcast
tmux split -t mcast
tmux split -t mcast
tmux split -t mcast
tmux select-layout -t mcast even-vertical

if [ "$name" != "mcast" ]; then
  tmux send-keys -t mcast.1 " ./proposer-acceptor 0 paxos-1g3p-group0.conf > /tmp/px00.log &" C-m
  tmux send-keys -t mcast.2 " ./proposer-acceptor 1 paxos-1g3p-group0.conf > /tmp/px01.log &" C-m
  tmux send-keys -t mcast.3 " ./proposer-acceptor 2 paxos-1g3p-group0.conf > /tmp/px02.log &" C-m

  tmux send-keys -t mcast.1 "$PREFIX ./node-simple -n 0 -g 0 -c mcast-1g3p.conf -s $name -p paxos-1g3p-group0.conf $SUFFIX" C-m
  tmux send-keys -t mcast.2 "$PREFIX ./node-simple -n 1 -g 0 -c mcast-1g3p.conf -s $name -p paxos-1g3p-group0.conf $SUFFIX" C-m
  tmux send-keys -t mcast.3 "$PREFIX ./node-simple -n 2 -g 0 -c mcast-1g3p.conf -s $name -p paxos-1g3p-group0.conf $SUFFIX" C-m
else
  tmux send-keys -t mcast.1 "$PREFIX ./node-simple -n 0 -g 0 -c mcast-1g3p.conf $SUFFIX" C-m
  tmux send-keys -t mcast.2 "$PREFIX ./node-simple -n 1 -g 0 -c mcast-1g3p.conf $SUFFIX" C-m
  tmux send-keys -t mcast.3 "$PREFIX ./node-simple -n 2 -g 0 -c mcast-1g3p.conf $SUFFIX" C-m
fi

tmux attach-session -t mcast
