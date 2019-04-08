from socket import *
import multiprocessing
import feiQCoreData
import threading
import feiQSendMsg
import feiQRecv
import feiQTcp
import sys

def create_udp_socket():
    # 创建udp套接字
    # 创建UDP套接字
    feiQCoreData.udp_socket = socket(AF_INET, SOCK_DGRAM)
    # 绑定本地信息
    feiQCoreData.udp_socket.bind(('', feiQCoreData.feiQ_port))
    # 设置允许广播
    feiQCoreData.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


def display_menu():
    """显示用户界面"""
    print("=" * 30)
    print("——飞鸽传书 v 3.0——")
    print("1. 上线广播")
    print("2. 下线广播")
    print("3. 向指定ip发送消息")
    print("4. 显示所用在线用户列表")
    print("5. 向指定ip发送文件")
    print("6. 显示要要下载文件")
    print("7. 下载文件")
    print("0. 退出系统")
    print("=" * 30)


def display_all_online_users():
    """显示所有已在线用户"""
    for i, user_info in enumerate(feiQCoreData.user_list):
        print(i, user_info)


def display_download_file_list():
    """显示要下载的文件"""
    for i, file_info in enumerate(feiQCoreData.download_file_list):
        print(i, file_info)


def send_download_file_2_process():
    """向子进程中发送要下载的文件信息"""
    display_download_file_list() # 显示下载文件信息
    try:
        num = int(input("请输入你要下载文件的序号："))
    except:
        print('输入有误')
    else:
        file_info = dict()
        file_info['type'] = "download_file"
        file_info['data'] = feiQCoreData.download_file_list[num]
        feiQCoreData.file_info_queue.put(file_info)

def start():
    # 创建一个队列Queue
    feiQCoreData.file_info_queue = multiprocessing.Queue()
    # 创建子进程来完成tcp相关数据
    tcp_process = multiprocessing.Process(target=feiQTcp.tcp_main, args=(feiQCoreData.file_info_queue,))
    tcp_process.start()

    # 创建udp套接字
    create_udp_socket()
    # 创建一个子线程，来循环接受udp消息
    recv_msg_thread = threading.Thread(target=feiQRecv.recv_msg)
    recv_msg_thread.start()

def main():
    # 10.15.166.14
    # 循环显示用户界面
    display_menu()
    command_num = int(input("请用户输入选项的序号:"))
    if command_num == 1:
        # 发送上线提醒
        feiQSendMsg.send_broadcast_online_msg()
    elif command_num == 2:
        # 发送下线提醒
        feiQSendMsg.send_broadcast_offline_msg()
    elif command_num == 3:
        # 向指定ip发送消息
        feiQSendMsg.send_msg_2_ip()
    elif command_num == 4:
        # 显示在线用户列表
        display_all_online_users()
    elif command_num == 5:
        # 向指定ip发送文件
        feiQSendMsg.send_file_2_ip()
    elif command_num == 6:
        # 显示要下载的文件
        display_download_file_list()
    elif command_num == 7:
        # 下载的文件
        send_download_file_2_process()
    elif command_num == 0:
        # 退出系统
        feiQSendMsg.send_broadcast_offline_msg()
        feiQCoreData.udp_socket.close()
        exit()