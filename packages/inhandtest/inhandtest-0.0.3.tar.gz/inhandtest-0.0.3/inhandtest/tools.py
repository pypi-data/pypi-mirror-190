# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:42:40
# @Author  : Pane Li
# @File    : tools.py
"""
tools

"""
import logging
import re
import telnetlib
import time


def loop_inspector(flag='状态', timeout=90, interval=5, assertion=True):
    """装饰器，期望接收函数返回的值为True，如果为False时进行轮询，直至超时失败，如果正确就退出

    :param flag:  功能名称，用以输出日志，如果不填  默认为’状态’二字
    :param timeout:  循环检测超时时间
    :param interval:  循环检测时间间隔
    :param assertion: 默认期望断言，如果为False时 返回值
    :return:  assertion为False时，返回函数的值
    """

    def timeout_(func):
        def inspector(*args, **kwargs):
            for i in range(0, timeout + 1, interval):
                result = func(*args, **kwargs)
                if not result:
                    logging.info(f'{flag} assert failure, wait for {interval}s inspection')
                    time.sleep(interval)
                    continue
                else:
                    logging.info(f'{flag} assert normal')
                    return result
            else:
                if assertion:
                    raise AssertionError(f'{flag} assert timeout failure')

        return inspector

    return timeout_


class Telnet:
    __doc__ = '使用telnet连接设备，封装下面命令'

    def __init__(self, model: str, host: str, super_user: str, super_password: str, user='adm', password='123456',
                 port=23):
        """使用telnet连接设备

        :param model: 设备型号，‘VG710'
        :param host: 设备lan ip， 192.168.2.1
        :param super_user: 超级管理员的用户名称
        :param super_password:  超级管理员的密码
        :param user: 用户名
        :param password: 用户密码
        :param port: 端口
        """
        self.model = model
        self.host = host
        self.super_user = super_user
        self.super_password = super_password
        self.user = user
        self.password = password
        self.port = port
        self.host_name = ''
        self.super_tag = '/www #'
        self.config_tag = '(config)#'
        self.user_tag = '#'
        self.normal_tag = '>'
        if self.model.upper() not in ['VG710']:
            raise Exception(f'Not support this device model {self.model}')
        self.tn: telnetlib.Telnet
        self.__login()

    def update_hostname(self, hostname: str):
        """更新hostname 后对应的telnet也需要更新

        :param hostname: str
        :return:
        """
        self.host_name = hostname
        self.user_tag = f'{hostname}#'
        self.normal_tag = f'{hostname}>'

    def __login(self):
        """


        :return:
        """
        login_spe = {"VG710": '#'}
        try:
            # 连接telnet服务器
            logging.info("Start telnet 【%s:%s】" % (self.host, self.port))
            self.tn = telnetlib.Telnet(self.host, self.port, timeout=10)
        except:
            raise ConnectionError(f'Device【{self.host}:{self.port} connect failed】')
        logging.info("Telnet 【%s:%s】 connected" % (self.host, self.port))
        logging.info(self.tn.read_until('login:'.encode("cp936")).decode("cp936").strip())
        # 登录路由器
        self.tn.write("{}\n".format(self.user).encode("cp936"))
        logging.info(self.tn.read_until('Password:'.encode("cp936")).decode("cp936").strip())
        self.tn.write("{}\n".format(self.password).encode("cp936"))
        login_result = self.tn.read_until(login_spe.get(self.model).encode("cp936"), timeout=20).decode("cp936").strip()
        logging.info(login_result)
        if 'Login incorrect' in login_result:
            raise Exception('UsernameOrPasswordError')
        self.update_hostname(login_result.split('\r\n')[-1].split(' ')[-1][:-1])
        logging.info(f"Device {self.host} login success. user_tag: {self.user_tag}")

    def __auto_login(function):
        """自动重新登录, 只能当装饰器使用， 不对外使用

        :param function:
        :return:
        """

        def __auto_login(self, *args, **kwargs):
            try:
                res = function(self, *args, **kwargs)
            except (ConnectionResetError, ConnectionAbortedError):
                self.__login()
                res = function(self, *args, **kwargs)
            return res

        return __auto_login

    @staticmethod
    def __replace_cli(old: str or list or dict, replace_value: dict):
        """替换值， 当为字典时只替换key的值

        :param old:
        :param replace_value:
        :return:
        """
        new_old = old
        if old and replace_value:
            if isinstance(old, str):
                for k, v in replace_value.items():
                    new_old = new_old.replace(k, v)
            elif isinstance(old, list):
                new_old = []
                for i in old:
                    for k, v in replace_value.items():
                        i = str(i).replace(k, v)
                    new_old.append(i)
            elif isinstance(old, dict):
                new_old = {}
                for k, v in old.items():
                    for _k, _v in replace_value.items():
                        k = str(k).replace(_k, _v)
                    new_old.update({k: v})
            else:
                raise Exception('Not support this type')
        return new_old

    @__auto_login
    def super_mode(self):
        """进入路由器的超级模式

        @return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.info(read_contents)
        if self.config_tag in read_contents:
            self.send_cli(["exit", self.super_user + " " + self.super_password])
        elif self.super_tag in read_contents or (('/' in read_contents) and (' #' in read_contents)):
            self.send_cli(['cd /www'])
        elif self.user_tag in read_contents:
            self.send_cli([self.super_user + " " + self.super_password])
        elif self.normal_tag in read_contents:
            self.send_cli(["enable", self.password, self.super_user + ' ' + self.super_password])
        else:
            logging.warning(f'not support this mode. telnet return contents: {read_contents}')
            self.close()
            self.__login()
            self.super_mode()
        logging.info(f"Device {self.host} access in super mode")

    @__auto_login
    def config_mode(self):
        """配置模式

        :return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.info(read_contents)
        if self.config_tag in read_contents:
            pass
        elif self.super_tag in read_contents or (('/' in read_contents) and (' #' in read_contents)):
            self.send_cli(["cli", "con t"])
        elif self.user_tag in read_contents:
            self.send_cli(['con t'])
        elif self.normal_tag in read_contents:
            self.send_cli(["enable", self.password, 'con t'])
        else:
            logging.warning(f'not support this mode, last content:{read_contents}')
            self.close()
            self.__login()
            self.config_mode()
        logging.info(f"Device {self.host} access in config mode")

    @__auto_login
    def user_mode(self):
        """用户特权模式， 默认进入就是用户特权模式

        :return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.info(read_contents)
        if self.config_tag in read_contents:
            self.send_cli(['exit'])
        elif self.super_tag in read_contents or (('/' in read_contents) and (' #' in read_contents)):
            self.send_cli(["cli"])
        elif self.user_tag in read_contents:
            pass
        elif self.normal_tag in read_contents:
            self.send_cli(["enable", self.password])
        else:
            logging.warning(f'not support this mode. telnet return contents: {read_contents}')
            self.close()
            self.__login()
            self.user_mode()
        logging.info(f"Device {self.host} access in user mode")

    @__auto_login
    def normal_mode(self):
        """普通模式

        :return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))  # 普通模式下输入ctrl+c会返回  % Command is not supported!
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.info(read_contents)
        if self.config_tag in read_contents:
            self.send_cli(['exit', 'disable'])
        elif self.super_tag in read_contents or (('/' in read_contents) and (' #' in read_contents)):
            self.send_cli(["cli", "disable"])
        elif self.user_tag in read_contents:
            self.send_cli(['disable'])
        elif self.normal_tag in read_contents:
            pass

        else:
            logging.warning(
                f'not support this mode. telnet return contents: {read_contents} normal_tag: {self.normal_tag}')
            self.close()
            self.__login()
            self.user_mode()
        logging.info(f"Device {self.host} access in normal mode")

    @__auto_login
    def send_cli(self, command: list or str, read_until=None, **kwargs) -> str:
        """发送命令，支持多条，返回最后一条命令输入后的结果

        :param command: 支持发送多条命令["first_command", "second_command"] or 'command'
        :param read_until: str or list, 直至返回结果终止， 与command相呼应，如None的情况表示输入命令后等待1s， ['/www', None]
        :param kwargs
               timeout: 当有read_until时， timeout参数生效， 读取超时时间 默认30秒
               type_: 'super'|'config'|'user'|'normal'|None
               key_replace: 字典, 需将固定字符替换为另一字符则填写该参数, 例: {'\r\n': '', ' ': ''}等
               key_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在key_replace 有值时生效，默认last_read
                                 'cli': 仅替换发出去的命令
                                 'last_read': 仅替换最后读取到的内容
                                 'cli_last_read': 既要替换cli 也要替换最后读取到的内容

        :return: 读取超时时返回Exception， 如果命令执行正确，返回最后一条命令输入后的结果
        """
        key_replace_type = kwargs.get('key_replace_type') if kwargs.get('key_replace_type') else 'last_read'
        if kwargs.get('key_replace') and 'cli' in key_replace_type:
            command = self.__replace_cli(command, kwargs.get('key_replace'))
        logging.info(f"Device {self.host} send cli {command}")
        timeout = kwargs.get('timeout') if kwargs.get('timeout') else 30
        result = ''
        if not kwargs.get('type_') is None:
            if kwargs.get('type_') == 'super':
                self.super_mode()
            elif kwargs.get('type_') == 'config':
                self.config_mode()
            elif kwargs.get('type_') == 'user':
                self.user_mode()
            else:
                self.normal_mode()
        if command:
            command = [command] if isinstance(command, str) else command
            if read_until:
                read_until = [read_until] if isinstance(read_until, str) else read_until
                if len(read_until) != len(command):
                    raise Exception('The read_until params is error')
            else:
                read_until = [None for i in range(0, len(command))]
            for com, read_until_ in zip(command, read_until):
                self.tn.write((com + "\n").encode("cp936"))
                until_result = []
                for i in range(0, timeout, 1):  # 30秒没有找到期望的就主动断开
                    time.sleep(1)
                    result = self.tn.read_very_eager().decode('cp936').strip()
                    if result:
                        logging.info(result)
                    if read_until_:
                        until_result.append(result)
                        all_ = ''.join(until_result).replace('\r\n', '').replace(com, '')
                        if isinstance(read_until_, str):
                            if read_until_ in all_:
                                break
                        elif isinstance(read_until_, list):
                            if not [read_until_one for read_until_one in read_until_ if read_until_one not in all_]:
                                break
                    else:
                        # 如果没有readuntil 直接返回
                        break
                else:
                    self.tn.write(("\003" + "\r").encode("cp936"))
                    time.sleep(1)
                    raise Exception('ReadUntilTimeOutError')
        if kwargs.get('key_replace') and 'last_read' in key_replace_type:
            return self.__replace_cli(result, kwargs.get('key_replace'))
        else:
            return result

    @__auto_login
    def assert_cli(self, cli=None, expect=None, timeout=120, interval=5, type_='super',
                   key_replace=None, key_replace_type='last_read'):

        """在某个模式下支持输入一条或多条命令, 且支持对执行时最后一条命令返回的结果做断言
           该方法对ping tcpdump命令 无效

        :param cli: str or list, 发送的命令 一条或者多条
        :param expect: str or list or dict, 一条或多条希望校验的存在的结果，如需要判断不存在时，可以使用字典{$expect: False}
                       同时校验时可以是{$expect1: True, $expect: False}, str或者list时都是判断存在
        :param timeout: 检测超时时间  秒
        :param interval: 检测间隔时间 秒
        :param type_: 'super'|'config'|'user'|'normal'
        :param key_replace: 字典, 需将固定字符替换为另一字符则填写该参数, 例: {'\r\n': '', ' ': ''}等 默认去掉换行
        :param key_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在key_replace 有值时生效，默认last_read
                                 'cli': 仅替换发出去的命令
                                 'last_read': 仅替换最后读取到的内容
                                 'expect': 仅替换期望校验的值
                                 'cli_last_read'|'cli_expect'|'last_read_expect' 任意两种组合
                                 'cli_expect_last_read': 既要替换cli 也要替换最后读取到的内容还有校验的值
        :return: None|ResourceNotFoundError
        """

        if key_replace is None:
            key_replace = {'\r\n': ''}
        if cli is not None:
            for i in range(0, timeout, interval):
                if key_replace and 'cli' in key_replace_type:
                    cli = self.__replace_cli(cli, key_replace)
                    key_replace_type = key_replace_type.replace('cli', '')
                last_cli = cli if isinstance(cli, str) else cli[-1]
                key_replace.update({last_cli: ''})  # 替换到发出去的命令
                result = self.send_cli(cli, type_=type_, key_replace=key_replace, key_replace_type=key_replace_type)
                expect = str(expect) if isinstance(expect, int) else expect
                check_ = True
                if expect:
                    if 'expect' in key_replace_type:
                        expect = self.__replace_cli(expect, key_replace)
                    logging.info(f'start assert cli expect {expect}')
                    if isinstance(expect, str):
                        if expect not in result:
                            check_ = False
                    elif isinstance(expect, list):
                        if [expect_ for expect_ in expect if expect_ not in result]:
                            check_ = False
                    elif isinstance(expect, dict):
                        for k, v in expect.items():
                            if v:
                                if k not in result:
                                    check_ = False
                                    break
                            else:
                                if k in result:
                                    check_ = False
                                    break
                    else:
                        raise Exception('parameter expect is error')
                if check_:
                    break
                else:
                    time.sleep(interval)
                    logging.info(f"{expect} assert failure, wait for {interval}s inspection")
            else:
                raise Exception(f'{expect} not found timeout')
            logging.info(f'assert cli normal')

    @__auto_login
    @loop_inspector('Telnet ping', timeout=60)
    def ping(self, address='www.baidu.com', packets_number=4, params='', params_replace=None, lost_packets=False):
        """设备里面ping地址

        :param address: 域名或者IP
        :param packets_number, ping 包的个数，默认都是4个
        :param params: 参数 如'-I cellular1'、'-s 32'
        :param params_replace: 字典类型， 传入的参数转换关系表{$old: $new}
        :param lost_packets: True|False 如果为True判断会丢包，如果为False判断不丢包
        :return:
        """
        self.super_mode()
        params = params if params.startswith(' ') else ' ' + params
        params = self.__replace_cli(params, params_replace)
        x = True
        result = self.send_cli("ping " + address + params + f' -c {packets_number}', self.super_tag)
        if lost_packets:
            # 判断需要丢包
            if 'received, 0% packet loss' in result:
                x = False
        else:
            # 当判断不为丢包时
            if 'received, 0% packet loss' not in result:
                x = False
        return x

    @__auto_login
    def tcpdump(self, expect: str or list or dict, params_replace=None, timeout=30, interval=5, **kwargs):
        """

        :param expect: str or list or dict,
                       一条或多条希望校验的存在的结果，如需要判断不存在时，可以使用字典{$expect: False}
                       str或者list时都是判断存在
        :param kwargs: 命令参数, str, interface| param| cat_num
                        interface: 接口名称, wan| wifi_24g| wifi_5g| lan| cellular1
                        param: 抓包过滤关键字, None, 'icmp', 'http', 'port 21', 'host 1.1.1.1 and icmp'
                        catch_num: 抓包数量, int
        :param params_replace: 字典类型， 传入的参数转换关系表{$old: $new}
        :param timeout: 校验超时时间, int
        :param interval: 5
        :return:
        """
        flag = {'interface': '-i', 'param': '', 'catch_num': '-c'}
        command = 'tcpdump'
        if kwargs:
            for k, v in kwargs.items():
                for k_, v_ in flag.items():
                    if k == k_:
                        command = command + f' {v_} ' + f'{v}'
        command = self.__replace_cli(command, params_replace)
        for i in range(0, timeout, interval):
            tag_not = False
            if isinstance(expect, dict):
                for k, v in expect.items():
                    if not v:
                        tag_not = True
                        break
                expect = [_ for _ in expect.keys()]
            else:
                pass
            if not tag_not:  # 判断需要抓到
                try:
                    self.send_cli(command, [expect], timeout=15, type_='super')
                    logging.info('find the exception in tcpdump result.')
                    self.tn.write(("\003" + "\r").encode("cp936"))
                    break
                except:
                    time.sleep(interval)
                    continue
            else:  # 判断不需要抓到
                try:
                    self.send_cli(command, [expect], timeout=10, type_='super')
                    self.tn.write(("\003" + "\r").encode("cp936"))
                    time.sleep(interval)
                    continue
                except:
                    break
        else:
            raise Exception('TcpdumpTimeOutError')

    @__auto_login
    @loop_inspector('Telnet regular match content')
    def re_match(self, command: str or list, regular: str or list, type_='super', last_read_replace=None) -> str or list:
        """根据表达式获取最后一次执行命令的

        :param command: 发送命令，可以是一条或多条
        :param regular: 正则表达式，对执行的最后一次命令返回内容进行正则查询，必须要查询到，
                        如果查不到，直至查询超时并报错
                        如果查到不止一个，返回每个正则表达式的第一个
                        列子：硬件地址 r'HWaddr(.*)inet6'， '(([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})|([0-9a-fA-F]{2}[-]){5}([0-9a-fA-F]{2}))'
        :param type_: 'super'|'config'|'user'|'normal'
        :param last_read_replace: dict 替换最后一次命令返回内容的值 {'\r\n':'', ' ': ''}
        :return: str or list ，根据正则表达式的个数返回值
        """
        result = self.send_cli(command, type_=type_, key_replace=last_read_replace)
        if isinstance(regular, str):
            re_list = re.findall(regular, result)
            if re_list:
                for i in re_list:
                    if isinstance(i, str):
                        return re.findall(regular, result)[0]
                    else:
                        return re.findall(regular, result)[0]
            else:
                logging.info(f'regular {regular} match content None')
                return False
        elif isinstance(regular, list):
            result_ = []
            for regular_ in regular:
                re_list = re.findall(regular_, result)
                if re_list:
                    for i in re_list:
                        if isinstance(i, str):
                            result_.append(re.findall(regular_, result)[0])
                        else:
                            result_.append(re.findall(regular_, result)[0][0])
                else:
                    logging.info(f'regular {regular_} match content None')
                    return False
            else:
                return result_

    @__auto_login
    def reboot(self):
        """直接重启设备

        @return:
        """
        self.user_mode()
        self.send_cli(['reboot', 'y'])
        logging.info("【%s】Device is rebooting, wait for 120s" % self.host)
        time.sleep(120)

    @__auto_login
    def close(self):
        """关闭连接

        @return:
        """
        self.tn.close()
        logging.info("Telnet 【%s:%s】 close connect session" % (self.host, self.port))


if __name__ == '__main__':
    import sys
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO,
                        stream=sys.stdout)
    my = Telnet('VG710', '10.5.47.197', 'inhand', '64391099@inhand')
    print(my.re_match('ifconfig ath0', [r'HWaddr(.*)inet6', r'HWaddr(.*)inet6'], last_read_replace={'\r\n': '', ' ': ''}))
