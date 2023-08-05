# -*- coding: utf-8 -*-
import os
import sys
import zlib
import time
import uuid
import pickle
import socket
import queue
import bcrypt
import hashlib
import threading
import traceback
from tqdm import tqdm
from pathlib import Path
from datetime import datetime

import ChatRoom
from ChatRoom.log import Log
from ChatRoom.encrypt import encrypt_rsa, encrypt_aes
from ChatRoom.MessyServerHardware import MessyServerHardware

FILE_LOG_FILE_PATH = os.path.join(ChatRoom.__file__.replace("__init__.py", ""), "file_log.log")
FILE_LOG_LOCK = threading.Lock()

FILE_SEND_BUFFER_SIZE = 1048576
FILE_MD5_BLOCKSIZE = 1048576

class User():
    pass

# ========================= 自身使用 ============================
class ShareObject(object):

    def __init__(self, master, flush_time_interval=60):
        self._master = master
        self._share_dict = {}

        self.__flush_time_interval = flush_time_interval
        self.__auto_flush_server()

    def __str__(self) -> str:
        return str(self._share_dict)

    def __repr__(self) -> str:
        return str(self._share_dict)

    def __getitem__(self, key):
        return self._share_dict[key]

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)

    def __iter__(self):
        return self._share_dict.__iter__()

    def _items_(self):
        return self._share_dict.items()

    def __setattr__(self, attr: str, value) -> None:
        """ set & modify"""
        # 保存变量
        super().__setattr__(attr, value)

        if not attr.startswith("_"):
            # 保存字典
            self._share_dict[attr] = value
            # 向所有其他用户发送该变化
            for user in [getattr(self._master.user, user_attr) for user_attr in dir(self._master.user) if not user_attr.startswith("_")]:
                try:
                    user_name = user._name
                except AttributeError:
                    # 这个异常可以过滤掉自身,因为自身中是没有_name属性的且该变化不用发送给自身
                    continue

                self._master.send(user_name, ["CMD_SHARE_UPDATE", {attr:value}])
                # print("send", user._name, ["CMD_SHARE_UPDATE", {attr:value}])

    def __delattr__(self, name: str) -> None:
        """ del """
        # 删除变量
        try:
            super().__delattr__(name)
        except AttributeError:
            pass

        try:
            del self._share_dict[name]
        except KeyError:
            pass

        if not name.startswith("_"):
            # 保存字典
            # 向所有其他用户发送该变化
            for user in [getattr(self._master.user, user_attr) for user_attr in dir(self._master.user) if not user_attr.startswith("_")]:
                try:
                    user_name = user._name
                except AttributeError:
                    # 这个异常可以过滤掉自身,因为自身中是没有_name属性的且该变化不用发送给自身
                    continue

                self._master.send(user_name, ["CMD_SHARE_DEL", name])
                # print("send", user._name, ["CMD_SHARE_DEL", name])

    def __auto_flush_server(self):
        """ 每隔一段时间自动同步 """
        # ShareObject 的同步间隔为60s,这个60s比较长,这个功能只是保险,因为任何的修改,赋值,删除都会即刻更新到其他节点上,这里只保证即刻更新后的同步机制
        def sub():
            while True:
                try:
                    time.sleep(self.__flush_time_interval)
                    for user in [getattr(self._master.user, user_attr) for user_attr in dir(self._master.user) if not user_attr.startswith("_")]:
                        try:
                            user_name = user._name
                        except AttributeError:
                            # 这个异常可以过滤掉自身,因为自身中是没有_name属性的且该变化不用发送给自身
                            continue

                        self._master.send(user_name, ["CMD_SHARE_FLUSH", self._share_dict])
                        # print("send", user._name, ["CMD_SHARE_UPDATE", {attr:value}])

                except Exception as err:
                    self._master._log.log_info_format_err("Flush Err", "同步share错误!")
                    traceback.print_exc()
                    print(err)

        auto_flush_server_th = threading.Thread(target=sub)
        auto_flush_server_th.daemon = True
        auto_flush_server_th.start()

class StatusObject(object):

    def __init__(self, master, flush_time_interval=30):
        self._master = master
        self._share_dict = {}

        self.__flush_time_interval = flush_time_interval
        self.__auto_flush_server()

        self.__mshd = MessyServerHardware()

    def __str__(self) -> str:
        return str(self._share_dict)

    def __repr__(self) -> str:
        return str(self._share_dict)

    def __getitem__(self, key):
        return self._share_dict[key]

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)

    def __iter__(self):
        return self._share_dict.__iter__()

    def _items_(self):
        return self._share_dict.items()

    def __setattr__(self, attr: str, value) -> None:
        """ set & modify"""
        # 保存变量
        super().__setattr__(attr, value)

        if not attr.startswith("_"):
            # 保存字典
            self._share_dict[attr] = value

    def __delattr__(self, name: str) -> None:
        """ del """
        # 删除变量
        try:
            super().__delattr__(name)
        except AttributeError:
            pass

        try:
            del self._share_dict[name]
        except KeyError:
            pass

    def __auto_flush_server(self):
        """ 每隔一段时间自动同步 """
        # StatusObject的属性修改不会即刻更新,所以这里是30s更新一次,一个恰当的频率
        def sub():
            while True:
                try:
                    time.sleep(self.__flush_time_interval)
                    self._share_dict = self.__mshd.get_all()

                    for key, value in self._share_dict.items():
                        self.__setattr__(key, value)

                    for user in [getattr(self._master.user, user_attr) for user_attr in dir(self._master.user) if not user_attr.startswith("_")]:
                        try:
                            user_name = user._name
                        except AttributeError:
                            # 这个异常可以过滤掉自身,因为自身中是没有_name属性的且该变化不用发送给自身
                            continue

                        self._master.send(user_name, ["CMD_STATUS_FLUSH", self._share_dict])
                        # print("send", user._name, ["CMD_SHARE_UPDATE", {attr:value}])

                except Exception as err:
                    self._master._log.log_info_format_err("Flush Err", "同步status错误!")
                    traceback.print_exc()
                    print(err)

        auto_flush_server_th = threading.Thread(target=sub)
        auto_flush_server_th.daemon = True
        auto_flush_server_th.start()

class MySelfObject(object):

    def __init__(self, master):
        self.share = ShareObject(master)
        self.status = StatusObject(master)

# ======================== 其他User使用 =========================
class OUSObject(object):
    """ Other User Share And Status Object """

    def __init__(self) -> None:
        self._share_dict = {}

    def __str__(self) -> str:
        return str(self._share_dict)

    def __repr__(self) -> str:
        return str(self._share_dict)

    def __getitem__(self, key):
        return self._share_dict[key]

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)

    def __iter__(self):
        return self._share_dict.__iter__()

    def _items_(self):
        return self._share_dict.items()

    def __setattr__(self, attr: str, value) -> None:
        """ set & modify"""
        # 保存变量
        super().__setattr__(attr, value)

        if not attr.startswith("_"):
            # 保存字典
            self._share_dict[attr] = value

    def __delattr__(self, name: str) -> None:
        """ del """
        # 删除变量
        try:
            super().__delattr__(name)
        except AttributeError:
            pass

        try:
            del self._share_dict[name]
        except KeyError:
            pass

# ========================== 普通类 ============================
class SendFile(object):
    def __init__(self, reve_user, source_file_path, remote_file_path, compress=None):
        # 常见压缩格式不进行数据流压缩
        self._no_compress_type_list = ['exe', '7z', 'zip', 'rar', 'iso', 'bz', 'bz2', 'gz', 'xz']

        self._uuid = uuid.uuid1()
        self.reve_user = reve_user
        self.source_file_path = source_file_path
        self.remote_file_path = remote_file_path
        self.md5 = ""
        self.len = 0
        self.statu = "waiting"
        self.percent = 0
        self._send_times = 0
        _, file_name = os.path.split(source_file_path)
        split_list = file_name.split(".")
        file_type = split_list[-1]
        self._file_type = file_type

        if compress == None:
            if self._file_type in self._no_compress_type_list:
                self._compress_flag = False
            else:
                self._compress_flag = True
        else:
            self._compress_flag = compress

class RecvFile(object):
    def __init__(self, send_user, source_file_path, remote_file_path, compress=None):
        # 常见压缩格式不进行数据流压缩
        self._no_compress_type_list = ['exe', '7z', 'zip', 'rar', 'iso', 'bz', 'bz2', 'gz', 'xz']

        self._uuid = uuid.uuid1()
        self.send_user = send_user
        self.source_file_path = source_file_path
        self.remote_file_path = remote_file_path
        self.md5 = ""
        self.len = 0
        self.statu = "waiting"
        self.percent = 0
        self._send_times = 0
        _, file_name = os.path.split(source_file_path)
        split_list = file_name.split(".")
        file_type = split_list[-1]
        self._file_type = file_type

        if compress == None:
            if self._file_type in self._no_compress_type_list:
                self._compress_flag = False
            else:
                self._compress_flag = True
        else:
            self._compress_flag = compress

