#!/bin/bash

CLIENTS=$1

for ((i=0;i<CLIENTS;i++)); do
    tmux send-keys -t clients.$i C-c C-m
done