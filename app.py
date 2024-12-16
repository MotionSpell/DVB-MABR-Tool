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
    repair_args = {}
    for section in config.sections():
        if section == 'Source':
            src_args = dict(config['Source'])
        elif section == 'Server':
            server_args = dict(config['Server'])
        elif section == 'Gateway':
            gateway_args = dict(config['Gateway'])
        elif section == 'Mode':
            mode = config['Mode'].get('mode', '').lower()
        elif section == 'Repair':
            repair_args = dict(config['Repair'])
    return src_args, server_args, gateway_args, mode, repair_args

def main():
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python app.py <config_file>")
        return

    config_file = sys.argv[1]

    # Load configuration from the specified file
    src_args, server_args, gateway_args, mode, repair_args = load_configuration(config_file)

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
    opts.append("-no-h2")
    opts.append("-rescan-fonts")
    gpac.set_args(opts)

    # Create session
    fs = gpac.FilterSession()
    
    # Load server or gateway filter based on mode
    if mode == 'server':
        # Load source filter
        if 'stream_src' in src_args and src_args['stream_src'].strip():  # Check if stream_src is not empty
            src_filter = src_args['stream_src']
            src = fs.load_src(src_filter)
            dasher = fs.load("dashin:forward=file:split_as")

        else:
            src = fs.load_src("avgen")
            aenc = fs.load(f"ffenc:c={src_args.get('a_enc', 'aac')}")
            venc = fs.load(f"ffenc:c={src_args.get('v_enc', 'avc')}")
            reframer = fs.load(f"reframer:rt=on")
            dasher = fs.load("dasher:dmode=dynamic:stl")
            manifest_src={server_args['manifest_src']}

        # Load destination filter for server mode
        dst_filter_base = f"{server_args['protocol']}{server_args['ip_dst']}:{server_args['port_dst']}/{server_args['manifest_src']}:furl={server_args['fdt_absolute_url']}:carousel={server_args['carousel']}:ifce={server_args['ifce']}:use_inband={server_args['use_inband_transport']}"
        dst_filter = (dst_filter_base + (":llmode" if server_args['low_latency'] == "true" else "")
                                        + (f":errsim={server_args['errsim']}" if server_args.get('errsim') else ""))
        dst = fs.load_dst(dst_filter)
        gpac.set_logs(server_args["logs"])
    
    elif mode == 'gateway':
        # Load source for gateway
        repair_urls = ",".join(repair_args['repair_urls'].split('\n'))
        src_sess_base = f"{gateway_args['protocol']}{gateway_args['ip_src']}:{gateway_args['port_src']}:ifce={gateway_args['ifce']}:repair={repair_args['repair']}:nbcached={gateway_args['nbcached']}"
        src_sess = src_sess_base + (f"::repair_urls={repair_urls}" if repair_urls!="" else "")
        print(src_sess)
        src = fs.load_src(src_sess)

        # load dasher 
        dasher_base= f"dashin:forward=file:split_as:keep_burl={gateway_args['keep_base_url']}"
        dasher_string = dasher_base + (f":relative_url={gateway_args['relative_url']}" if gateway_args['keep_base_url'] == "inject" else "")
        dasher= fs.load(dasher_string)
        
        #load http server
        dst_sess =  f"{gateway_args['ip_addr']}:{gateway_args['port_addr']}/{gateway_args['dst']}:rdirs={gateway_args['rdirs']}:max_cache_size=-{gateway_args['max_cache_size']}:reqlog='*':cors=auto:sutc={gateway_args['sutc']}:max_cache_segs={gateway_args['max_segs']}"
        print(f"playback link  :  {gateway_args['ip_addr']}:{gateway_args['port_addr']}/{gateway_args['dst']}")
        dst = fs.load_dst(dst_sess)
        gpac.set_logs(gateway_args["logs"])
        
    else:
        print("Invalid mode specified in configuration file")
        return
    

    # Run the filter session
    fs.run()

if __name__ == "__main__":
    main()