class Node():

    def __init__(self, name, master):

        self._name  = name
        self._master = master

        self.share = OUSObject()
        self.status = OUSObject()

    def send(self, data):
        """
        文档:
            向其他集群节点发送数据

        参数:
            data : all type
                发送的数据,支持所有内建格式和第三方格式
        """

        self._master.send(self._name, ["CMD_SEND", data])

    def get(self, get_name, *args, timeout=60, **kwargs):
        """
        文档:
            向其他集群节点发送请求

        参数:
            get_name : str
                请求的名称,以此来区分不同的请求逻辑
            *args : all type
                位置参数, 任意数量, 任意类型
            **kwargs : all type
                关键字参数, 任意数量, 任意类型

        """

        uuid_id = uuid.uuid1()

        self._master._get_event_info_dict[uuid_id] = {
            "event" : threading.Event(),
        }

        self._master.send(self._name, ["CMD_GET", uuid_id, get_name, (args, kwargs)])

        self._master._get_event_info_dict[uuid_id]["event"].clear()
        if self._master._get_event_info_dict[uuid_id]["event"].wait(timeout):
            return self._master._get_event_info_dict[uuid_id]["result"]
        else:
            raise Exception("TimeoutError: {0} {1} timeout err!".format(get_name, timeout))

    def send_file(self, source_file_path, remote_file_path, show=False, compress=False, wait=False, uuid=None):
        """
        文档:
            向其他集群节点发送文件

        参数:
            source_file_path : str
                本机需要发送的文件路径
            remote_file_path : str
                对方接收文件的路径
            show : bool (default False)
                是否显示发送进度
            compress : bool (default False)
                是否压缩传输, 默认不压缩, 设置为None可以自动根据文件类型判断
            wait : bool (default False)
                是否等待文件传输完成后再返回, 此模式下如果md5校验失败会尝试重新发送一次

        返回:
            file_status_object : object
                reve_user : str
                    接收的用户名称
                source_file_path : str
                    本机需要发送的文件路径
                remote_file_path : str
                    对方接收文件的路径
                md5 : str
                    文件md5
                len : int
                    文件字节长度
                statu  : str
                    文件发送状态
                    waiting : 等待发送
                    sending : 发送中
                    waitmd5 : 等待MD5校验
                    success : 发送成功*
                    文件发送错误状态
                    md5err  : 发送完毕但md5错误*
                    timeout : 发送超时*
                    offline : 用户离线*
                percent : float
                    文件发送百分比
        """
        if not os.path.isfile(source_file_path):
            raise FileNotFoundError(source_file_path)

        send_file = SendFile(self._name, source_file_path, remote_file_path, compress)
        if uuid:
            send_file._uuid = uuid
        self._master._send_file_task_queue.put([send_file, show])

        if wait:
            time.sleep(0.1)
            while True:
                try:
                    # waiting & waitmd5
                    getattr(self._master.user, self._name)
                except AttributeError:
                    # 用户断线
                    self._master._log.log_info_format_err("Send Offline ERR", source_file_path)
                    send_file.statu = "offline"
                    return send_file

                if send_file.statu == "sending":
                    if time.time() - send_file._last_send_time > 30:
                        # 30s 都没有发送下一次, 可能网络断开了
                        self._master._log.log_info_format_err("Send Timeout ERR", source_file_path)
                        send_file.statu = "timeout"
                        return send_file
                elif send_file.statu == "success":
                    return send_file
                elif send_file.statu == "md5err":
                    self._master._log.log_info_format_err("Send MD5 ERR", source_file_path)
                    # 出错重试一次
                    new_send_file = self.send_file(source_file_path, remote_file_path, show=show, compress=compress, wait=False)
                    while True:
                        time.sleep(1)

                        try:
                            # waiting & waitmd5
                            getattr(self._master.user, self._name)
                        except AttributeError:
                            # 用户断线
                            self._master._log.log_info_format_err("Send Offline ERR", source_file_path)
                            new_send_file.statu = "offline"
                            return new_send_file

                        if new_send_file.statu == "sending":
                            if time.time() - new_send_file._last_send_time > 30:
                                # 30s 都没有发送下一次, 可能网络断开了
                                self._master._log.log_info_format_err("Send Timeout ERR", source_file_path)
                                new_send_file.statu = "timeout"
                                return new_send_file
                        elif new_send_file.statu == "success":
                            return new_send_file
                        elif new_send_file.statu == "md5err":
                            self._master._log.log_info_format_err("Send MD5 ERR R", source_file_path)
                            return new_send_file

                time.sleep(1)
        else:
            return send_file

    def recv_file(self, remote_file_path, source_file_path, show=False, compress=False, wait=False):
        """
        文档:
            向其他集群节点下载文件

        参数:
            remote_file_path : str
                对方发送文件的路径
            source_file_path : str
                本机需要接收的文件路径
            show : bool (default False)
                是否显示发送进度
            compress : bool (default False)
                是否压缩传输, 默认不压缩, 设置为None可以自动根据文件类型判断
            wait : bool (default False)
                是否等待文件传输完成后再返回, 此模式下如果md5校验失败会尝试接收发送一次

        返回:
            file_status_object : object
                send_user : str
                    发送的用户名称
                source_file_path : str
                    本机需要接收的文件路径
                remote_file_path : str
                    对方发送文件的路径
                md5 : str
                    文件md5
                len : int
                    文件字节长度
                statu  : str
                    文件接收状态
                    waiting : 等待接收
                    recving : 接收中
                    waitmd5 : 等待MD5校验
                    success : 接收成功*
                    文件接收错误状态
                    md5err  : 接收完毕但md5错误*
                    timeout : 接收超时*
                    offline : 用户离线*
                percent : float
                    文件发送百分比
        """
        r_uuid = uuid.uuid1()
        send_file = RecvFile(self._name, remote_file_path, source_file_path, compress=compress)
        send_file._uuid = r_uuid
        self._master._send_file_info_dict[send_file._uuid] = send_file
        self._master.send(self._name, ["CMD_RECV_FILE", remote_file_path, source_file_path, show, compress, r_uuid])

        if wait:
            time.sleep(0.1)
            while True:
                try:
                    # waiting & waitmd5
                    getattr(self._master.user, self._name)
                except AttributeError:
                    # 用户断线
                    self._master._log.log_info_format_err("Recv Offline ERR", source_file_path)
                    send_file.statu = "offline"
                    return send_file

                if send_file.statu == "recving":
                    if time.time() - send_file._last_recv_time > 30:
                        # 30s 都没有接收下一次, 可能网络断开了
                        self._master._log.log_info_format_err("Recv Timeout ERR", source_file_path)
                        send_file.statu = "timeout"
                        return send_file
                elif send_file.statu == "success":
                    return send_file
                elif send_file.statu == "md5err":
                    self._master._log.log_info_format_err("Recv MD5 ERR", source_file_path)
                    # 出错重试一次
                    new_send_file = self.recv_file(remote_file_path, source_file_path, show=show, compress=compress, wait=False)
                    while True:
                        time.sleep(1)

                        try:
                            # waiting & waitmd5
                            getattr(self._master.user, self._name)
                        except AttributeError:
                            # 用户断线
                            self._master._log.log_info_format_err("Recv Offline ERR", source_file_path)
                            new_send_file.statu = "offline"
                            return new_send_file

                        if new_send_file.statu == "recving":
                            if time.time() - new_send_file._last_recv_time > 30:
                                # 30s 都没有接收下一次, 可能网络断开了
                                self._master._log.log_info_format_err("Recv Timeout ERR", source_file_path)
                                new_send_file.statu = "timeout"
                                return new_send_file
                        elif new_send_file.statu == "success":
                            return new_send_file
                        elif new_send_file.statu == "md5err":
                            self._master._log.log_info_format_err("Recv MD5 ERR R", source_file_path)
                            return new_send_file

                time.sleep(1)
        else:
            return send_file

    def send_path(self, source_path, remote_path, show=True, compress=False, timeout=0):
        """
        文档:
            发送一个文件夹下所有文件, 若远程文件目录有对应文件则会跳过, 只发送改变的文件
            无法发送空文件夹

        参数:
            source_path : str
                需要发送的目录
            remote_path : str
                对方接收的目录
            show : bool (default False)
                是否显示发送进度
            compress : bool (default False)
                是否压缩传输, 默认不压缩, 设置为None可以自动根据文件类型判断
            timeout : int (default 0)
                超时,如果发送超时则抛出异常,默认不检测超时
        返回:
            all_task_list : list
                所有任务的列表,包含所有的 file_status_object
        """
        def _md5sum(file_path, blocksize=FILE_MD5_BLOCKSIZE):

            root_path, file_name = os.path.split(file_path)
            md5_info_path = os.path.join(root_path, ".md5")
            if not os.path.exists(md5_info_path):
                os.mkdir(md5_info_path)
            info_path = os.path.join(md5_info_path, file_name+".info")

            try:
                with open(info_path, "rb") as frb:
                    file_info = pickle.load(frb)

                last_mtime = os.path.getmtime(file_path)

                if last_mtime != file_info["mtime"]:
                    raise FileNotFoundError
                else:
                    return file_info["md5"]

            except FileNotFoundError:
                hash = hashlib.md5()
                with open(file_path, "rb") as fb:
                    while True:
                        block = fb.read(blocksize)
                        if not block:
                            break
                        hash.update(block)

                file_info = {
                    "mtime" : os.path.getmtime(file_path),
                    "md5"   : hash.hexdigest(),
                }

                with open(info_path, "wb") as fwb:
                    pickle.dump(file_info, fwb)

                return hash.hexdigest()

        def analysis_all_file_list(source_path, remote_path):

            def get_all_file(source_path, yes_root=''):
                """ 获取某个路径下不带根路径的文件列表 """
                all_file_list = []
                root = source_path
                for path in os.listdir(source_path):
                    join_path = os.path.join(root, path)
                    yes_path = os.path.join(yes_root, path)
                    if os.path.isdir(join_path):
                        # is path
                        all_file_list.extend(get_all_file(join_path, yes_root=yes_path))
                    else:
                        if ".md5" not in yes_path:
                            all_file_list.append(yes_path)

                return all_file_list

            all_file_list = get_all_file(source_path)

            all_file_info_list = []
            for file in all_file_list:
                all_file_info_list.append(
                    {
                        "source" : os.path.join(source_path, file),
                        "smd5"   : "",
                        "remote" : os.path.join(remote_path, file),
                        "rmd5"   : "",
                    }
                )

            return all_file_info_list

        start_time = time.time()
        if remote_path in ('', '.', '\\', '/'):
            raise ValueError("不允许使用根路径, 请至少指定一个文件夹!")
        if remote_path[:2] in ('c:' 'C:'):
            raise ValueError("不允许发送到系统目录!")

        all_file_info_list = analysis_all_file_list(source_path, remote_path)
        for file_info_dict in all_file_info_list:
            file_info_dict["smd5"] = _md5sum(file_info_dict["source"])

        task_uuid = uuid.uuid1()
        self._master._send_path_task_dict[task_uuid] = {}
        self._master._send_path_task_dict[task_uuid]['event'] = threading.Event()
        self._master._send_path_task_dict[task_uuid]['event'].clear()

        self._master.send(self._name, ["CMD_SRND_PATH", all_file_info_list, remote_path, task_uuid])

        self._master._send_path_task_dict[task_uuid]['event'].wait()

        all_file_info_list = self._master._send_path_task_dict[task_uuid]['all_file_info_list']

        all_task_list = []
        for file_info_dict in all_file_info_list:
            if file_info_dict["smd5"] != file_info_dict["rmd5"]:

                if timeout:
                    if time.time() - start_time > timeout:
                        raise RuntimeError("send_path Timeout Err!")

                # 使用 wait=True 防止网络流速度大于硬盘流导致客户端内存被占满
                if os.path.getsize(file_info_dict["source"]) < 5242880:
                    # 文件大小小于5M不用等待Md5
                    send_file = self.send_file(file_info_dict["source"], file_info_dict["remote"], show=show, compress=compress, wait=False)
                else:
                    # 大文件等待发送,如果md5错误会重新发送一次
                    send_file = self.send_file(file_info_dict["source"], file_info_dict["remote"], show=show, compress=compress, wait=True)
                all_task_list.append(send_file)
            else:
                print("Skip same file: {0}".format(file_info_dict["source"]))

        while True:
            time.sleep(3)
            if timeout:
                if time.time() - start_time > timeout:
                    raise RuntimeError("send_path Timeout Err!")
            all_down_flag = True
            err_flag = False
            for send_file in all_task_list:

                if send_file.statu == "waiting":
                    try:
                        # waiting & waitmd5
                        getattr(self._master.user, self._name)
                    except AttributeError:
                        # 用户断线
                        self._master._log.log_info_format_err("Send Offline ERR", send_file.source_file_path)
                        send_file.statu = "offline"
                    all_down_flag = False
                elif send_file.statu == "sending":
                    if time.time() - send_file._last_send_time > 30:
                        # 30s 都没有发送下一次, 可能网络断开了
                        self._master._log.log_info_format_err("Send Timeout ERR", send_file.source_file_path)
                        send_file.statu = "timeout"
                    all_down_flag = False
                elif send_file.statu == "waitmd5":
                    try:
                        # waiting & waitmd5
                        getattr(self._master.user, self._name)
                    except AttributeError:
                        # 用户断线
                        self._master._log.log_info_format_err("Send Offline ERR", send_file.source_file_path)
                        send_file.statu = "offline"
                    all_down_flag = False
                elif send_file.statu == "success":
                    pass
                elif send_file.statu == "md5err":
                    # 重新发送
                    new_send_file = self.send_file(send_file.source_file_path, send_file.remote_file_path, show=show, compress=compress, wait=True)
                    if new_send_file.statu == "md5err":
                        # 重新发送还是md5错误
                        send_file.statu = "md5err2"
                    else:
                        send_file.statu = new_send_file.statu
                elif send_file.statu == "md5err2":
                    err_flag = True
                elif send_file.statu == "timeout":
                    err_flag = True
                elif send_file.statu == "offline":
                    err_flag = True

            if all_down_flag:
                break

        if err_flag:
            raise RuntimeError("send_path Err!")

        return all_task_list

