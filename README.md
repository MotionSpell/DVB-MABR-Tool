# DVB-MABR-Tool

Welcome to the [DVB-MABR Validation Tool](https://dvb.org/news/rfp-released-for-dvb-mabr-validation-tool/).

The repository contains a Python script (`app.py`), a configuration file (`config.ini`), and three scripts for launching the application in the different modes described in the DVB's RfP a/o the V2V (Verification and Validation) document.

## Description

The Python script `app.py` is designed to configure and run a media processing application using the [GPAC](https://gpac.io) library. It loads configurations from the provided `config.ini` file and/or from the command-line, processes command-line arguments, and initiates the media processing session accordingly. The application can run in two modes: server or gateway.

## Requirements

- Python 3.x
- GPAC library (libgpac.so/.dll/.dylib):
   1. installed with a prefix detected by `pkg-config` and
   2. accessible from your shell (Windows: ```export PATH=``` ; Linux: ```export LD_LIBRARY_PATH=``` ; MacOS: ```export DYLD_LIBRARY_PATH=```)
- A MPEG-DASH player (GPAC (`gpac -play http://127.0.0.1:8080/Manifest.mpd`)), [dash.js](https://reference.dashif.org/dash.js/latest/samples/dash-if-reference-player/index.html?mpd=http://127.0.0.1:8080/Manifest.mpd), Theoplayer, ...) for viewing the stream (optional)

## Usage

1. **Configuration Setup:**
   - If necessary modify the `config.ini` file to customize settings according to your requirements. Ensure that all necessary parameters are correctly set for the chosen mode (`server` or `gateway`).
   
2. **Running Examples:**
   - The repository provides a script (`run_servers.sh`) using the TAD streaming content to demonstrate the sequential execution of server and gateway modes. This script can be executed to automatically run the servers.
   - Example usage:
     ```bash
     ./run_servers.sh
     ```
     Then choose which TAD stream to execute:

     ```bash
     Choose a stream source:
     A: Live segment template without manifest updates
     B: Live segment template with manifest updates every 30s
     C: Live segment timeline with manifest updates every 30s
     D: Multi-period, 1 period per minute
     E: low-latency single rate
     F: low-latency multi rate
     ```

     then run this command    
     ```bash
      ./scripts/launch_gateway.sh 
     ``` 
     
     to launch the gateway with default configuration.

3. **Viewing the Stream:**
   - After launching the application, you can use [dash.js](https://reference.dashif.org/dash.js/latest/samples/dash-if-reference-player/index.html?mpd=http://127.0.0.1:8080/Manifest.mpd) or the GPAC player (`gpac -play http://127.0.0.1:8080/Manifest.mpd`) to view the stream. The playback link will be provided in the terminal output for gateway mode.
   - The default playback URL is `http://127.0.0.1:8080/Manifest.mpd`.
   - When using dash.js you may need to install a CORS extension for your browser.

4. **Advanced mode: manual launch of the Application:**
   - Execute the appropriate launch script based on the desired mode:
     - For running in server mode with default multicast adreeses/options, execute ```python3 app.py config.ini mode=server stream_src="http_source_link" ```.
     - For running in gateway mode, execute  with default multicast adreeses/options```python3 app.py config.ini mode=gateway ```.
   - Example usage:
     ```bash
     ./scripts/launch_server.sh
     ./scripts/launch_gateway.sh
     ```
   - Notes on configurable options:
     - To select how the URI of objects delived should be constructed use the option: "fdt_absolute_url" in the global configuration file.
     - To select how the manifests and init segments are delivered use the option: "use_inband_transport" in the global configuration file.

## Note

Troubleshoot:
- Error or warning messages should be processed by order of appearance. There is a butterfly effect in errors so try to identify the root error.
- Ensure that the GPAC library is properly installed on your system.
- Additional parameters and configurations can be added to the `config.ini` file as needed.
- The GPAC Python bindings use ctypes for interfacing with libgpac filter session, while providing an object-oriented wrapper hiding all ctypes internals and GPAC C design.
- The timeout of the repair mode depends on [this patch](https://github.com/gpac/gpac/compare/master...rbouqueau:buildbot-mabr_client_object_timeout?expand=1) which is not yet in GPAC master.
- In case of gateway errors, one can check the state of the HTTP cache by replace the `gmem` value of `rdirs = gmem` by any valid folder. Then inspect this cache folder.

You must:
- Use the bindings which come along with your GPAC installation, otherwise ABI/API might mismatch, resulting in crashes.
- Use a regular GPAC build, not a static library version (so python bindings are not compatible with static or mp4box-only build).
- Make sure the libgpac shared library is known to your dynamic library loader.

The binding is called `libgpac.py`, and is by default available in GPAC share folder, for example `/usr/local/share/gpac/python`. It is hosted in GPAC source tree under share/python.

The Python module handler is furthermore very likely not configured to look at this directory, in `app.py` we have to indicate where to look:
     ```
        sys.path.append('/usr/local/share/gpac/python')
     ```

Alternatively you can use pip to install the binding.

For more information on this visit:
- the wiki page: [wiki](https://wiki.gpac.io/Howtos/python/)
- or this post:  [github discussion](https://github.com/gpac/gpac/issues/2161#issuecomment-1087281505)
