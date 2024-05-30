#!/bin/bash

# Get arguments
stream_src="$1"
manifest_dst="${2}"  # Use default value if manifest_dst is not provided

python3 app.py config.ini mode=server stream_src="$stream_src" manifest_dst="$manifest_dst" 
