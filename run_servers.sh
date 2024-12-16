#!/bin/bash

# Define the list of stream sources
stream_sources=(
    "https://livesim2.dashif.org/livesim2/testpic_2s/Manifest.mpd"
    "https://livesim2.dashif.org/livesim2/mup_30/testpic_2s/Manifest.mpd"
    "" # "https://livesim2.dashif.org/livesim2/segtimeline_1/testpic_2s/Manifest.mpd"
    "https://livesim2.dashif.org/livesim2/periods_60/continuous_1/testpic_2s/Manifest.mpd"
    "https://akamaibroadcasteruseast.akamaized.net/cmaf/live/657078/akasource/out.mpd"
    "https://cmafref.akamaized.net/cmaf/live-ull/2006350/akambr/out.mpd"
)

# Function to launch server
launch_server() {
    local src="$1"
    local dst="$2"
    local llmode="${3:-false}"  # Default to false if not provided
    ./scripts/launch_server.sh "$src" "$dst" "$llmode" &
    LAUNCH_SERVER_PID=$!
    echo "launch_server.sh started with PID $LAUNCH_SERVER_PID"
    echo $LAUNCH_SERVER_PID > /tmp/server_pid
}

# Function to forcefully terminate the app.py process
force_terminate() {
    if [ -f /tmp/server_pid ]; then
        APP_PID=$(cat /tmp/server_pid)
        echo "Forcefully terminating app.py with PID $APP_PID"
        kill -SIGKILL $APP_PID
        rm -f /tmp/server_pid
    else
        echo "No app.py process found."
    fi
}

sigint_handler() {
    echo "SIGINT caught - forcing termination ..."
    force_terminate
    exit 1
}

trap 'sigint_handler' SIGINT

# Ask user for choice
echo "Choose a stream source:"
echo "A: Live segment template without manifest updates"
echo "B: Live segment template with manifest updates every 30s"
echo "C: Live segment timeline with manifest updates every 30s"
echo "D: Multi-period, 1 period per minute"
echo "E: low-latency single rate"
echo "F: low-latency multi rate"
echo "Q: Quit and terminate server"

read -r choice

# Launch server based on user choice
case "$choice" in
    A)
        launch_server "${stream_sources[0]}"
        ;;
    B)
        launch_server "${stream_sources[1]}"
        ;;
    C)
        launch_server "${stream_sources[2]}"
        ;;
    D)
        launch_server "${stream_sources[3]}"
        ;;
    E)
        launch_server "${stream_sources[4]}" "" true
        ;;
    F)
        launch_server "${stream_sources[5]}" "" true
        ;;
    Q)
        force_terminate
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Loop to keep the script running and allow user to quit
while true; do
    read -p "Press Q to quit: " input
    if [[ $input == "Q" || $input == "q" ]]; then
        force_terminate
        exit 0
    fi
done
