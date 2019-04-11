import os
import readConfig as readConfig
import logging
from datetime import datetime
import threading

localReadConfig = readConfig.ReadConfig()


class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = readConfig.proDir          # 从readConfig模块中拿到项目路径并合成
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):      # 如果路径不存在，则新建一个
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # 定义写入文件的handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        # 定义日志输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    # 以下都是定制特定的日志输出格式
    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name+" - Code:"+code+" - msg:"+msg)

    # 返回一个保存日志的路径，用于生成报告的路径，日志和报告存储一起
    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(logPath, "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return logPath

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            logger.error(str(ex))


class MyLog:
    log = None
    # lock锁参考博客：https://blog.csdn.net/JackLiu16/article/details/81267176
    # 在多线程中使用lock可以让多个线程在写入日志时不会错乱，一个写入文件后，其他的线程必须排队等待
    mutex = threading.Lock()    # 创建一个锁

    def __init__(self):
        pass

    @staticmethod
    def get_log():

        if MyLog.log is None:
            MyLog.mutex.acquire()   # 锁定后要记得释放
            MyLog.log = Log()
            MyLog.mutex.release()   # 释放

        return MyLog.log

if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")

