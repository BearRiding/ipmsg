from socket import *
import feiQCoreData
import threading
import feiQSendMsg
import feiQRecv

def deal_feiq_data(recv_data):
    """处理接收到的飞鸽数据"""
    return feiQRecv.deal_feiq_data(recv_data)


def deal_option_data(feiq_data):
    """处理飞鸽数据中option包编号和文件序号"""
    option_list = feiq_data['option'].split(":", 3)
    packet_id = option_list[0]
    file_id = option_list[1]

    return int(packet_id, 16), int(file_id)


def send_file(client_socket):
    """发送文件给客户端"""
    recv_data = client_socket.recv(1024)
    #print(recv_data) >>>b'1_lbt80_0#128#F0DEF1E52ADF#0#0#0#4000#9:1502097760:Administrator:\xd5\xb2\xc0\xf6\xbe\xfd:96:5987d043:0:0:'
    feiq_data = deal_feiq_data(recv_data)
    # 处理'option': '5987d043:0:0:'
    packet_id, file_id = deal_option_data(feiq_data)
    print("对方发送文件的包编号：%d, 序号：%d" % (packet_id, file_id))
    for file_info_data in feiQCoreData.file_list:
        if packet_id == file_info_data['packet_id'] and file_id == file_info_data['file_id']:
            try:
                f = open(file_info_data['file_name'], 'rb')
                while True:
                    content = f.read(1024)
                    if content:
                        # 如果从文件中读取数据，就给tcp客户端发过去
                        client_socket.send(content)
                    else:
                        break
                f.close()
            except Exception as ret:
                print("发送文件失败:%s" % ret)
            else:
                print("%s>>>发送成功" % file_info_data['file_name'])

                # 发送成功就从列表删除
                feiQCoreData.file_list.remove(file_info_data)
                break # 不加break出现执行下一行else:
    else:
        print('没有找到要发送的文件×××××')
    client_socket.close()


def get_file_info_from_queue(file_info_queue):
    """获取文件信息来着进程间的消息"""
    while True:
        file_info = file_info_queue.get()
        print('刚刚收到的文件信息是：', file_info)
        if file_info['type'] == 'send_file':
            # 若是发送文件
            feiQCoreData.file_list.append(file_info['data'])
            for i, file_info_data in enumerate(feiQCoreData.file_list):
                print(i, file_info_data)
        elif file_info['type'] == 'download_file':
            # 若是下载文件
            download_file(file_info['data'])


def download_file(file_data):
    """下载文件"""
    # 创建一个tcp套接字
    tcp_client_socket = socket(AF_INET, SOCK_STREAM)
    # 链接服务器
    tcp_client_socket.connect((file_data['dest_ip'], feiQCoreData.feiQ_port))
    # 处理下载文件option信息(59826220:0:0:)
    download_file_option = '%x:%x:%x' % (file_data['packet_id'], file_data['file_id'], 0)
    # 构建信息b'1_lbt80_0#128#F0DEF1E52ADF#0#0#0#4000#9:1501745760:Administrator:\xd5\xb2\xc0\xf6\xbe\xfd:96:59826220:0:0:'
    download_file_msg = feiQSendMsg.build_msg(feiQCoreData.IPMSG_GETFILEDATA, download_file_option)
    # 发送数据给服务器
    tcp_client_socket.send(download_file_msg.encode('gbk'))
    # 接收数据
    try:
        f = open(file_data['file_name'], 'wb')
        file_size = file_data['file_size']
        recv_size = 0
        while True:
            recv_data = tcp_client_socket.recv(1024)
            if recv_data:
                f.write(recv_data)
            else:
                break
            recv_size += len(recv_data)
            if recv_size >= file_size:
                break
    except Exception as ret:
        print('下载文件错：%s' % ret)
    else:
        print("%s>>>>下载成功" % file_data['file_name'])
        f.close()
    tcp_client_socket.close()


def tcp_main(file_info_queue):
    """tcp_main主控此进程"""
    # 创建一个子线程来接受进程间的queue
    recv_queue_thread = threading.Thread(target=get_file_info_from_queue, args=(file_info_queue,))
    recv_queue_thread.start()

    # 创建tcp套接字
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    # 绑定本地信息
    tcp_server_socket.bind(("", feiQCoreData.feiQ_port))
    # 将套接字转换成监听套接字
    tcp_server_socket.listen(128)
    
    while True:
        # 循环等待新客户端的链接,阻塞的
        client_socket, client_addr = tcp_server_socket.accept()
        # 创建子线程为其接受文件消息
        send_file_thread = threading.Thread(target=send_file, args=(client_socket,))
        send_file_thread.start()
        

if __name__ == "__main__":
    tcp_main()
    
