#!/bin/bash

# Function to terminate the app.py process
force_terminate() {
    if [ -f /tmp/gateway_pid ]; then
        APP_PID=$(cat /tmp/gateway_pid)
        echo "terminating gateway with PID $APP_PID"
        kill -SIGKILL $APP_PID
        rm -f /tmp/gateway_pid
    else
        echo "No app.py process found."
    fi
}

# Run the app.py script in the background and capture its PID
python3 app.py config.ini mode=gateway sutc=true &
APP_PID=$!
echo $APP_PID > /tmp/gateway_pid

# Loop to keep the script running and allow user to quit
while true; do
    read -p "Press Q to quit: " input
    if [[ $input == "Q" || $input == "q" ]]; then
        force_terminate
        exit 0
    fi
done
