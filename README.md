# Crash Triage for MCFICS and AFLNET

### Preresiquite
**System:**
```bash
sudo apt-get update && sudo apt get install python3 python3-pip python3-venv
```
## Installation (Tested on Ubuntu 20.04)
1. Install Crash Triage
```bash
git clone --recursive git@github.com:ezeob002/Crash_Triage_AFLNET.git # clone
cd Crash_Triage_AFLNET                         # workdir
python3 -m venv env                     # Creat virtual environment
source env/bin/activate                 # Activate virtual environment
cd 3rd_party_code/exploitable                           
python setup.py install              # Install exploitable
cd ../..                              # Move to the top tree folder       
pip install -r requirements.txt         # Install other libraries
```


This gives a compiled server example
## Usage

```bash
python crash_triage.py --help

usage: crash_triage.py [-h] [-dp DATA_PATH] [-sp SERVER_PATH] [-rp RESULT_PATH] [-st SEND_TIMEOUT]
                       [-rt RECV_TIMEOUT] [-p PORT] [-hs HOST]

 A script to help investigate crash from AFLNET and MCFICS

optional arguments:
  -h, --help            show this help message and exit
  -dp DATA_PATH, --data_path DATA_PATH
                        Data path of the Crash input
  -sp SERVER_PATH, --server_path SERVER_PATH
                        Compiled server path
  -rp RESULT_PATH, --result_path RESULT_PATH
                        result path
  -st SEND_TIMEOUT, --send_timeout SEND_TIMEOUT
                        Send Timeout
  -rt RECV_TIMEOUT, --recv_timeout RECV_TIMEOUT
                        Recv timeout
  -p PORT, --port PORT  target port
  -hs HOST, --host HOST target host

```
**Run the example server for EPICS**
```bash
python crash_triage.py -dp /your-afl-data-path
```
## Acknowledgement 
We would like to the following code repository, this project will not be possible with this code base.


* Network Protocol Fuzzing for Humans [BooFuzz](https://github.com/jtpereyda/boofuzz)

## Owner of Repo 

* **Uchenna Ezeobi** (uezeobi@uccs.edu, uchenna.ezeobi3@gmail.com)