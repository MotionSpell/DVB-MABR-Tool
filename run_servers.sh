#!/bin/bash

# Define the list of stream sources
stream_sources=(
    "https://livesim2.dashif.org/livesim2/testpic_2s/Manifest.mpd"
    "https://livesim2.dashif.org/livesim2/mup_30/testpic_2s/Manifest.mpd"
    "https://livesim2.dashif.org/livesim2/segtimeline_1/testpic_2s/Manifest.mpd"
    "https://livesim2.dashif.org/livesim2/periods_60/continuous_1/testpic_2s/Manifest.mpd"
)

# Function to launch server
launch_server() {
    local src="$1"
    local dst="$2"
    ./scripts/launch_server.sh "$src" "$dst" &
}

# Ask user for choice
echo "Choose a stream source:"
echo "A: Live segment template without manifest updates"
echo "B: Live segment template with manifest updates every 30s"
echo "C: Live segment timeline with manifest updates every 30s"
echo "D: Multi-period, 1 period per minute"
echo "E: All streams"
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
        for ((i=0; i<${#stream_sources[@]}; i++)); do
            launch_server "${stream_sources[i]}"
        done
        ;;
    *)
        echo "Invalid choice. Exiting."
        ;;
esac