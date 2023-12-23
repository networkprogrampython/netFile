#实现单线程，迭代服务器(依次服务每一个客户端)
import socket
from multiprocessing import Pool
#限制最大传输速度
MAX_BYTES = 1024
tcp_server_host = ''
tcp_server_port = 8888
tcp_server_addr = (tcp_server_host ,tcp_server_port)


#成功找到文件返回文件长度+文件二进制流；失败返回0
def get_files_content(fileName ,tcp_client_addr):
    try:
        print('{}正在请求下载{}'.format(tcp_client_addr ,fileName))
        with open('./files/' + fileName ,'rb') as fp:
            file_content = fp.read()
            #返回长度 + 二进制文件数据
            return "{:010d}".format(len(file_content)).encode("utf-8") + file_content
    except FileNotFoundError:
        print('{}请求的{}未找到'.format(tcp_client_addr ,fileName))
        return '0'.encode('utf-8')


#实现客户端和服务器交流
def communication(sock ,addr):
    print('listen to {}'.format(addr))
    while True:
        request = sock.recv(MAX_BYTES).decode('utf-8')
        if request == 'quit':
            print('{}已退出'.format(addr))
            sock.close()
            break
        else:
            response = get_files_content(request ,addr)
            sock.send(response)


def main():
    #创建空套接
    tcp_server_sock = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
    #绑定端口
    tcp_server_sock.bind(tcp_server_addr)
    #设置监听数量位4
    tcp_server_sock.listen(4)
    #设定线程池中最大数量为2
    pool = Pool(2)
    while True:
        tcp_client_sock ,tcp_client_addr = tcp_server_sock.accept()
        pool.apply_async(func=communication ,args=(tcp_client_sock ,tcp_client_addr))



if __name__ == '__main__':
    main()
