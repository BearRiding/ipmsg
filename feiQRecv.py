import feiQCoreData
import feiQSendMsg


def deal_feiq_data(recv_data):
    """处理接受到的飞鸽数据"""
    recv_data = recv_data.decode("gbk", errors="ignore")
    feiq_data_list = recv_data.split(":", 5)

    feiq_data = dict()
    feiq_data['vision'] = feiq_data_list[0]
    feiq_data['packet_id'] = feiq_data_list[1]
    feiq_data['user_name'] = feiq_data_list[2]
    feiq_data['host_name'] = feiq_data_list[3]
    feiq_data['command_num'] = feiq_data_list[4]
    feiq_data['option'] = feiq_data_list[5]

    return feiq_data


def deal_command_option_num(command_num):
    """提取命令字中的命令以及选项"""
    command = int(command_num) & 0x000000ff
    command_option = int(command_num) & 0xffffff00

    return command, command_option


def judge_and_add_online_user(user_name, host_name, dest_ip):
    """判断这个用户是否已经存在列表中，若在就添加"""
    for user_info in feiQCoreData.user_list:
        if user_info['ip'] == dest_ip:
            return

    new_online_user = dict()
    new_online_user['ip'] = dest_ip
    new_online_user['user_name'] = user_name
    new_online_user['host_name'] = host_name
    feiQCoreData.user_list.append(new_online_user)


def judge_and_del_offline_user(dest_ip):
    """判断用户下线，删除下线用户"""
    for user_info in feiQCoreData.user_list:
        if user_info["ip"] == dest_ip:
            feiQCoreData.user_list.remove(user_info)
            break


def recv_msg():
    """接受消息"""
    while True:
        recv_data, dest_addr = feiQCoreData.udp_socket.recvfrom(1024)
        feiq_data = deal_feiq_data(recv_data)
        # :288:123123123\0\0(命令字：接受信息内容)
        command, command_option = deal_command_option_num(feiq_data['command_num'])

        if command == feiQCoreData.IPMSG_BR_ENTRY:
            # 有用户上线
            print('%s上线' % feiq_data['option'])

            find_post = feiq_data['option'].find('\0')
            if find_post != -1:
                user_name = feiq_data['option'][:find_post]
            else:
                user_name = feiq_data['option']

            judge_and_add_online_user(user_name, feiq_data['host_name'], dest_addr[0])
            
            # 通报对方，我已经在线
            answer_online_msg = feiQSendMsg.build_msg(feiQCoreData.IPMSG_ANSENTRY)
            feiQSendMsg.send_msg(answer_online_msg, dest_addr[0])

        elif command == feiQCoreData.IPMSG_BR_EXIT:
            # 用户下线
            print("%s下线" % feiq_data['user_name'])
            judge_and_del_offline_user(dest_addr[0])
        
        elif command == feiQCoreData.IPMSG_ANSENTRY:
            # 对方通报在线
            print('%s已经在线' % feiq_data['user_name'])
            judge_and_add_online_user(feiq_data['option'][:feiq_data['option'].find('\0')], feiq_data['host_name'], dest_addr[0])

        elif command == feiQCoreData.IPMSG_SENDMSG:
            # 接受消息

            # 判断发送的消息为文件消息..一般是\0 0:test.doc:05600:5983d77e:1:(\0 文件序号：文件名：文件大小：文件修改时间：文件类型：)
            if command_option & 0x00f00000 == feiQCoreData.IPMSG_FILEATTACHOPT:
                file_msg_list = feiq_data['option'][feiq_data['option'].find('\0')+1:].split(':', 5)

                download_file_info = dict()
                download_file_info['file_id'] = int(file_msg_list[0])
                download_file_info['file_name'] = file_msg_list[1]
                download_file_info['file_size'] = int(file_msg_list[2], 16)
                download_file_info['dest_ip'] = dest_addr[0]
                download_file_info['packet_id'] = int(feiq_data['packet_id'])

                feiQCoreData.download_file_list.append(download_file_info)
            else:
                global message
                print("\n收到来着《%s》消息：%s" % (feiq_data['user_name'], feiq_data['option']))
                message = 'from ' + feiq_data['user_name'] + '  ' + feiq_data['option']

            # 给对方发送消息确认(告知对方已经收到了)
            recv_ok_msg = feiQSendMsg.build_msg(feiQCoreData.IPMSG_RECVMSG)
            feiQSendMsg.send_msg(recv_ok_msg, dest_addr[0])

            
message = 'null'
            

