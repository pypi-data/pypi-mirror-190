import os,socket
import time,subprocess
import click

global_route = {'route':None}
def update_route():
    stat,output = subprocess.getstatusoutput('ip route')
    if stat != 0:
        raise Exception('No such command: ip')
    output = [i.split()[2] for i in output.splitlines() if i.strip().startswith('default')]
    if output:
        global_route['route'] = output
def get_connect():
    route = global_route['route']
    if not route:
        update_route()
        route = global_route['route']
    connected = False 
    if route:
        for i in route:
            stat,_ = subprocess.getstatusoutput(f'ping -c 3 {i}')
            if stat == 0:
                connected = True 
                break 
        if not connected:
            update_route()
    return connected
        
def run(poweroff):
    mt = 0
    ok = False
    p = os.environ['PATH']
    p += ':/sbin:/usr/sbin:/usr/bin'
    os.environ['PATH'] = p

    wait_time,check_time = 147,24
    while True:
        connected = get_connect()
        print('connected:',connected)
   
        if not connected:
            mt += 1
            slpt = check_time
            if not ok:
                slpt = wait_time
        else:
            ok = True 
            mt = 0
            slpt = wait_time
        if mt>3 and ok:
            os.system(poweroff)
            break
        print(f'sleep {slpt}')
        time.sleep(slpt)

@click.command()
@click.option('--poweroff_cmd','-p',default='poweroff')
def main(poweroff_cmd):
    run(poweroff_cmd)
if __name__=='__main__':
    main()