import os
import glob
import time
import hashlib
import signal
import argparse

from triage.utils.executor import Executor
from triage.utils.replay import Replay
from triage.utils.tcp_socket_connection import TCPSocketConnection
from triage.utils.ip_constants import DEFAULT_MAX_RECV

def main():
    message= " A script to help investigate crash from AFLNET and MCFICS"
    parser = argparse.ArgumentParser(
            description=message,
            formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument("-dp", "--data_path", type=str, help="Data path of the Crash input")
    parser.add_argument("-sp", "--server_path", type=str, default="./targets/mailbox mypv", help="Compiled server path")
    parser.add_argument("-rp", "--result_path", type=str, default="./result", help="result path")
    parser.add_argument("-st", "--send_timeout", type=int, default=3.0, help="Send Timeout")
    parser.add_argument("-rt", "--recv_timeout", type=int, default=3.0, help="Recv timeout")
    parser.add_argument("-p", "--port", type=int, default=5075, help="target port")
    parser.add_argument("-hs", "--host", type=str, default="127.0.0.1",  help="target host")
    args = parser.parse_args()
    # You're running on a 64 bits computer 
    gdb_script = """ printf "[+] Disabling verbose and complaints"\n
        set verbose off
        set complaints 0
        set logging file %s
        set logging on
        r
        printf "[+] Backtrace:"\n
        bt
        printf "[+] info reg:"\n
        info reg
        printf "[+] exploitable:"\n
        source 3rd_party_code/exploitable/exploitable/exploitable.py
        exploitable
        printf "[+] disassemble $rip, $rip+16:"\n
        disassemble $rip, $rip+16
        printf "[+] list"\n
        list
    """

    # Assumption that you installed and the target is already instrumented

    server_with_gdb =  Executor()
    data_path = args.data_path
    server_path = args.server_path
    data = []
    for root, dirs, files in os.walk(data_path):
            for file in files:
                if not file.endswith(".txt"): # To avoid README.txt
                    data.append(os.path.join(root,file))
    # print(len(data))

    client = TCPSocketConnection(host=args.host,
                                     port=args.port,
                                     send_timeout=args.send_timeout,
                                     recv_timeout=args.recv_timeout)

    res_path = args.result_path
    os.makedirs(res_path, exist_ok=True)
    N = 1 #Hard code for now.
    cmd = 'gdb -x gdb.script --batch --args {}  '.format(args.server_path)
    for d in data:
        seq = Replay.replay_data_afl(d)
        file_name = os.path.basename(d)
        for i in range(N):
            output_gdb_script = gdb_script % ("{}/{}.txt".format(res_path,file_name))
            open('gdb.script', 'w').write(output_gdb_script)
            abort_test = False
            try:
                res = server_with_gdb.start_process(cmd)
                #Connect ot the server through the client and send sequence of messages
                time.sleep(1)
                try:
                    client.open()
                except Exception as e:
                    for _ in range(3):
                        server_with_gdb.start_process(cmd)
                        print("Trying to restart")
                        time.sleep(2)
                        try:
                            client.open()
                            break
                        except Exception as e:
                            abort_test = True
                if abort_test:
                    print("Could not connect, aborting")
                    continue
                for s in seq:
                    try:
                        print("Sending {}".format(s))
                        client.send(s)
                        recv = client.recv(DEFAULT_MAX_RECV)
                        print("Receiving {}".format(recv))
                        time.sleep(0.001)
                    except Exception as e:
                        print(" {} got this error - {}".format(d, e))
            except Exception as e:
                print(e)
            finally:
                try:
                    time.sleep(1.0)
                    if (server_with_gdb.p_process.poll() is None):
                        server_with_gdb.kill()
                    time.sleep(0.05)
                except:
                    pass
        exit()
        
            
if __name__ == "__main__":
    main()
