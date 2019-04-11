import requests
import readConfig as readConfig
from common.Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        # 调用ReadConfig模块的方法取得到config.ini文件的HTTP值
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        # 导入日志方法，self.logger调用
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        # 定义一个空得字典用来接收传入的各种参数，供后部分的请求方法GET,POST函数中调用
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    # 拼接url地址 http://www.baidu.com + API地址并赋值给self.url
    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+'://'+host+url

    # 传入headder参数后赋值给self.headers
    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    # 传入param参数后赋值给self.param
    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    # 传入data参数后赋值给self.data
    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    # 传入data参数后赋值给self.data，几乎不会用（可省略）
    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'F:/AppTest/Test/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))  # timeout 请求超时时间
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data（包括get参数和post表单提交方式）
    # uninclude upload file （不包括上传文件方式）
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file （上传文件方式）
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json  （JSON提交方式）
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    print("ConfigHTTP")