class Server():

    def __init__(self, ip, port, password="abc123", log=None, user_napw_info=None, blacklist=None, encryption=True, gui_log_information=None):
        """
        文档:
            建立一个服务端

        参数:
            ip : str
                建立服务的IP地址
            port : int
                端口
            password : str
                密码
            log : None or str
                日志等级
                    None: 除了错误什么都不显示
                    "INFO": 显示基本连接信息
                    "DEBUG": 显示所有信息
            user_napw_info : dict(default {})
                用户加密密码信息字典, 设定后只有使用正确的用户名和密码才能登录服务端
                不指定跳过用户真实性检测
                使用 hash_encryption 函数生成需要的 user_napw_info
            blacklist : list(default [])
                ip黑名单, 在这个列表中的ip无法连接服务端
            encryption : bool(default True)
                是否加密传输, 不加密效率较高

        例子:
            # Server
            server = Server("127.0.0.1", 12345, password="abc123", log="INFO",
                    # user_napw_info={
                    #     "Foo" : b'$2b$15$DFdThRBMcnv/doCGNa.W2.wvhGpJevxGDjV10QouNf1QGbXw8XWHi',
                    #     "Bar" : b'$2b$15$DFdThRBMcnv/doCGNa.W2.wvhGpJevxGDjV10QouNf1QGbXw8XWHi',
                    #     },
                    # blacklist = ["192.168.0.10"],
                    )

            # 运行默认的回调函数(所有接受到的信息都在self.recv_info_queue队列里,需要用户手动实现回调函数并使用)
            # 默认的回调函数只打印信息
            server.default_callback_server()
        """
        self.ip = ip
        self.port = port
        self.password = password

        self.encryption = encryption

        if not blacklist:
            self.blacklist = []
        else:
            self.blacklist = blacklist

        self.user = User()
        # 在用户对象里保存自己
        self.user.myself = MySelfObject(self)

        self._send_lock = threading.Lock()

        # {"Alice" : b'$2b$15$DFdThRBMcnv/doCGNa.W2.wvhGpJevxGDjV10QouNf1QGbXw8XWHi'}
        if not user_napw_info:
            self.user_napw_info = {}
        else:
            self.user_napw_info = user_napw_info

        self.recv_info_queue = queue.Queue()

        self._send_file_task_queue = queue.Queue()

        self._recv_file_task_queue = queue.Queue()

        self._recv_path_task_queue = queue.Queue()

        self._send_path_task_dict = {}

        self._get_event_info_dict = {}

        self._recv_get_info_queue = queue.Queue()

        self._get_callback_func_dict = {}

        self._log = Log(log, gui_log_information)

        self._encrypt_rsa = encrypt_rsa()
        self._encrypt_aes = encrypt_aes()

        self._user_dict = {}

        self._send_file_info_dict = {}

        self._send_file_user_lock_dict = {}

        self.ip_err_times_dict = {}

        self.is_encryption_dict = {}

        self.user_addr_dict = {}

        self._connect_timeout_sock_set = set()

        self._init_conncet()

        self._connect_timeout_server()

        self._get_event_callback_server()

        self._send_file_server()

        self._recv_file_server()

        self._recv_path_server()

    def _init_conncet(self):

        def sub():
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._sock.bind((self.ip, self.port))
            self._sock.listen(99)

            self.port = self._sock.getsockname()[1]

            self._log.log_info_format("Sucess", "等待用户连接..")
            while True:
                try:
                    sock, addr = self._sock.accept()
                    tcplink_th = threading.Thread(target=self._tcplink, args=(sock, addr))
                    tcplink_th.daemon = True
                    tcplink_th.start()
                except Exception as err:
                    print("@NOW: @612{0}".cformat("运行用户线程错误!"))
                    traceback.print_exc()
                    print(err)

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _tcplink(self, sock, addr):

        if addr[0] in self.blacklist:
            self._blacklist(sock, addr)
            return

        self._connect_timeout_sock_set.add(sock)

        self._log.log_info_format("Connect", addr)

        try:
            client_pubkey = self._recv_fun_s(sock)
        except:
            self._ip_err_callback(addr)
            sock.close()
            return

        # NOTE 两用户加密 一用户不加密 加密的自动兼容不加密的 下面的为每个用户保存是否加密字典不能少
        # 每次都得判断 损失一点点性能
        if client_pubkey == "NOT_ENCRYPTION" or not self.encryption:
            # 如果客户端不加密,那么服务端不加密
            # 如果服务端不加密,客户端也不加密
            self._send_fun_s(sock, "NOT_ENCRYPTION")
            client_name, client_password = self._recv_fun_s(sock)
            self._log.log_info_warning_format("WARNING", "NOT_ENCRYPTION")
            self.is_encryption_dict[client_name] = False
        else:
            self._send_fun_s(sock, self._encrypt_rsa.pubkey)
            client_name, client_password = self._recv_fun_encrypt_s(sock)
            self.is_encryption_dict[client_name] = True

        try:
            self._user_dict[client_name]
            self._log.log_info_format_err("client name repeat", client_name)
            sock.close()
            return
        except KeyError:
            self._user_dict[client_name] = {}
            self._user_dict[client_name]["sock"] = sock
            self._user_dict[client_name]["pubkey"] = client_pubkey
            setattr(self.user, client_name, Node(client_name, self))

        password = self._recv_fun_encrypt(client_name)
        if password != self.password:
            self._log.log_info_format_err("Verified failed", client_name)
            self._password_err(client_name)
            self._ip_err_callback(addr)
            return
        else:
            self._log.log_info_format("Verified successfully", client_name)
            self._password_correct(client_name)

        if self.user_napw_info:
            hashed = self.user_napw_info.get(client_name, False)
            if hashed:
                ret = bcrypt.checkpw(client_password.encode(), hashed)
                if not ret:
                    self._log.log_info_format_err("Login failed", client_name)
                    self._log.log_debug_format_err("_tcplink", "User password is wrong!")
                    self._login_err(client_name)
                    self._ip_err_callback(addr)
                    return
            else:
                self._log.log_info_format_err("Login failed", client_name)
                self._log.log_debug_format_err("_tcplink", "User does not exist!")
                self._login_err(client_name)
                self._ip_err_callback(addr)
                return
        else:
            self._log.log_debug_format("_tcplink", "Client information is not set! Use user_napw_info to set!")

        self._log.log_info_format("Login successfully", client_name)
        self._login_correct(client_name)
        self._connect_timeout_sock_set.remove(sock)
        self._send_fun_encrypt(client_name, (self._encrypt_aes.key, self._encrypt_aes.iv))
        aes_key, aes_iv = self._recv_fun_encrypt(client_name)
        self._user_dict[client_name]["aes_key"] = aes_key
        self._user_dict[client_name]["aes_iv"] = aes_iv
        self._connect_end()

        self.user_addr_dict[client_name] = addr

        while True:
            try:
                recv_data = self._recv_fun_encrypt_fast(client_name)
                # print(recv_data)
            except (ConnectionRefusedError, ConnectionResetError, TimeoutError, ConnectionAbortedError) as err:
                self._log.log_info_format_err("Offline", "{0} {1}".format(client_name, err))
                try:
                    self._disconnect_user_fun(client_name)
                except Exception as err:
                    traceback.print_exc()
                    print(err)
                break
            except Exception as err:
                print("@NOW: @612{0}".cformat("捕获到连接未知错误:"))
                traceback.print_exc()
                print(err)
                self._log.log_info_format_err("Offline", "{0} {1}".format(client_name, err))
                try:
                    self._disconnect_user_fun()
                except Exception as err:
                    traceback.print_exc()
                    print(err)
                break

            try:
                cmd = recv_data[0]
                if cmd == "CMD_SEND":
                    # send ["CMD_SEND", data]
                    self.recv_info_queue.put([client_name, recv_data[1]])
                elif cmd == "CMD_GET":
                    # process ["CMD_GET", uuid_id, get_name, (args, kwargs)]
                    self._recv_get_info_queue.put([client_name, recv_data])
                elif cmd == "CMD_REGET":
                    # get result ["CMD_REGET", uuid_id, result_data]
                    self._get_event_info_dict[recv_data[1]]["result"] = recv_data[2]
                    self._get_event_info_dict[recv_data[1]]["event"].set()
                elif cmd == "CMD_SHARE_UPDATE":
                    # ["CMD_SHARE_UPDATE", {attr:value}]
                    update_share_dict = recv_data[1]
                    get_user = getattr(self.user, client_name)
                    get_user.share._share_dict.update(update_share_dict)
                    for name, value in update_share_dict.items():
                        setattr(get_user.share, name, value)
                elif cmd == "CMD_SHARE_DEL":
                    # ["CMD_SHARE_DEL", name]
                    name = recv_data[1]
                    get_user = getattr(self.user, client_name)
                    del get_user.share._share_dict[name]
                    delattr(get_user.share, name)
                elif cmd == "CMD_SHARE_FLUSH":
                    # ["CMD_SHARE_FLUSH", self._share_dict]
                    share_dict = recv_data[1]
                    get_user = getattr(self.user, client_name)
                    # 更新变量
                    get_user.share._share_dict.update(share_dict)
                    for name, value in share_dict.items():
                        setattr(get_user.share, name, value)
                    # 删除多余变量
                    for del_key in get_user.share._share_dict.keys() - share_dict.keys():
                        del get_user.share._share_dict[del_key]
                        delattr(get_user.share, del_key)
                elif cmd == "CMD_STATUS_FLUSH":
                    # ["CMD_STATUS_FLUSH", self._share_dict]
                    status_dict = recv_data[1]
                    get_user = getattr(self.user, client_name)
                    # 更新变量
                    get_user.status._share_dict.update(status_dict)
                    for name, value in status_dict.items():
                        setattr(get_user.status, name, value)
                    # 删除多余变量
                    for del_key in get_user.status._share_dict.keys() - status_dict.keys():
                        del get_user.status._share_dict[del_key]
                        delattr(get_user.status, del_key)
                elif cmd == "CMD_SEND_FILE":
                    # ["CMD_SEND_FILE", xxx, xx, xx]
                    self._recv_file_task_queue.put((client_name, recv_data))
                elif cmd == "CMD_ERCV_FILE_MD5":
                    # ['CMD_ERCV_FILE_MD5', "FILE_RECV_MD5", UUID('d6fbf782-0404-11ed-8912-68545ad0c824'), '9234cf4bffbd28432965c322c]
                    self._recv_file_task_queue.put((client_name, recv_data))
                elif cmd == "CMD_RECV_FILE":
                    # ["CMD_RECV_FILE", remote_file_path, source_file_path, show, compress, uuid] server_name
                    user_obj = getattr(self.user, client_name)
                    user_obj.send_file(recv_data[1], recv_data[2], show=recv_data[3], compress=recv_data[4], uuid=recv_data[5])
                elif cmd == "CMD_SRND_PATH":
                    # ["CMD_SRND_PATH", all_file_info_list, remote_path, task_uuid]
                    self._recv_path_task_queue.put((recv_data[1], recv_data[2], client_name, recv_data[3]))
                elif cmd == "CMD_RECV_PATH":
                    # ["CMD_RECV_PATH", task_uuid, all_file_info_list]
                    self._send_path_task_dict[recv_data[1]]['all_file_info_list'] = recv_data[2]
                    self._send_path_task_dict[recv_data[1]]['event'].set()
                else:
                    self._log.log_info_format_err("Format Err", "收到 {0} 错误格式数据: {1}".format(client_name, recv_data))
            except Exception as err:
                self._log.log_info_format_err("Runtime Err", "Server处理数据错误!")
                traceback.print_exc()
                print(err)

    def _default_get_event_callback_func(self, data):
        return ["Undefined", data]

    def register_get_event_callback_func(self, get_name, func):
        self._get_callback_func_dict[get_name] = func

    def _get_event_callback_server(self):
        def server():

            def do_user_func_th(client_name, callback_func, data, uuid_id):
                try:
                    # data : (*args, **kwargs)
                    result = callback_func(*data[0], **data[1])
                    self.send(client_name, ["CMD_REGET", uuid_id, result])
                except Exception as err:
                    print("@NOW: @612{0}".cformat("Client 处理get任务线程错误!"))
                    traceback.print_exc()
                    print(err)

            while True:
                try:
                    # client_name, ["CMD_GET", uuid_id, get_name, (args, kwargs)]
                    client_name, recv_data = self._recv_get_info_queue.get()
                    _, uuid_id, get_name, data = recv_data

                    try:
                        callback_func = self._get_callback_func_dict[get_name]

                        # 并发处理get请求
                        sub_th = threading.Thread(target=do_user_func_th, args=(client_name, callback_func, data, uuid_id))
                        sub_th.daemon = True
                        sub_th.start()

                    except KeyError:
                        result = self._default_get_event_callback_func(data)
                        self.send(client_name, ["CMD_REGET", uuid_id, result])
                except Exception as err:
                    print("@NOW: @612{0}".cformat("Client 处理get任务错误!"))
                    traceback.print_exc()
                    print(err)

        server_th = threading.Thread(target=server)
        server_th.daemon = True
        server_th.start()

    def _disconnect_user_fun(self, *args, **kwargs):
        pass

    def _register_disconnect_user_fun(self, disconnect_user_fun):

        self._disconnect_user_fun = disconnect_user_fun

    def _ip_err_callback(self, addr):

        self._log.log_info_format_err("IP Err", addr)
        ip = addr[0]
        try:
            self.ip_err_times_dict[ip] += 1
        except KeyError:
            self.ip_err_times_dict[ip] = 1

        if self.ip_err_times_dict[ip] >= 3:
            self.blacklist.append(ip)

    def default_callback_server(self):
        def sub():
            while True:
                from_user, recv_data = self.recv_info_queue.get()
                print("{0} from {1} recv: {2}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), from_user, recv_data))

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _connect_timeout_server(self):

        def sub():
            # 无论是否已经断开了都会再次断开次
            old_check_time_dict = {}
            while True:
                time.sleep(10)
                remove_sock_list = []
                for sock in self._connect_timeout_sock_set:
                    try:
                        old_check_time = old_check_time_dict[sock]
                    except KeyError:
                        old_check_time = old_check_time_dict[sock] = time.time()

                    if time.time() - old_check_time >= 15:
                        self._log.log_info_warning_format("WARNING", "timeout sock close: {0}".format(sock))
                        sock.close()
                        remove_sock_list.append(sock)

                for sock in remove_sock_list:
                    self._connect_timeout_sock_set.remove(sock)
                    del old_check_time_dict[sock]

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _connect_end(self):
        self._log.log_debug_format("_connect_end", "connect_end")

    def _disconnect(self, client_name):
        self._log.log_debug_format_err("_disconnect", "disconnect")
        self._user_dict[client_name]["sock"].close()
        del self._user_dict[client_name]
        delattr(self.user, client_name)

    def _password_err(self, client_name):
        self._log.log_debug_format_err("_password_err", "password_err")
        self._send_fun_encrypt(client_name, "t%fgDYJdI35NJKS")
        self._user_dict[client_name]["sock"].close()
        del self._user_dict[client_name]
        delattr(self.user, client_name)

    def _password_correct(self, client_name):
        self._log.log_debug_format("_password_correct", "password_correct")
        self._send_fun_encrypt(client_name, "YES")

    def _login_err(self, client_name):
        self._log.log_debug_format_err("_login_err", "login_err")
        self._send_fun_encrypt(client_name, "Jif43DF$dsg")
        self._user_dict[client_name]["sock"].close()
        del self._user_dict[client_name]
        delattr(self.user, client_name)

    def _login_correct(self, client_name):
        self._log.log_debug_format("_login_correct", "login_correct")
        self._send_fun_encrypt(client_name, "YES")

    def _blacklist(self, sock, addr):
        self._log.log_info_format_err("Blacklist Ban", addr)
        self._log.log_debug_format_err("_blacklist", "blacklist")
        sock.close()

    def _recv_fun_s(self, sock):
        try:
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            # data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._log.log_debug_format_err("_recv_fun_s", "disconnect")
            sock.close()
            raise err

    def _send_fun_s(self, sock, data):
        try:
            ds = pickle.dumps(data)

            len_n = '{:17}'.format(len(ds)).encode()

            # 全部一起发送
            sock.sendall(len_n + ds)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._log.log_debug_format_err("_send_fun_s", "disconnect")
            sock.close()
            raise err

    def _recv_fun_encrypt_s(self, sock):
        try:
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            if data_type != b'F':
                data_bytes = self._encrypt_rsa.decrypt(data_bytes)
            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._log.log_debug_format_err("_recv_fun_encrypt_s", "disconnect")
            sock.close()
            raise err

    def _send_fun_encrypt_s(self, sock, data):
        # NOTE 这个函数现在暂时未使用,如果使用要考虑到为加密端对加密端的兼容问题
        try:
            ds = pickle.dumps(data)

            ds = self._encrypt_rsa.encrypt_user(ds, self._user_dict[sock]["pubkey"])

            len_n = '{:17}'.format(len(ds)).encode()

            encrypt_data = len_n + ds
            # 全部一起发送
            sock.sendall(encrypt_data)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._log.log_debug_format_err("_send_fun_encrypt_s", "disconnect")
            sock.close()
            raise err

    def _recv_fun(self, client_name):
        try:
            sock = self._user_dict[client_name]["sock"]
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            # data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(client_name)
            raise err

    def _send_fun(self, client_name, data):
        try:
            sock = self._user_dict[client_name]["sock"]
            ds = pickle.dumps(data)

            len_n = '{:17}'.format(len(ds)).encode()

            # 全部一起发送
            sock.sendall(len_n + ds)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(client_name)
            raise err

    def _recv_fun_encrypt(self, client_name):
        try:
            sock = self._user_dict[client_name]["sock"]
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            if self.is_encryption_dict[client_name] and data_type != b'F':
                data_bytes = self._encrypt_rsa.decrypt(data_bytes)
            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            # traceback.print_exc()
            # print(err)
            self._disconnect(client_name)
            raise err

    def _send_fun_encrypt(self, client_name, data):
        try:
            sock = self._user_dict[client_name]["sock"]
            ds = pickle.dumps(data)

            if self.is_encryption_dict[client_name]:
                ds = self._encrypt_rsa.encrypt_user(ds, self._user_dict[client_name]["pubkey"])

            len_n = '{:17}'.format(len(ds)).encode()

            encrypt_data = len_n + ds
            # 全部一起发送
            sock.sendall(encrypt_data)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(client_name)
            raise err

    def _recv_fun_encrypt_fast(self, client_name):
        try:
            sock = self._user_dict[client_name]["sock"]
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            if self.is_encryption_dict[client_name] and data_type != b'F':
                data_bytes = self._encrypt_aes.decrypt(data_bytes)
            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            # traceback.print_exc()
            # print(err)
            self._disconnect(client_name)
            raise err

    def _send_fun_encrypt_fast(self, client_name, data):
        try:
            sock = self._user_dict[client_name]["sock"]
            ds = pickle.dumps(data)

            if self.is_encryption_dict[client_name]:
                ds = self._encrypt_aes.encrypt_user(ds, self._user_dict[client_name]["aes_key"], self._user_dict[client_name]["aes_iv"])

            len_n = '{:17}'.format(len(ds)).encode()

            encrypt_data = len_n + ds
            # 全部一起发送
            sock.sendall(encrypt_data)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(client_name)
            raise err

    def send(self, client_name, data):

        self._send_fun_encrypt_fast(client_name, data)

        # self._send_lock.acquire()
        # try:
        #     self._send_fun_encrypt(client_name, data)
        # finally:
        #     self._send_lock.release()
        pass

    def _md5sum(self, file_path, blocksize=FILE_MD5_BLOCKSIZE):
        root_path, file_name = os.path.split(file_path)
        md5_info_path = os.path.join(root_path, ".md5")
        if not os.path.exists(md5_info_path):
            os.mkdir(md5_info_path)
        info_path = os.path.join(md5_info_path, file_name+".info")

        try:
            with open(info_path, "rb") as frb:
                file_info = pickle.load(frb)

            last_mtime = os.path.getmtime(file_path)

            if last_mtime != file_info["mtime"]:
                raise FileNotFoundError
            else:
                return file_info["md5"]

        except FileNotFoundError:
            hash = hashlib.md5()
            with open(file_path, "rb") as fb:
                while True:
                    block = fb.read(blocksize)
                    if not block:
                        break
                    hash.update(block)

            file_info = {
                "mtime" : os.path.getmtime(file_path),
                "md5"   : hash.hexdigest(),
            }

            with open(info_path, "wb") as fwb:
                pickle.dump(file_info, fwb)

            return hash.hexdigest()

    def _send_file_server(self):
        def sub():

            def get_file_size_str(file_size):
                file_size = file_size / 1024
                if file_size < 1000:
                    return "{0:.2f}K".format(file_size)
                else:
                    file_size = file_size / 1024
                    if file_size < 1000:
                        return "{0:.2f}MB".format(file_size)
                    else:
                        file_size = file_size / 1024
                        return "{0:.2f}GB".format(file_size)

            def compress_fun(send_buff):
                return zlib.compress(send_buff)

            def no_compress_fun(send_buff):
                return send_buff

            def send_file_th_server(send_file, show):
                """ 发送文件线程 """
                reve_user = send_file.reve_user
                try:
                    user_lock = self._send_file_user_lock_dict[reve_user]
                except KeyError:
                    user_lock = threading.Lock()
                    self._send_file_user_lock_dict[reve_user] = user_lock

                user_lock.acquire()
                try:
                    self._send_file_info_dict[send_file._uuid] = send_file

                    source_file_path = send_file.source_file_path
                    remote_file_path = send_file.remote_file_path

                    # 计算MD5
                    send_file.statu = "calcumd5"
                    send_file.len = os.path.getsize(source_file_path)
                    send_file.md5 = self._md5sum(source_file_path)

                    # 发送文件
                    send_file._last_send_time = time.time()
                    send_file.statu = "sending"
                    # 发送文件流次数
                    send_times = int((send_file.len / FILE_SEND_BUFFER_SIZE) + 2)
                    send_file._send_times = send_times
                    # 发送文件对象信息
                    self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_INFO", send_file._uuid, send_file.reve_user, source_file_path, remote_file_path, \
                        send_file._compress_flag, send_times, send_file.len, send_file.md5, show])

                    if send_file._compress_flag:
                        used_compress_fun = compress_fun
                    else:
                        used_compress_fun = no_compress_fun

                    FILE_LOG_LOCK.acquire()
                    try:
                        with open(FILE_LOG_FILE_PATH, "a", encoding="utf-8") as fa:
                            fa.write("{0}: Send to {1} {2}\n".format(
                            time.strftime('%Y-%m-%d %H:%M:%S'),
                            reve_user,
                            source_file_path,
                            ))
                    finally:
                        FILE_LOG_LOCK.release()
                    if show:
                        with open(source_file_path, "rb") as frb:
                            file_name = source_file_path
                            if len(source_file_path) > 50:
                                file_name = "..." + source_file_path[-45:]
                            title="Send: {0} {1} to {2}".format(file_name, get_file_size_str(send_file.len), reve_user)
                            for index in tqdm(range(send_times), desc=title):
                                send_buff = frb.read(FILE_SEND_BUFFER_SIZE)
                                # 注释掉这段是让发送方和接收方发送和接收的数据量一样多
                                # if send_buff == b'':
                                #     send_file.percent = 1
                                #     continue
                                send_buff = used_compress_fun(send_buff)
                                self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_BUFF", send_file._uuid, send_buff])
                                send_file._last_send_time = time.time()
                                send_file.percent = index / send_times
                            send_file.percent = 1
                    else:
                        with open(source_file_path, "rb") as frb:
                            for index in range(send_times):
                                send_buff = frb.read(FILE_SEND_BUFFER_SIZE)
                                # if send_buff == b'':
                                #     send_file.percent = 1
                                #     continue
                                send_buff = used_compress_fun(send_buff)
                                self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_BUFF", send_file._uuid, send_buff])
                                send_file._last_send_time = time.time()
                                send_file.percent = index / send_times

                    # 发送接收完毕
                    self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_END", send_file._uuid])

                    send_file.statu = "waitmd5"
                except Exception as err:
                    self._log.log_info_format_err("Send File TH", "发送文件数据流错误!")
                    traceback.print_exc()
                    print(err)
                finally:
                    user_lock.release()

            while True:
                try:
                    send_file, show = self._send_file_task_queue.get()

                    send_file_th = threading.Thread(target=send_file_th_server, args=(send_file, show))
                    send_file_th.daemon = True
                    send_file_th.start()
                except Exception as err:
                    self._log.log_info_format_err("Send File", "发送文件数据流错误!")
                    traceback.print_exc()
                    print(err)

        send_file_server_th = threading.Thread(target=sub)
        send_file_server_th.daemon = True
        send_file_server_th.start()

    def _recv_file_server(self):
        """ 接收_send_file_server服务发送过来的文件流 """
        def sub():

            def get_file_size_str(file_size):
                file_size = file_size / 1024
                if file_size < 1000:
                    return "{0:.2f}K".format(file_size)
                else:
                    file_size = file_size / 1024
                    if file_size < 1000:
                        return "{0:.2f}MB".format(file_size)
                    else:
                        file_size = file_size / 1024
                        return "{0:.2f}GB".format(file_size)

            def de_compress_fun(file_buff):
                return zlib.decompress(file_buff)

            def no_de_compress_fun(file_buff):
                return file_buff

            def alive_bar_th(send_file, send_user_name, bar_queue, show):
                if show:
                    file_name = send_file.remote_file_path
                    if len(send_file.remote_file_path) > 50:
                        file_name = "..." + send_file.remote_file_path[-45:]
                    title="Recv: {0} {1} from {2}".format(file_name, get_file_size_str(send_file.len), send_user_name)
                    send_times = send_file._send_times
                    for index in tqdm(range(send_times), desc=title):
                        bar_queue.get()
                        send_file.percent = index / send_times
                    send_file.percent = 1
                else:
                    send_times = send_file._send_times
                    for index in range(send_times):
                        bar_queue.get()
                        send_file.percent = index / send_times
                    send_file.percent = 1

            while True:
                try:
                    send_user_name, file_data = self._recv_file_task_queue.get()
                    file_cmd = file_data[1]
                    if file_cmd == "FILE_INFO":
                        # ['CMD_SEND_FILE', 'FILE_INFO', uuid, name, source_file_path, remote_file_path, _compress_flag, send_times, len, md5, show]
                        try:
                            send_file = self._send_file_info_dict[file_data[2]]
                        except KeyError:
                            send_file = RecvFile(file_data[3], file_data[4], file_data[5], file_data[6])
                        send_file._send_times = file_data[7]
                        send_file._source_md5 = file_data[9]
                        send_file.len = file_data[8]
                        # 保存进度条
                        send_file._bar_queue = queue.Queue()

                        alive_bar_th_th = threading.Thread(target=alive_bar_th, args=(send_file, send_user_name, send_file._bar_queue, file_data[10]))
                        alive_bar_th_th.daemon = True
                        alive_bar_th_th.start()

                        if send_file._compress_flag:
                            send_file._used_de_compress_fun = de_compress_fun
                        else:
                            send_file._used_de_compress_fun = no_de_compress_fun
                        send_file._uuid = file_data[2]
                        self._send_file_info_dict[send_file._uuid] = send_file
                        # 检查路径,若文件存在就删除(覆盖),若路径不存在就新建
                        remote_file_path = file_data[5]
                        # if os.path.isfile(remote_file_path):
                        #     os.remove(remote_file_path)
                        if os.path.isfile(remote_file_path + '.crf'):
                            os.remove(remote_file_path + '.crf')
                        path, _ = os.path.split(remote_file_path)
                        if not os.path.isdir(path):
                            if path:
                                os.makedirs(path)
                        send_file._last_recv_time = time.time()
                        send_file.statu = "recving"

                        FILE_LOG_LOCK.acquire()
                        try:
                            with open(FILE_LOG_FILE_PATH, "a", encoding="utf-8") as fa:
                                fa.write("{0}: Recv from {1} {2}\n".format(
                                    time.strftime('%Y-%m-%d %H:%M:%S'),
                                    send_user_name,
                                    remote_file_path,
                                ))
                        finally:
                            FILE_LOG_LOCK.release()
                    elif file_cmd == "FILE_BUFF":
                        # ['CMD_SEND_FILE', 'FILE_BUFF', UUID('3ec7e3ac-03f7-11ed-a13e-68545ad0c824'), b'\xff\xd8\xff\xe1\x12\xc8Exif\x00\x00MM\x00*\]
                        file_uuid = file_data[2]
                        file_buff = file_data[3]
                        send_file = self._send_file_info_dict[file_uuid]
                        remote_file_path = send_file.remote_file_path
                        # 追加数据进文件
                        file_buff = send_file._used_de_compress_fun(file_buff)
                        for index in range(1, 4):
                            try:
                                with open(remote_file_path + '.crf', "ab") as fab:
                                    fab.write(file_buff)
                                break
                            except PermissionError:
                                # permission denied
                                print("permission denied: Re Try.")
                                time.sleep(1 * index)
                        send_file._last_recv_time = time.time()
                        send_file._bar_queue.put(True)
                    elif file_cmd == "FILE_END":
                        # ['CMD_SEND_FILE', 'FILE_END', UUID('5302e4ee-03f7-11ed-8a81-68545ad0c824')]
                        send_file.statu = "waitmd5"
                        file_uuid = file_data[2]
                        send_file = self._send_file_info_dict[file_uuid]
                        remote_file_path = send_file.remote_file_path
                        # 计算文件MD5
                        remote_file_md5 = self._md5sum(remote_file_path + '.crf')
                        send_file.md5 = remote_file_md5
                        if send_file._source_md5 == remote_file_md5:
                            if os.path.isfile(remote_file_path):
                                os.remove(remote_file_path)
                            # 复原文件名
                            os.rename(remote_file_path + '.crf', remote_file_path)
                            send_file.statu = "success"
                        else:
                            send_file.statu = "md5err"
                        # 发送给对方md5
                        self.send(send_user_name, ["CMD_ERCV_FILE_MD5", "FILE_RECV_MD5", send_file._uuid, remote_file_md5])
                    elif file_cmd == "FILE_RECV_MD5":
                        # ['CMD_ERCV_FILE_MD5', "FILE_RECV_MD5", UUID('d6fbf782-0404-11ed-8912-68545ad0c824'), '9234cf4bffbd28432965c322c]
                        file_uuid = file_data[2]
                        send_file = self._send_file_info_dict[file_uuid]
                        if send_file.md5 ==  file_data[3]:
                            send_file.statu = "success"
                        else:
                            self._log.log_info_format_err("Recv File", "接收端文件数据MD5错误! {0}".format(send_file.source_file_path))
                            send_file.statu = "md5err"
                except Exception as err:
                    self._log.log_info_format_err("Recv File", "接收文件数据流错误!")
                    traceback.print_exc()
                    print(err)

        recv_file_server_th = threading.Thread(target=sub)
        recv_file_server_th.daemon = True
        recv_file_server_th.start()

    def _recv_path_server(self):
        """ 接收目录文件服务线程 """
        def sub():

            def getAllFiles(folder):
                """ 获取某个路径全文件 """
                filepath_list = []
                for root, folder_names, file_names in os.walk(folder):
                    for file_name in file_names:
                        file_path = os.path.join(root, file_name)
                        filepath_list.append(file_path)
                        # print(file_path)
                return filepath_list

            def del_emp_dir(path):
                """ 删除空文件夹 """
                # 这个函数对空文件夹下的空文件夹每次调用只能删除一个,需要多次调用
                for (root, dirs, files) in os.walk(path):
                    for item in dirs:
                        dir = os.path.join(root, item)
                        try:
                            os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
                            print("Remove empty folder: {0}".format(dir))
                        except Exception:
                            pass

                for (root, dirs, files) in os.walk(path):
                    for item in dirs:
                        dir = os.path.join(root, item)
                        try:
                            os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
                            print("Remove empty folder: {0}".format(dir))
                        except Exception:
                            pass

                for (root, dirs, files) in os.walk(path):
                    for item in dirs:
                        dir = os.path.join(root, item)
                        try:
                            os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
                            print("Remove empty folder: {0}".format(dir))
                        except Exception:
                            pass

            def _md5sum(file_path, blocksize=FILE_MD5_BLOCKSIZE):
                root_path, file_name = os.path.split(file_path)
                md5_info_path = os.path.join(root_path, ".md5")
                if not os.path.exists(md5_info_path):
                    os.mkdir(md5_info_path)
                info_path = os.path.join(md5_info_path, file_name+".info")

                try:
                    with open(info_path, "rb") as frb:
                        file_info = pickle.load(frb)

                    last_mtime = os.path.getmtime(file_path)

                    if last_mtime != file_info["mtime"]:
                        raise FileNotFoundError
                    else:
                        return file_info["md5"]

                except FileNotFoundError:
                    hash = hashlib.md5()
                    with open(file_path, "rb") as fb:
                        while True:
                            block = fb.read(blocksize)
                            if not block:
                                break
                            hash.update(block)

                    file_info = {
                        "mtime" : os.path.getmtime(file_path),
                        "md5"   : hash.hexdigest(),
                    }

                    with open(info_path, "wb") as fwb:
                        pickle.dump(file_info, fwb)

                    return hash.hexdigest()

            while True:
                try:
                    all_file_info_list, remote_path, send_user_name, task_uuid = self._recv_path_task_queue.get()
                    # [{'source': '.\\.Room\\log.db',
                    # 'smd5': 'dd42eea5d5d99ffb9fa8319e01967f10',
                    # 'remote': 'H:\\path\\.Room\\log.db',
                    # 'rmd5': ''},
                    # {'source': '.\\新建 RTF 文档.rtf',
                    # 'smd5': '8274425de767b30b2fff1124ab54abb5',
                    # 'remote': 'H:\\path\\新建 RTF 文档.rtf',
                    # 'rmd5': ''}]

                    # 安全检测
                    if remote_path in ('', '.', '\\', '/') or remote_path[:2] in ('c:' 'C:'):
                        # 发送空
                        self.send(send_user_name, ["CMD_RECV_PATH", task_uuid, []])

                    # 删除多余文件
                    all_send_file_path_list = []
                    for file_info in all_file_info_list:
                        # 获得绝对路径
                        all_send_file_path_list.append(Path(file_info['remote']).absolute())

                    for local_file_path in getAllFiles(remote_path):
                        if (".md5" not in local_file_path) and (Path(local_file_path).absolute() not in all_send_file_path_list):
                            # 如果本地的这个文件不在列表, 就删除
                            print("删除多余文件:", local_file_path)
                            os.remove(local_file_path)

                    # 删除空文件夹
                    del_emp_dir(remote_path)

                    # 计算md5
                    for file_info in all_file_info_list:
                        try:
                            file_info['rmd5'] = _md5sum(file_info['remote'])
                        except FileNotFoundError:
                            pass

                    self.send(send_user_name, ["CMD_RECV_PATH", task_uuid, all_file_info_list])

                except Exception as err:
                    self._log.log_info_format_err("Recv Path", "处理接收目录错误!")
                    traceback.print_exc()
                    print(err)

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _send_fun_file(self, client_name, data):
        try:
            sock = self._user_dict[client_name]["sock"]
            ds = pickle.dumps(data)

            len_n = b'F' + '{:16}'.format(len(ds)).encode()

            encrypt_data = len_n + ds
            # 全部一起发送
            sock.sendall(encrypt_data)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(client_name)
            raise err

    def send_file(self, client_name, data):

        self._send_fun_file(client_name, data)

        # self._send_lock.acquire()
        # try:
        #     self._send_fun_file(client_name, data)
        # finally:
        #     self._send_lock.release()
        pass

    def get_user(self):

        return self._user_dict.keys()

class Client():

    def __init__(self, client_name, client_password, log=None, auto_reconnect=False, reconnect_name_whitelist=None, encryption=True):
        """
        文档:
            创建一个客户端

        参数:
            client_name : str
                客户端名称(用户名)
            client_password : str
                客户端密码(密码)
            log : None or str
                日志等级
                    None: 除了错误什么都不显示
                    "INFO": 显示基本连接信息
                    "DEBUG": 显示所有信息
            auto_reconnect : Bool(default False)
                断开连接后是否自动重连服务端
            reconnect_name_whitelist : list(default [])
                如果reconnect_name_whitelist不为空, 则重新连接只会连接客户端名称在reconnect_name_whitelist里的服务端
            encryption : bool(default True)
                是否加密传输, 不加密效率较高

        例子:
            # Client
            client = Client("Foo", "123456", log="INFO", auto_reconnect=True, reconnect_name_whitelist=None)

            # 运行默认的回调函数(所有接受到的信息都在self.recv_info_queue队列里,需要用户手动实现回调函数并使用)
            # 默认的回调函数只打印信息
            client.default_callback_server()

            # 连接服务端, 服务端名称在客户端定义为Baz
            client.conncet("Baz" ,"127.0.0.1", 12345, password="abc123")
        """
        if client_name == "myself":
            raise NameError('Client name not allowed to use "myself"')

        self.client_name = client_name
        self.client_password = client_password

        self.encryption = encryption
        if not encryption:
            # 不使用加密,全局不加密
            # 如果客户端加密,那么客户端会根据服务端的加密情况自动兼容
            self._recv_fun_encrypt = self._recv_fun
            self._send_fun_encrypt = self._send_fun

        self.recv_info_queue = queue.Queue()

        self._send_file_task_queue = queue.Queue()

        self._recv_file_task_queue = queue.Queue()

        self._recv_path_task_queue = queue.Queue()

        self._send_path_task_dict = {}

        self._get_event_info_dict = {}

        self._recv_get_info_queue = queue.Queue()

        self._get_callback_func_dict = {}

        self.is_encryption_dict = {}

        self.user_addr_dict = {}

        self._connect_timeout_sock_set = set()

        self.user = User()
        # 在用户对象里保存自己
        self.user.myself = MySelfObject(self)

        self._send_lock = threading.Lock()

        self._auto_reconnect = auto_reconnect

        if not reconnect_name_whitelist:
            self._reconnect_name_whitelist = []
        else:
            self._reconnect_name_whitelist = reconnect_name_whitelist

        self._user_dict = {}

        self._send_file_info_dict = {}

        self._send_file_user_lock_dict = {}

        self._encrypt_rsa = encrypt_rsa()
        self._encrypt_aes = encrypt_aes()

        self._log = Log(log)

        self._auto_reconnect_parameters_dict = {}
        self._auto_reconnect_lock_dict = {}
        self._auto_reconnect_timedelay_dict = {}

        if self._auto_reconnect:
            self._auto_reconnect_server()

        self._connect_timeout_server()

        self._get_event_callback_server()

        self._send_file_server()

        self._recv_file_server()

        self._recv_path_server()

    def conncet(self, server_name, ip, port, password="abc123"):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        if sys.platform == "win32":
            sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60000, 30000))

        sock.connect((ip, port))
        self._connect_timeout_sock_set.add(sock)

        self._log.log_info_format("Connect", server_name)
        self._user_dict[server_name] = {}
        self._user_dict[server_name]["sock"] = sock

        if self.encryption:
            self._send_fun(server_name, self._encrypt_rsa.pubkey)
        else:
            self._send_fun(server_name, "NOT_ENCRYPTION")

        server_pubkey = self._recv_fun(server_name)
        if server_pubkey == "NOT_ENCRYPTION":
            self._log.log_info_warning_format("WARNING", "NOT_ENCRYPTION")
            self.is_encryption_dict[server_name] = False
        else:
            self.is_encryption_dict[server_name] = True
        self._user_dict[server_name]["pubkey"] = server_pubkey

        setattr(self.user, server_name, Node(server_name, self))

        self._send_fun_encrypt(server_name, [self.client_name, self.client_password])
        self._send_fun_encrypt(server_name, password)

        connect_code = self._recv_fun_encrypt(server_name)
        if connect_code == "YES":
            self._log.log_info_format("Verified successfully", server_name)
            self._password_correct()
        else:
            self._log.log_info_format_err("Verified failed", server_name)
            self._password_err(server_name)
            return

        login_code = self._recv_fun_encrypt(server_name)
        if login_code == "YES":
            self._log.log_info_format("Login successfully", server_name)
            self._login_correct()
        else:
            self._log.log_info_format_err("Login failed", server_name)
            self._login_err(server_name)
            return

        self._connect_timeout_sock_set.remove(sock)
        self._send_fun_encrypt(server_name, (self._encrypt_aes.key, self._encrypt_aes.iv))
        aes_key, aes_iv = self._recv_fun_encrypt(server_name)
        self._user_dict[server_name]["aes_key"] = aes_key
        self._user_dict[server_name]["aes_iv"] = aes_iv
        self._connect_end()

        self._recv_data_server(server_name)

        self._auto_reconnect_parameters_dict[server_name] = [server_name, ip, port, password]
        try:
            self._auto_reconnect_lock_dict[server_name]
        except KeyError:
            self._auto_reconnect_lock_dict[server_name] = threading.Lock()

        try:
            self._connect_user_fun()
        except Exception as err:
            traceback.print_exc()
            print(err)

        self.user_addr_dict[server_name] = (ip, port)

    def _auto_reconnect_server(self):

        def re_connect(server_name, ip, port, password):

            lock = self._auto_reconnect_lock_dict[server_name]

            if lock.locked():
                return

            lock.acquire()
            try:
                for _ in range(10):
                    # limit max 10 times
                    try:
                        old_delay = self._auto_reconnect_timedelay_dict[server_name]
                        if old_delay > 30:
                            self._auto_reconnect_timedelay_dict[server_name] = 30
                    except KeyError:
                        old_delay = self._auto_reconnect_timedelay_dict[server_name] = 0

                    time.sleep(old_delay)

                    try:
                        if server_name not in self._user_dict.keys():
                            self.conncet(server_name, ip, port, password)
                            self._auto_reconnect_timedelay_dict[server_name] = 0
                            break
                        else:
                            self._log.log_info_format("already connect", server_name)
                            break
                    except Exception as err:
                    # except ConnectionRefusedError:
                        # except connect all err was in this
                        self._log.log_info_format_err("Re Connect Failed", "{0} {1}".format(server_name, err))
                        self._auto_reconnect_timedelay_dict[server_name] += 5
            finally:
                lock.release()

        def server():
            while True:
                time.sleep(30)
                for server_name in self._auto_reconnect_parameters_dict.keys():
                    if server_name not in self._user_dict.keys():
                        if self._reconnect_name_whitelist:
                            if server_name in self._reconnect_name_whitelist:
                                server_name, ip, port, password = self._auto_reconnect_parameters_dict[server_name]
                                re_connect_th = threading.Thread(target=re_connect, args=(server_name, ip, port, password))
                                re_connect_th.daemon = True
                                re_connect_th.start()
                        else:
                            server_name, ip, port, password = self._auto_reconnect_parameters_dict[server_name]
                            re_connect_th = threading.Thread(target=re_connect, args=(server_name, ip, port, password))
                            re_connect_th.daemon = True
                            re_connect_th.start()

        server_th = threading.Thread(target=server)
        server_th.daemon = True
        server_th.start()

    def _disconnect_user_fun(self, *args, **kwargs):
        pass

    def _register_disconnect_user_fun(self, disconnect_user_fun):

        self._disconnect_user_fun = disconnect_user_fun

    def _connect_user_fun(self, *args, **kwargs):
        pass

    def _register_connect_user_fun(self, connect_user_fun):

        self._connect_user_fun = connect_user_fun

    def _recv_data_server(self, server_name):
        def sub():
            while True:
                try:
                    recv_data = self._recv_fun_encrypt_fast(server_name)
                    # print(recv_data)
                except (ConnectionRefusedError, ConnectionResetError, TimeoutError, ConnectionAbortedError) as err:
                    self._log.log_info_format_err("Offline", "{0} {1}".format(server_name, err))
                    try:
                        self._disconnect_user_fun()
                    except Exception as err:
                        traceback.print_exc()
                        print(err)
                    break
                except Exception as err:
                    print("@NOW: @612{0}".cformat("捕获到连接未知错误:"))
                    traceback.print_exc()
                    print(err)
                    self._log.log_info_format_err("Offline", "{0} {1}".format(server_name, err))
                    try:
                        self._disconnect_user_fun()
                    except Exception as err:
                        traceback.print_exc()
                        print(err)
                    break

                try:
                    cmd = recv_data[0]
                    if cmd == "CMD_SEND":
                        # send ["CMD_SEND", data]
                        self.recv_info_queue.put([server_name, recv_data[1]])
                    elif cmd == "CMD_GET":
                        # process ["CMD_GET", uuid_id, get_name, (args, kwargs)]
                        self._recv_get_info_queue.put([server_name, recv_data])
                    elif cmd == "CMD_REGET":
                        # get result ["CMD_REGET", uuid_id, result_data]
                        self._get_event_info_dict[recv_data[1]]["result"] = recv_data[2]
                        self._get_event_info_dict[recv_data[1]]["event"].set()
                    elif cmd == "CMD_SHARE_UPDATE":
                        # ["CMD_SHARE_UPDATE", {attr:value}]
                        update_share_dict = recv_data[1]
                        get_user = getattr(self.user, server_name)
                        get_user.share._share_dict.update(update_share_dict)
                        for name, value in update_share_dict.items():
                            setattr(get_user.share, name, value)
                    elif cmd == "CMD_SHARE_DEL":
                        # ["CMD_SHARE_DEL", name]
                        name = recv_data[1]
                        get_user = getattr(self.user, server_name)
                        del get_user.share._share_dict[name]
                        delattr(get_user.share, name)
                    elif cmd == "CMD_SHARE_FLUSH":
                        # ["CMD_SHARE_FLUSH", self._share_dict]
                        share_dict = recv_data[1]
                        get_user = getattr(self.user, server_name)
                        # 更新变量
                        get_user.share._share_dict.update(share_dict)
                        for name, value in share_dict.items():
                            setattr(get_user.share, name, value)
                        # 删除多余变量
                        for del_key in get_user.share._share_dict.keys() - share_dict.keys():
                            del get_user.share._share_dict[del_key]
                            delattr(get_user.share, del_key)
                    elif cmd == "CMD_STATUS_FLUSH":
                        # ["CMD_STATUS_FLUSH", self._share_dict]
                        status_dict = recv_data[1]
                        get_user = getattr(self.user, server_name)
                        # 更新变量
                        get_user.status._share_dict.update(status_dict)
                        for name, value in status_dict.items():
                            setattr(get_user.status, name, value)
                        # 删除多余变量
                        for del_key in get_user.status._share_dict.keys() - status_dict.keys():
                            del get_user.status._share_dict[del_key]
                            delattr(get_user.status, del_key)
                    elif cmd == "CMD_SEND_FILE":
                        # ["CMD_SEND_FILE", xxx, xx, xx]
                        self._recv_file_task_queue.put((server_name, recv_data))
                    elif cmd == "CMD_ERCV_FILE_MD5":
                        # ['CMD_ERCV_FILE_MD5', "FILE_RECV_MD5", UUID('d6fbf782-0404-11ed-8912-68545ad0c824'), '9234cf4bffbd28432965c322c]
                        self._recv_file_task_queue.put((server_name, recv_data))
                    elif cmd == "CMD_RECV_FILE":
                        # ["CMD_RECV_FILE", remote_file_path, source_file_path, show, compress, uuid] server_name
                        user_obj = getattr(self.user, server_name)
                        user_obj.send_file(recv_data[1], recv_data[2], show=recv_data[3], compress=recv_data[4], uuid=recv_data[5])
                    elif cmd == "CMD_SRND_PATH":
                        # ["CMD_SRND_PATH", all_file_info_list, remote_path, task_uuid]
                        self._recv_path_task_queue.put((recv_data[1], recv_data[2], server_name, recv_data[3]))
                    elif cmd == "CMD_RECV_PATH":
                        # ["CMD_RECV_PATH", task_uuid, all_file_info_list]
                        self._send_path_task_dict[recv_data[1]]['all_file_info_list'] = recv_data[2]
                        self._send_path_task_dict[recv_data[1]]['event'].set()
                    else:
                        self._log.log_info_format_err("Format Err", "收到 {0} 错误格式数据: {1}".format(server_name, recv_data))
                except Exception as err:
                    self._log.log_info_format_err("Runtime Err", "Client处理数据错误!")
                    traceback.print_exc()
                    print(err)

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _default_get_event_callback_func(self, data):
        return ["Undefined", data]

    def register_get_event_callback_func(self, get_name, func):
        self._get_callback_func_dict[get_name] = func

    def _get_event_callback_server(self):
        def server():

            def do_user_func_th(client_name, callback_func, data, uuid_id):
                try:
                    # data : (*args, **kwargs)
                    result = callback_func(*data[0], **data[1])
                    self.send(client_name, ["CMD_REGET", uuid_id, result])
                except Exception as err:
                    print("@NOW: @612{0}".cformat("Client 处理get任务线程错误!"))
                    traceback.print_exc()
                    print(err)

            while True:
                try:
                    # client_name, ["CMD_GET", uuid_id, get_name, (args, kwargs)]
                    client_name, recv_data = self._recv_get_info_queue.get()
                    _, uuid_id, get_name, data = recv_data

                    try:
                        callback_func = self._get_callback_func_dict[get_name]

                        # 并发处理get请求
                        sub_th = threading.Thread(target=do_user_func_th, args=(client_name, callback_func, data, uuid_id))
                        sub_th.daemon = True
                        sub_th.start()

                    except KeyError:
                        result = self._default_get_event_callback_func(data)
                        self.send(client_name, ["CMD_REGET", uuid_id, result])
                except Exception as err:
                    print("@NOW: @612{0}".cformat("Client 处理get任务线程错误!"))
                    traceback.print_exc()
                    print(err)

        server_th = threading.Thread(target=server)
        server_th.daemon = True
        server_th.start()

    def default_callback_server(self):
        def sub():
            while True:
                from_user, recv_data = self.recv_info_queue.get()
                print("{0} from {1} recv: {2}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), from_user, recv_data))

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _connect_timeout_server(self):

        def sub():
            # 无论是否已经断开了都会再次断开次
            old_check_time_dict = {}
            while True:
                time.sleep(10)
                remove_sock_list = []
                for sock in self._connect_timeout_sock_set:
                    try:
                        old_check_time = old_check_time_dict[sock]
                    except KeyError:
                        old_check_time = old_check_time_dict[sock] = time.time()

                    if time.time() - old_check_time >= 15:
                        self._log.log_info_warning_format("WARNING", "timeout sock close: {0}".format(sock))
                        sock.close()
                        remove_sock_list.append(sock)

                for sock in remove_sock_list:
                    self._connect_timeout_sock_set.remove(sock)
                    del old_check_time_dict[sock]

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _connect_end(self):
        self._log.log_debug_format("_connect_end", "connect_end")

    def _disconnect(self, server_name):
        self._log.log_debug_format_err("_disconnect", "disconnect")
        self._user_dict[server_name]["sock"].close()
        del self._user_dict[server_name]
        delattr(self.user, server_name)

    def _password_err(self, server_name):
        self._log.log_debug_format_err("_password_err", "password_err")
        self._user_dict[server_name]["sock"].close()
        del self._user_dict[server_name]
        delattr(self.user, server_name)

    def _password_correct(self):
        self._log.log_debug_format("_password_correct", "password_correct")

    def _login_err(self, server_name):
        self._log.log_debug_format_err("_login_err", "login_err")
        self._user_dict[server_name]["sock"].close()
        del self._user_dict[server_name]
        delattr(self.user, server_name)

    def _login_correct(self):
        self._log.log_debug_format("_login_correct", "login_correct")

    def _recv_fun(self, server_name):
        try:
            sock = self._user_dict[server_name]["sock"]
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            # data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(server_name)
            raise err

    def _send_fun(self, server_name, data):
        try:
            sock = self._user_dict[server_name]["sock"]
            ds = pickle.dumps(data)

            len_n = '{:17}'.format(len(ds)).encode()

            # 全部一起发送
            sock.sendall(len_n + ds)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(server_name)
            raise err

    def _recv_fun_encrypt(self, server_name):
        try:
            sock = self._user_dict[server_name]["sock"]
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            if self.is_encryption_dict[server_name] and data_type != b'F':
                data_bytes = self._encrypt_rsa.decrypt(data_bytes)
            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            # traceback.print_exc()
            # print(err)
            self._disconnect(server_name)
            raise err

    def _send_fun_encrypt(self, server_name, data):
        try:
            sock = self._user_dict[server_name]["sock"]
            ds = pickle.dumps(data)

            if self.is_encryption_dict[server_name]:
                ds = self._encrypt_rsa.encrypt_user(ds, self._user_dict[server_name]["pubkey"])

            len_n = '{:17}'.format(len(ds)).encode()

            encrypt_data = len_n + ds
            # 全部一起发送
            sock.sendall(encrypt_data)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(server_name)
            raise err

    def _recv_fun_encrypt_fast(self, server_name):
        try:
            sock = self._user_dict[server_name]["sock"]
            # 接收长度
            len_n = 17
            buff = sock.recv(len_n)
            buff_frame = buff
            while len(buff) < len_n:
                len_n = len_n - len(buff)
                buff = sock.recv(len_n)
                buff_frame += buff

            data_type = buff_frame[:1]
            len_n = int(buff_frame[1:])

            # 接收数据
            buff = sock.recv(len_n)
            data_bytes = buff
            while len(buff) < len_n:
                # 接收的不够的时候
                len_n = len_n - len(buff)
                # 接受剩余的
                buff = sock.recv(len_n)
                # print("buff:\n", buff)
                # 原来的补充剩余的
                data_bytes += buff

            if self.is_encryption_dict[server_name] and data_type != b'F':
                data_bytes = self._encrypt_aes.decrypt(data_bytes)
            func_args_dict = pickle.loads(data_bytes)

            return func_args_dict
        except Exception as err:
            # traceback.print_exc()
            # print(err)
            self._disconnect(server_name)
            raise err

    def _send_fun_encrypt_fast(self, server_name, data):
        try:
            sock = self._user_dict[server_name]["sock"]
            ds = pickle.dumps(data)

            if self.is_encryption_dict[server_name]:
                ds = self._encrypt_aes.encrypt_user(ds, self._user_dict[server_name]["aes_key"], self._user_dict[server_name]["aes_iv"])

            len_n = '{:17}'.format(len(ds)).encode()

            encrypt_data = len_n + ds
            # 全部一起发送
            sock.sendall(encrypt_data)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(server_name)
            raise err

    def send(self, server_name, data):

        self._send_fun_encrypt_fast(server_name, data)

        # self._send_lock.acquire()
        # try:
        #     self._send_fun_encrypt(server_name, data)
        # finally:
        #     self._send_lock.release()
        pass

    def _md5sum(self, file_path, blocksize=FILE_MD5_BLOCKSIZE):
        root_path, file_name = os.path.split(file_path)
        md5_info_path = os.path.join(root_path, ".md5")
        if not os.path.exists(md5_info_path):
            os.mkdir(md5_info_path)
        info_path = os.path.join(md5_info_path, file_name+".info")

        try:
            with open(info_path, "rb") as frb:
                file_info = pickle.load(frb)

            last_mtime = os.path.getmtime(file_path)

            if last_mtime != file_info["mtime"]:
                raise FileNotFoundError
            else:
                return file_info["md5"]

        except FileNotFoundError:
            hash = hashlib.md5()
            with open(file_path, "rb") as fb:
                while True:
                    block = fb.read(blocksize)
                    if not block:
                        break
                    hash.update(block)

            file_info = {
                "mtime" : os.path.getmtime(file_path),
                "md5"   : hash.hexdigest(),
            }

            with open(info_path, "wb") as fwb:
                pickle.dump(file_info, fwb)

            return hash.hexdigest()

    def _send_file_server(self):
        def sub():

            def get_file_size_str(file_size):
                file_size = file_size / 1024
                if file_size < 1000:
                    return "{0:.2f}K".format(file_size)
                else:
                    file_size = file_size / 1024
                    if file_size < 1000:
                        return "{0:.2f}MB".format(file_size)
                    else:
                        file_size = file_size / 1024
                        return "{0:.2f}GB".format(file_size)

            def compress_fun(send_buff):
                return zlib.compress(send_buff)

            def no_compress_fun(send_buff):
                return send_buff

            def send_file_th_server(send_file, show):
                """ 发送文件线程 """
                reve_user = send_file.reve_user
                try:
                    user_lock = self._send_file_user_lock_dict[reve_user]
                except KeyError:
                    user_lock = threading.Lock()
                    self._send_file_user_lock_dict[reve_user] = user_lock

                user_lock.acquire()
                try:
                    self._send_file_info_dict[send_file._uuid] = send_file

                    source_file_path = send_file.source_file_path
                    remote_file_path = send_file.remote_file_path

                    # 计算MD5
                    send_file.statu = "calcumd5"
                    send_file.len = os.path.getsize(source_file_path)
                    send_file.md5 = self._md5sum(source_file_path)

                    # 发送文件
                    send_file._last_send_time = time.time()
                    send_file.statu = "sending"
                    # 发送文件流次数
                    send_times = int((send_file.len / FILE_SEND_BUFFER_SIZE) + 2)
                    send_file._send_times = send_times
                    # 发送文件对象信息
                    self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_INFO", send_file._uuid, send_file.reve_user, source_file_path, remote_file_path, \
                        send_file._compress_flag, send_times, send_file.len, send_file.md5, show])

                    if send_file._compress_flag:
                        used_compress_fun = compress_fun
                    else:
                        used_compress_fun = no_compress_fun

                    FILE_LOG_LOCK.acquire()
                    try:
                        with open(FILE_LOG_FILE_PATH, "a", encoding="utf-8") as fa:
                            fa.write("{0}: Send to {1} {2}\n".format(
                            time.strftime('%Y-%m-%d %H:%M:%S'),
                            reve_user,
                            source_file_path,
                            ))
                    finally:
                        FILE_LOG_LOCK.release()
                    if show:
                        with open(source_file_path, "rb") as frb:
                            file_name = source_file_path
                            if len(source_file_path) > 50:
                                file_name = "..." + source_file_path[-45:]
                            title="Send: {0} {1} to {2}".format(file_name, get_file_size_str(send_file.len), reve_user)
                            for index in tqdm(range(send_times), desc=title):
                                send_buff = frb.read(FILE_SEND_BUFFER_SIZE)
                                # 注释掉这段是让发送方和接收方发送和接收的数据量一样多
                                # if send_buff == b'':
                                #     send_file.percent = 1
                                #     continue
                                send_buff = used_compress_fun(send_buff)
                                self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_BUFF", send_file._uuid, send_buff])
                                send_file._last_send_time = time.time()
                                send_file.percent = index / send_times
                            send_file.percent = 1
                    else:
                        with open(source_file_path, "rb") as frb:
                            for index in range(send_times):
                                send_buff = frb.read(FILE_SEND_BUFFER_SIZE)
                                # if send_buff == b'':
                                #     send_file.percent = 1
                                #     continue
                                send_buff = used_compress_fun(send_buff)
                                self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_BUFF", send_file._uuid, send_buff])
                                send_file._last_send_time = time.time()
                                send_file.percent = index / send_times

                    # 发送接收完毕
                    self.send_file(reve_user, ["CMD_SEND_FILE", "FILE_END", send_file._uuid])

                    send_file.statu = "waitmd5"
                except Exception as err:
                    self._log.log_info_format_err("Send File TH", "发送文件数据流错误!")
                    traceback.print_exc()
                    print(err)
                finally:
                    user_lock.release()

            while True:
                try:
                    send_file, show = self._send_file_task_queue.get()

                    send_file_th = threading.Thread(target=send_file_th_server, args=(send_file, show))
                    send_file_th.daemon = True
                    send_file_th.start()
                except Exception as err:
                    self._log.log_info_format_err("Send File", "发送文件数据流错误!")
                    traceback.print_exc()
                    print(err)

        send_file_server_th = threading.Thread(target=sub)
        send_file_server_th.daemon = True
        send_file_server_th.start()

    def _recv_file_server(self):
        """ 接收_send_file_server服务发送过来的文件流 """
        def sub():

            def get_file_size_str(file_size):
                file_size = file_size / 1024
                if file_size < 1000:
                    return "{0:.2f}K".format(file_size)
                else:
                    file_size = file_size / 1024
                    if file_size < 1000:
                        return "{0:.2f}MB".format(file_size)
                    else:
                        file_size = file_size / 1024
                        return "{0:.2f}GB".format(file_size)

            def de_compress_fun(file_buff):
                return zlib.decompress(file_buff)

            def no_de_compress_fun(file_buff):
                return file_buff

            def alive_bar_th(send_file, send_user_name, bar_queue, show):
                if show:
                    file_name = send_file.remote_file_path
                    if len(send_file.remote_file_path) > 50:
                        file_name = "..." + send_file.remote_file_path[-45:]
                    title="Recv: {0} {1} from {2}".format(file_name, get_file_size_str(send_file.len), send_user_name)
                    send_times = send_file._send_times
                    for index in tqdm(range(send_times), desc=title):
                        bar_queue.get()
                        send_file.percent = index / send_times
                    send_file.percent = 1
                else:
                    send_times = send_file._send_times
                    for index in range(send_times):
                        bar_queue.get()
                        send_file.percent = index / send_times
                    send_file.percent = 1

            while True:
                try:
                    send_user_name, file_data = self._recv_file_task_queue.get()
                    file_cmd = file_data[1]
                    if file_cmd == "FILE_INFO":
                        # ['CMD_SEND_FILE', 'FILE_INFO', uuid, name, source_file_path, remote_file_path, _compress_flag, send_times, len, md5, show]
                        try:
                            send_file = self._send_file_info_dict[file_data[2]]
                        except KeyError:
                            send_file = RecvFile(file_data[3], file_data[4], file_data[5], file_data[6])
                        send_file._send_times = file_data[7]
                        send_file._source_md5 = file_data[9]
                        send_file.len = file_data[8]
                        # 保存进度条
                        send_file._bar_queue = queue.Queue()

                        alive_bar_th_th = threading.Thread(target=alive_bar_th, args=(send_file, send_user_name, send_file._bar_queue, file_data[10]))
                        alive_bar_th_th.daemon = True
                        alive_bar_th_th.start()

                        if send_file._compress_flag:
                            send_file._used_de_compress_fun = de_compress_fun
                        else:
                            send_file._used_de_compress_fun = no_de_compress_fun
                        send_file._uuid = file_data[2]
                        self._send_file_info_dict[send_file._uuid] = send_file
                        # 检查路径,若文件存在就删除(覆盖),若路径不存在就新建
                        remote_file_path = file_data[5]
                        # if os.path.isfile(remote_file_path):
                        #     os.remove(remote_file_path)
                        if os.path.isfile(remote_file_path + '.crf'):
                            os.remove(remote_file_path + '.crf')
                        path, _ = os.path.split(remote_file_path)
                        if not os.path.isdir(path):
                            if path:
                                os.makedirs(path)
                        send_file._last_recv_time = time.time()
                        send_file.statu = "recving"

                        FILE_LOG_LOCK.acquire()
                        try:
                            with open(FILE_LOG_FILE_PATH, "a", encoding="utf-8") as fa:
                                fa.write("{0}: Recv from {1} {2}\n".format(
                                    time.strftime('%Y-%m-%d %H:%M:%S'),
                                    send_user_name,
                                    remote_file_path,
                                ))
                        finally:
                            FILE_LOG_LOCK.release()
                    elif file_cmd == "FILE_BUFF":
                        # ['CMD_SEND_FILE', 'FILE_BUFF', UUID('3ec7e3ac-03f7-11ed-a13e-68545ad0c824'), b'\xff\xd8\xff\xe1\x12\xc8Exif\x00\x00MM\x00*\]
                        file_uuid = file_data[2]
                        file_buff = file_data[3]
                        send_file = self._send_file_info_dict[file_uuid]
                        remote_file_path = send_file.remote_file_path
                        # 追加数据进文件
                        file_buff = send_file._used_de_compress_fun(file_buff)
                        for index in range(1, 4):
                            try:
                                with open(remote_file_path + '.crf', "ab") as fab:
                                    fab.write(file_buff)
                                break
                            except PermissionError:
                                # permission denied
                                print("permission denied: Re Try.")
                                time.sleep(1 * index)
                        send_file._last_recv_time = time.time()
                        send_file._bar_queue.put(True)
                    elif file_cmd == "FILE_END":
                        # ['CMD_SEND_FILE', 'FILE_END', UUID('5302e4ee-03f7-11ed-8a81-68545ad0c824')]
                        send_file.statu = "waitmd5"
                        file_uuid = file_data[2]
                        send_file = self._send_file_info_dict[file_uuid]
                        remote_file_path = send_file.remote_file_path
                        # 计算文件MD5
                        remote_file_md5 = self._md5sum(remote_file_path + '.crf')
                        send_file.md5 = remote_file_md5
                        if send_file._source_md5 == remote_file_md5:
                            if os.path.isfile(remote_file_path):
                                os.remove(remote_file_path)
                            # 复原文件名
                            os.rename(remote_file_path + '.crf', remote_file_path)
                            send_file.statu = "success"
                        else:
                            send_file.statu = "md5err"
                        # 发送给对方md5
                        self.send(send_user_name, ["CMD_ERCV_FILE_MD5", "FILE_RECV_MD5", send_file._uuid, remote_file_md5])
                    elif file_cmd == "FILE_RECV_MD5":
                        # ['CMD_ERCV_FILE_MD5', "FILE_RECV_MD5", UUID('d6fbf782-0404-11ed-8912-68545ad0c824'), '9234cf4bffbd28432965c322c]
                        file_uuid = file_data[2]
                        send_file = self._send_file_info_dict[file_uuid]
                        if send_file.md5 ==  file_data[3]:
                            send_file.statu = "success"
                        else:
                            self._log.log_info_format_err("Recv File", "接收端文件数据MD5错误! {0}".format(send_file.source_file_path))
                            send_file.statu = "md5err"
                except Exception as err:
                    self._log.log_info_format_err("Recv File", "接收文件数据流错误!")
                    traceback.print_exc()
                    print(err)

        recv_file_server_th = threading.Thread(target=sub)
        recv_file_server_th.daemon = True
        recv_file_server_th.start()

    def _recv_path_server(self):
        """ 接收目录文件服务线程 """
        def sub():

            def getAllFiles(folder):
                """ 获取某个路径全文件 """
                filepath_list = []
                for root, folder_names, file_names in os.walk(folder):
                    for file_name in file_names:
                        file_path = os.path.join(root, file_name)
                        filepath_list.append(file_path)
                        # print(file_path)
                return filepath_list

            def del_emp_dir(path):
                """ 删除空文件夹 """
                # 这个函数对空文件夹下的空文件夹每次调用只能删除一个,需要多次调用
                for (root, dirs, files) in os.walk(path):
                    for item in dirs:
                        dir = os.path.join(root, item)
                        try:
                            os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
                            print("Remove empty folder: {0}".format(dir))
                        except Exception:
                            pass

                for (root, dirs, files) in os.walk(path):
                    for item in dirs:
                        dir = os.path.join(root, item)
                        try:
                            os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
                            print("Remove empty folder: {0}".format(dir))
                        except Exception:
                            pass

                for (root, dirs, files) in os.walk(path):
                    for item in dirs:
                        dir = os.path.join(root, item)
                        try:
                            os.rmdir(dir)  #os.rmdir() 方法用于删除指定路径的目录。仅当这文件夹是空的才可以, 否则, 抛出OSError。
                            print("Remove empty folder: {0}".format(dir))
                        except Exception:
                            pass

            def _md5sum(file_path, blocksize=FILE_MD5_BLOCKSIZE):
                root_path, file_name = os.path.split(file_path)
                md5_info_path = os.path.join(root_path, ".md5")
                if not os.path.exists(md5_info_path):
                    os.mkdir(md5_info_path)
                info_path = os.path.join(md5_info_path, file_name+".info")

                try:
                    with open(info_path, "rb") as frb:
                        file_info = pickle.load(frb)

                    last_mtime = os.path.getmtime(file_path)

                    if last_mtime != file_info["mtime"]:
                        raise FileNotFoundError
                    else:
                        return file_info["md5"]

                except FileNotFoundError:
                    hash = hashlib.md5()
                    with open(file_path, "rb") as fb:
                        while True:
                            block = fb.read(blocksize)
                            if not block:
                                break
                            hash.update(block)

                    file_info = {
                        "mtime" : os.path.getmtime(file_path),
                        "md5"   : hash.hexdigest(),
                    }

                    with open(info_path, "wb") as fwb:
                        pickle.dump(file_info, fwb)

                    return hash.hexdigest()

            while True:
                try:
                    all_file_info_list, remote_path, send_user_name, task_uuid = self._recv_path_task_queue.get()
                    # [{'source': '.\\.Room\\log.db',
                    # 'smd5': 'dd42eea5d5d99ffb9fa8319e01967f10',
                    # 'remote': 'H:\\path\\.Room\\log.db',
                    # 'rmd5': ''},
                    # {'source': '.\\新建 RTF 文档.rtf',
                    # 'smd5': '8274425de767b30b2fff1124ab54abb5',
                    # 'remote': 'H:\\path\\新建 RTF 文档.rtf',
                    # 'rmd5': ''}]

                    # 安全检测
                    if remote_path in ('', '.', '\\', '/') or remote_path[:2] in ('c:' 'C:'):
                        # 发送空
                        self.send(send_user_name, ["CMD_RECV_PATH", task_uuid, []])

                    # 删除多余文件
                    all_send_file_path_list = []
                    for file_info in all_file_info_list:
                        # 获得绝对路径
                        all_send_file_path_list.append(Path(file_info['remote']).absolute())

                    for local_file_path in getAllFiles(remote_path):
                        if (".md5" not in local_file_path) and (Path(local_file_path).absolute() not in all_send_file_path_list):
                            # 如果本地的这个文件不在列表, 就删除
                            print("删除多余文件:", local_file_path)
                            os.remove(local_file_path)

                    # 删除空文件夹
                    del_emp_dir(remote_path)

                    # 计算md5
                    for file_info in all_file_info_list:
                        try:
                            file_info['rmd5'] = _md5sum(file_info['remote'])
                        except FileNotFoundError:
                            pass

                    self.send(send_user_name, ["CMD_RECV_PATH", task_uuid, all_file_info_list])

                except Exception as err:
                    self._log.log_info_format_err("Recv Path", "处理接收目录错误!")
                    traceback.print_exc()
                    print(err)

        sub_th = threading.Thread(target=sub)
        sub_th.daemon = True
        sub_th.start()

    def _send_fun_file(self, client_name, data):
        try:
            sock = self._user_dict[client_name]["sock"]
            ds = pickle.dumps(data)

            len_n = b'F' + '{:16}'.format(len(ds)).encode()

            encrypt_data = len_n + ds
            # 全部一起发送
            sock.sendall(encrypt_data)
        except Exception as err:
            traceback.print_exc()
            print(err)
            self._disconnect(client_name)
            raise err

    def send_file(self, client_name, data):

        self._send_fun_file(client_name, data)

        # self._send_lock.acquire()
        # try:
        #     self._send_fun_file(client_name, data)
        # finally:
        #     self._send_lock.release()
        pass

    def get_user(self):

        return self._user_dict.keys()

def hash_encryption(user_info_dict):
    """
    return Server's user_napw_info

    user_info_dict:
    {
        "Foo" : "123456",
        "Bar" : "abcdef",
    }

    return:
    {
        'Foo': b'$2b$10$qud3RGagUY0/DaQnGTw2uOz1X.TlpSF9sDhQFnQvAFuIfTLvk/UlC',
        'Bar': b'$2b$10$rLdCMR7BJmuIczmNHjD2weTn4Mqt7vrvPqrqdTAQamow4OzvnqPji'
    }
    """

    user_info_encryption_dict = {}
    for user, passwd in user_info_dict.items():
        salt = bcrypt.gensalt(rounds=10)
        ashed = bcrypt.hashpw(passwd.encode(), salt)
        user_info_encryption_dict[user] = ashed

    return user_info_encryption_dict

def get_host_ip():

    try:
        # NOTE 多网卡的情况下这个返回的ip不明确,目测是最后一个连接的网卡ip
        # 只能让用户手动设置 local_ip 来指定绑定的ip
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip

if __name__ == "__main__":
    # ============================================== Server ==============================================
    server = Server("127.0.0.1", 12345, password="abc123", log="INFO",
            # user_napw_info={
            #     "Foo" : b'$2b$15$DFdThRBMcnv/doCGNa.W2.wvhGpJevxGDjV10QouNf1QGbXw8XWHi',
            #     "Bar" : b'$2b$15$DFdThRBMcnv/doCGNa.W2.wvhGpJevxGDjV10QouNf1QGbXw8XWHi',
            #     },
            # blacklist = ["192.168.0.10"],
            )

    def server_test_get_callback_func(data):
        # do something
        if isinstance(data, int):
            time.sleep(data)
        return ["server test", data]

    # register get callback func
    server.register_get_event_callback_func("test", server_test_get_callback_func)
    # run send recv callback server
    server.default_callback_server()

    # ============================================== Client_1 ============================================
    client_1 = Client("Foo", "123456", log="INFO", auto_reconnect=True)

    def client_test_get_callback_func(data):
        # do something
        if isinstance(data, int):
            time.sleep(data)
        return ["client test", data]

    # register get callback func
    client_1.register_get_event_callback_func("test", client_test_get_callback_func)
    # run send recv callback server
    client_1.default_callback_server()

    # connect
    client_1.conncet("Server" ,"127.0.0.1", 12345, password="abc123")

    # ============================================== Client_2 ============================================
    client_2 = Client("Bar", "123456", log="INFO", auto_reconnect=True, encryption=False)

    def client_test_get_callback_func(data):
        # do something
        if isinstance(data, int):
            time.sleep(data)
        return ["client test", data]

    # register get callback func
    client_2.register_get_event_callback_func("test", client_test_get_callback_func)
    # run send recv callback server
    client_2.default_callback_server()

    # connect
    client_2.conncet("Server" ,"127.0.0.1", 12345, password="abc123")

    # ============================================== Test ==============================================
    # send info
    server.user.Foo.send("Hello world!")
    client_1.user.Server.send("Hello world!")
    client_2.user.Server.send("Hello world!")

    # get info
    print(client_1.user.Server.get("test", "Hello world!"))
    print(client_2.user.Server.get("test", "Hello world!"))

    st = time.time()
    print(client_1.user.Server.get("test", 3))
    print(time.time() - st)

    st = time.time()
    print(client_2.user.Server.get("test", 5))
    print(time.time() - st)
