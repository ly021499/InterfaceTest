import os
import codecs
import configparser

# 获取项目路径，供其它模块调用，split方法把文件路径切割成元组类型（路径，文件名）[0]取值路径
proDir = os.path.split(os.path.realpath(__file__))[0]
# 通过join方法将项目路径和config.ini拼成完整配置文件路径
configPath = os.path.join(proDir, "config.ini")

# ReadConfig类用于读取config.ini配置文件中的参数
class ReadConfig:
    def __init__(self):
        # 打开config.ini文件
        fd = open(configPath)
        # 读取config.ini文件
        data = fd.read()

        #  如果读取的数据的前3位是BOM_UTF8格式的则
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]     # 去除掉前3位字符，重新赋值给data
            # 使用codecs.open方法可以不用转换编码 重新 写入config,ini中
            file = codecs.open(configPath, "w")         # 原理博客： https://www.cnblogs.com/BigFishFly/p/6664700.html
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    # 通过参数化name,想取EMAIL中的任意值，则输入参数name进行取值
    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value


