import os
import unittest
from common.Log import MyLog as Log
import readConfig as readConfig
import HTMLTestRunner
from common.configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()

    # 逐行读取caselist.txt的文件名并添加进caseList列表中
    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        # 逐行读取文件名信息
        for value in fb.readlines():
            data = str(value)
            # 过滤空格和#开头注释的文件名
            if data != '' and not data.startswith("#"):
                # 再添加进caseList列表中
                self.caseList.append(data.replace("\n", ""))
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        # 执行set_case_list()方法拿到文件名列表self.caseList
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        # 遍历caseList列表
        for case in self.caseList:
            # 读取的文件名带了user路径，使用split进行分割，[-1]最后一个值
            case_name = case.split("/")[-1]
            print(case_name+".py")
            # 使用discover方法去寻找以case_name开头的文件（txt中并未带.py后缀）
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)

        # 判断suite_module列表中的对象是否大于0，否则返回None
        if len(suite_module) > 0:
            # 遍历suite_module列表拿到单个文件名对象
            for suite in suite_module:
                # 再遍历文件对象拿到testcase用例并添加到套件中
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            # 调用self.set_case_suite()方法得到suit对象
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("********TEST START********")
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                # run suit
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            fp.close()
            # 通过config.ini文件中的开关控制邮件是否发送，如果on就发送，off不发送
            # send test report by email
            if on_off == 'on':
                # 调用send_email()方法把生成的报告发送
                self.email.send_email()
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
