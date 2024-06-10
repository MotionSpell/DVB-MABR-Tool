#!/usr/bin/python3
import subprocess
import sys
import configparser
gpac_prefix = subprocess.check_output(['pkg-config', '--variable=prefix', 'gpac']).decode('utf-8').strip()
share_folder = gpac_prefix + '/share/gpac/python/'
sys.path.append(share_folder)
import libgpac as gpac

def load_configuration(config_file):
    config = configparser.ConfigParser(inline_comment_prefixes=(';', '#'))
    config.read(config_file)
    src_args = {}
    server_args = {}
    gateway_args = {}
    mode = ''
    for section in config.sections():
        if section == 'Source':
            src_args = dict(config['Source'])
        elif section == 'Server':
            server_args = dict(config['Server'])
        elif section == 'Gateway':
            gateway_args = dict(config['Gateway'])
        elif section == 'Mode':
            mode = config['Mode'].get('mode', '').lower()
    return src_args, server_args, gateway_args, mode

def main():
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python app.py <config_file>")
        return

    config_file = sys.argv[1]

    # Load configuration from the specified file
    src_args, server_args, gateway_args, mode = load_configuration(config_file)

    # Merge command-line arguments with configuration
    for arg in sys.argv[2:]:
        key, value = arg.split('=')
        if key == "mode":
            mode = value
        elif key in src_args:
            src_args[key] = value
        elif key in server_args:
            server_args[key]=value
        elif key in gateway_args:
            gateway_args[key] = value
        else:
            print("invalid option from cli: retrurning")
            return

    # Prepare options for libgpac
    opts = ["myapp"]
    opts.append("-no-block")
    gpac.set_args(opts)
    gpac.set_logs("route@debug")

    # Create session
    fs = gpac.FilterSession()
    
    # Load server or gateway filter based on mode
    if mode == 'server':
        # Load source filter
        if 'stream_src' in src_args and src_args['stream_src'].strip():  # Check if stream_src is not empty
            src_filter = src_args['stream_src']
            src = fs.load_src(src_filter)
            dasher = fs.load("dashin:forward=file")
            
        else:
            src_filter = "avgen"
            src = fs.load_src(src_filter)
            aenc = fs.load(f"ffenc:c={src_args.get('a_enc', 'aac')}")
            venc = fs.load(f"ffenc:c={src_args.get('v_enc', 'avc')}")
            dasher = fs.load("dasher:dynamic:profile=live")

        # Load destination filter for server mode
        if server_args['llmode'] == "true":
            dst_filter = f"{server_args['protocol']}{server_args['ip_dst']}:{server_args['port_dst']}{server_args['manifest_dst']}:llmode"
        else:
            dst_filter = f"{server_args['protocol']}{server_args['ip_dst']}:{server_args['port_dst']}{server_args['manifest_dst']}"
        dst = fs.load_dst(dst_filter)
    
    elif mode == 'gateway':
        # Load source for gateway
        src_sess = f"{gateway_args['protocol']}{gateway_args['ip_src']}:{gateway_args['port_src']}{gateway_args['manifest_src']}"
        src = fs.load_src(src_sess)

        # load dasher 
        dasher= fs.load("dashin:forward=file")
        
        #load http server
        dst_sess =  f"{gateway_args['ip_addr']}:{gateway_args['port_addr']}{gateway_args['dst']}:rdirs={gateway_args['rdirs']}:max_cache_size={gateway_args['max_cache_size']}:reqlog='*':cors=auto:sutc={gateway_args['sutc']}" 
        print(f"playback link   :  {gateway_args['ip_addr']}:{gateway_args['port_addr']}{gateway_args['dst']}")
        dst = fs.load_dst(dst_sess)
        
    else:
        print("Invalid mode specified in configuration file")
        return
    

    # Run the filter session
    fs.run()

if __name__ == "__main__":
    main()
