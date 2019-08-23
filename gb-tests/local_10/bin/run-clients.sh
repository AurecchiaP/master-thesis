#!/bin/bash

CLIENTS=$1
INPUT=$2

echo $INPUT

tmux new-session -d -s clients
for ((i=0;i<CLIENTS;i++)); do
    tmux split -t clients
    tmux select-layout -t clients tiled
    tmux send-keys -t clients.$i "$INPUT" C-m
done