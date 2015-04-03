function! Tl1send()
python << EOF
import vim
import socket
class TcpClient:
    def __init__(self):
        self.address = ('127.0.0.1', 3344)  
        self.sok = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    def send_mess(self, mess):
        self.sok.sendto(mess, self.address) 

cur_buf = vim.current.buffer
w = vim.current.window

(row, col) = w.cursor
tcpClient = TcpClient()
send_mess = format(cur_buf[row-1])
#print(send_mess)
tcpClient.send_mess(send_mess)

EOF
endfunction
