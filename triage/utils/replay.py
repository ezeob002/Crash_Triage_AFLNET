import pickle
import struct

class Replay(object):

    # def __init__(self):
    #     self.data = None
    """ Ignore this, For MCFICS (My fuzzer) """
    @staticmethod
    def read_data(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data
    """ This is the method for processing AFLNET """
    @staticmethod
    def replay_data_afl(file_path):
        packet_count = 0
        seq = list()
        size_of_unsigned_int = struct.calcsize('I')
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(size_of_unsigned_int)
                if not data:
                    break
                size = struct.unpack('I', data)[0]
                if size:
                    packet_count += 1
                    #print(f"\nSize of the current packet {packet_count} is {size}\n")
                    buf = f.read(size)
                    seq.append(buf)
        return seq