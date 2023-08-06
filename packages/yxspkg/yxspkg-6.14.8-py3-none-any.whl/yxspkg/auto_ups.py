import os,socket
import time,subprocess

def getip():
    afi = socket.AF_INET
    ip8 = '8.8.8.8'
    try:
        s=socket.socket(afi,socket.SOCK_DGRAM)
        s.connect((ip8,80))
        ip=s.getsockname()[0]
    except:
        ip = None
    finally:
        s.close()
    return ip

def main():
    mt = 0
    ok = False
    p = os.environ['PATH']
    p += ':/sbin:/usr/sbin'
    os.environ['PATH'] = p
    while True:
        t = getip()
        if t is None:
            mt += 1
        else:
            ok = True 
            mt = 0
        if mt>3 and ok:
            print('poweroff')
            os.system('poweroff')
            break
        print('sleep 60')
        time.sleep(60)
if __name__=='__main__':
    main()