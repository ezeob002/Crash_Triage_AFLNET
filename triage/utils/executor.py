import subprocess
import shlex
import psutil
import time


class Executor(object):

    __TIMEOUT_SIGNAL = 9998

    def __init__(self, *args, **kwargs):
        self.current_process = None
        self.cid = None
        self.shell_cmd = None

    def start_process(self, cmd, timeout=60):
        self.shell_cmd = shlex.split(cmd)
        #print(self.shell_cmd)
        try:
            if self.cid:
                try:
                    self.current_process.kill()
                except Exception as e:
                    print("Could not kill the process")
            self.p_process = self._fork()
            self.cid = self.p_process.pid
            self.current_process = psutil.Process(self.cid)

            if not self._wait_for_status(psutil.STATUS_SLEEPING, timeout=1.0):
                return False
        except Exception as e:
            return False
        return self.healthy()

    def _fork(self, env={}):
        return subprocess.Popen(
            args=self.shell_cmd,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True
        )

    def _wait_for_status(self, status: str, timeout: float = 1.0, sleep_time: float = 0.0001, negate: bool = False) -> bool:
        if self.current_process is None:
            return False
        cumulative_t = 0.0
        try:
            if not negate:
                while self.current_process.status() is not status:
                    # we are literally waiting for the process to wait on its socket
                    if cumulative_t >= timeout:
                        return False
                    time.sleep(sleep_time)
                    cumulative_t += sleep_time
            else:
                while self.current_process.status() is status:
                    # we are literally waiting for the process to wait on its socket
                    if cumulative_t >= timeout:
                        return False
                    time.sleep(sleep_time)
                    cumulative_t += sleep_time
        except Exception:
            return False
        return True

    def healthy(self):
        try:
            return self.current_process is not None and self.current_process.status() not in [psutil.STATUS_DEAD, psutil.STATUS_ZOMBIE]
        except Exception:
            return False

    def kill(self):
        if not self.current_process: return
        try:
            self.current_process.kill()
        except Exception as e:
            print("Process already died or cannot be killed!")
    
