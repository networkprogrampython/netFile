import socket

MAX_BYTES = 100
tcp_server_host = '127.0.0.1'
tcp_server_port = 8888
tcp_server_addr = (tcp_server_host ,tcp_server_port)


def main():
    # #创建空套接字
    tcp_client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #连接主机服务器
    tcp_client_sock.connect(tcp_server_addr)
    communication(tcp_client_sock)


#实现客户端和服务器之间的交流
def communication(sock):
    while True:
        request = input('请输入需要下载的文件名(退出输入："quit")：')
        sock.send(request.encode('utf-8'))

        if request == 'quit':
            print('服务结束')
            break
        # 返回文件长度（只接受前十位）
        file_length = int(sock.recv(10).decode('utf-8'))
        if file_length == 0:
            print('文件名未找到！')
            continue
        else:
            print('文件大小为：{}\n正在下载中。。。。。。'.format(file_length))
            file_content = b''
            while file_length > 0:
                temp_data = sock.recv(MAX_BYTES)
                file_content += temp_data
                file_length -= MAX_BYTES
            with open('./' + request ,'wb') as fp:
                fp.write(file_content)
            print('文件下载成功!')

    sock.close()


if __name__ == '__main__':
    main()
