#!/bin/bash

# Get arguments
stream_src="$1"
manifest_dst="${2}"  # Use default value if manifest_dst is not provided
llmode="${3:-false}"  # Use default value "false" if llmode is not provided

python3 app.py config.ini mode=server stream_src="$stream_src" manifest_dst="$manifest_dst" low_latency="$llmode" &
APP_PID=$!
echo "app.py started with PID $APP_PID"
echo $APP_PID > /tmp/server_pid
wait $APP_PID