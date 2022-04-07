import os
import hashlib
from ftp.server.conf.conf import configuration

block_size = configuration['block_size']
md5chk_alter = configuration['md5_check_alternation']

def read_in_block(file_path):
    m = hashlib.md5()
    with open(file_path, "rb") as f:
        while True:
            block = f.read(block_size)  # 每次读取固定长度到内存缓冲区
            if block:
                m.update(block)
                yield block
            else:
                return m.hexdigest()   # 如果读取到文件末尾，则退出

def check_md5(file_path,check_size=None, start_position=0):
    m = hashlib.md5()
    check_size = check_size if check_size else os.path.getsize(file_path)
    block = int(check_size / md5chk_alter) if check_size > block_size * 10 else block_size
    with open(file_path, "rb") as f:
        f.seek(start_position)
        while check_size:
            if check_size > block:
                content = f.read(block_size)
                m.update(content)
                f.seek(f.tell() - block_size + block)
                check_size -= block
            else:
                f.read(check_size)
                m.update(content)
                check_size -= check_size
    return m.hexdigest()

