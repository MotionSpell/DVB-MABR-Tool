# DVB-MABR-Tool

Welcome to the [DVB-MABR Validation Tool](https://dvb.org/news/rfp-released-for-dvb-mabr-validation-tool/).

The repository contains a Python script (`app.py`), a configuration file (`config.ini`), and three scripts for launching the application in the different modes described in the RfP a/o the V2V document.

## Description

The Python script `app.py` is designed to configure and run a media processing application using the GPAC library. It loads configurations from the provided `config.ini` file and/or from the commandline, processes command-line arguments, and initiates the media processing session accordingly. The application can run in two modes: server or gateway.

## Requirements

- Python 3.x
- GPAC library (libgpac.so/.dll/.dylib):
   1. installed with the default prefix (```/usr/local```) and
   2. accessible from your shell (Windows: ```export PATH=``` ; Linux: ```export LD_LIBRARY_PATH=``` ; MacOS: ```export DYLD_LIBRARY_PATH=```)
- A MPEG-DASH player (GPAC, dash.js, Theoplayer, ...) for viewing the stream (optional)

## Usage

1. **Configuration Setup:**
   - Modify the `config.ini` file to customize settings according to your requirements. Ensure that all necessary parameters are correctly set for the chosen mode (`server` or `gateway`).
   
2. **Running Examples:**
   - The repository provides a script (`run_servers.sh`) using the TAD streaming content to demonstrate the sequential execution of server and gateway modes. This script can be executed to automatically run the servers.
   - Example usage:
     ```bash
     ./run_servers.sh
     ```
     Than chose wich TAD stream to execute:

     ```bash
     Choose a stream source:
     A: Live segment template without manifest updates
     B: Live segment template with manifest updates every 30s
     C: Live segment timeline with manifest updates every 30s
     D: Multi-period, 1 period per minute
     E: low-latency single rate
     F: low-latency multi rate
     ```

     than run this command    
     ```bash
      ./scripts/launch_gateway.sh 
     ``` 
     
     to launch the gateway in default configuration

3. **Viewing the Stream:**
   - After launching the application, you can use dash.js or the GPAC player to view the stream. The playback link will be provided in the terminal output for gateway mode.
   - (by default: http://127.0.0.1:8080/Manifest.mpd)
   - to use dash.js you will need to install a cors extension for your browser.

4. **Advanced mode: manual launch of the Application:**
   - Execute the appropriate launch script based on the desired mode:
     - For running in server mode with default multicast adreeses/options, execute ```python3 app.py config.ini mode=server stream_src="http_source_link" ```.
     - For running in gateway mode, execute  with default multicast adreeses/options```python3 app.py config.ini mode=gateway ```.
   - Example usage:
     ```bash
     ./scripts/launch_server.sh
     ./scripts/launch_gateway.sh
     ```

## Note

Troubleshoot:
- Ensure that the GPAC library is properly installed and on your system.
- Additional parameters and configurations can be added to the `config.ini` file as needed.
- The GPAC Python bindings use ctypes for interfacing with libgpac filter session, while providing an object-oriented wrapper hiding all ctypes internals and GPAC C design.
- The timeout of the repair mode depends on [this patch](https://github.com/gpac/gpac/compare/master...rbouqueau:buildbot-mabr_client_object_timeout?expand=1) which is not yet in GPAC master.

You must:
- Use the bindings which come along with your GPAC installation, otherwise ABI/API might mismatch, resulting in crashes.
- Use a regular GPAC build, not a static library version (so python bindings are not compatible with static or mp4box-only build).
- Make sure the libgpac shared library is known to your dynamic library loader.

The binding is called libgpac.py, and is by default available in GPAC share folder, for example /usr/share/gpac/python. It is hosted in GPAC source tree under share/python.

The Python module handler is furthermore very likely not configured to look at this directory, in app.py we have to indicate where to look:
     ```
        sys.path.append('/usr/local/share/gpac/python')
     ```

Alternatively you can use pip to install the binding. 

for more information on this visit:
the wiki page: [wiki](https://wiki.gpac.io/Howtos/python/)
or this post:  [github discussion](https://github.com/gpac/gpac/issues/2161#issuecomment-1087281505)
