import feiQCoreData
import time
import os


def build_msg(command_num, option=''):
    """组装需要发送的消息"""
    # 用时间来代表id
    feiQCoreData.packet_id = int(time.time())
    # 拼装数据报
    msg = "%d:%d:%s:%s:%d:%s" % (feiQCoreData.feiQ_version, feiQCoreData.packet_id, feiQCoreData.feiQ_user_name, feiQCoreData.feiQ_host_name, command_num, option)
    
    return msg


def build_file_msg(file_name):
    """组装需要发送的文件消息"""
    try:
        # 得到文件大小
        file_size = os.path.getsize(file_name)
        # 得到文件创建时间
        file_ctime = os.path.getctime(file_name)
    except:
        print('%s >>文件不存在，请重新输入' % file_name)
    else:
        # 文件序号：文件名：文件大小：文件修改时间：文件类型
        # 0:test.doc:05600:5983d77e:1:
        option_str = "%d:%s:%x:%x:%x" % (0, file_name, file_size, int(file_ctime), feiQCoreData.IPMSG_FILE_REGULAR)
        command_num = feiQCoreData.IPMSG_SENDMSG | feiQCoreData.IPMSG_FILEATTACHOPT
        file_str = '\0' + option_str
        return build_msg(command_num, file_str)


def send_msg(send_data, dest_ip):
    """发送数据"""
    feiQCoreData.udp_socket.sendto(send_data.encode('gbk'), (dest_ip, feiQCoreData.feiQ_port))


def send_broadcast_online_msg():
    """发送上线提醒"""
    online_msg = build_msg(feiQCoreData.IPMSG_BR_ENTRY, feiQCoreData.feiQ_user_name)
    send_msg(online_msg, feiQCoreData.broadcast_ip)
    print('on line')


def send_broadcast_offline_msg():
    """发送下线提醒"""
    offline_msg = build_msg(feiQCoreData.IPMSG_BR_EXIT, feiQCoreData.feiQ_user_name)
    send_msg(offline_msg, feiQCoreData.broadcast_ip)
    print('off line')


def send_msg_2_ip(dest_ip, send_data):
        chat_msg = build_msg(feiQCoreData.IPMSG_SENDMSG, send_data)
        send_msg(chat_msg, dest_ip)
        print('发送成功')


def send_file_2_ip(dest_ip, send_data):
    if dest_ip and send_data:
        file_msg = build_file_msg(send_data)
        send_msg(file_msg, dest_ip)

        # 组织数据将其发送给子进程，告知其文件名，包编号，文件序号
        send_file_info = dict()
        send_file_info['packet_id'] = feiQCoreData.packet_id
        send_file_info['file_name'] = send_data
        send_file_info['file_id'] = 0

        send_info = dict()
        send_info["type"] = 'send_file'
        send_info['data'] = send_file_info

        feiQCoreData.file_info_queue.put(send_info)
