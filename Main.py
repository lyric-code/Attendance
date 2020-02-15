#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/2/14
# @Author   : LiangYue
# @Function : 
# @Reference: 


import sys
from GUI.MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
import re
import os.path as osp


def decode(csv_path, thres):
    """
    解析文件，返回键为姓名，值为是否参加的字典
    :param csv_path:
    :return:
    """
    with open(csv_path, encoding='utf-16') as f:
        csv = f.readlines()
    course = csv[2].split('\t')
    course_info = {
        'time': course[0],
        'class': course[1],
        'period': course[2]
    }
    student_info = {}
    for student in csv[6:]:
        student = student.split('\t')
        ori_name = student[2]
        if ori_name.endswith('(老师)'):
            continue
        watch = student[5]
        is_watch = False if '未参与' in watch or int(watch.split(':')[1]) < thres else True
        name = re.sub(r"[爸爸|妈妈|哥哥|姐姐|家长|姑姑|叔叔|舅舅|舅妈]", '', ori_name)
        name = re.sub(r"\(.*\)", '', name)
        if name not in student_info.keys():
            student_info[name] = is_watch
        else:
            student_info[name] = student_info[name] or is_watch
    return course_info, student_info


class ParseMainWindow(QMainWindow):
    """
    界面实现类，耗时函数需要使用多线程处理
    """

    def __init__(self):
        super(ParseMainWindow, self).__init__()
        self.ui = None
        self.csv_path = None
        self.ui_init()

    def ui_init(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('钉钉网课考勤统计')
        self.setWindowIcon(QIcon('./dingding.ico'))
        self.show()

    def redirect_print(self, info, color='k'):
        if color == 'k':
            color_code = '000000'
        elif color == 'y':
            color_code = 'FF8000'
        elif color == 'r':
            color_code = 'FF0000'
        elif color == 'b':
            color_code = '0000FF'
        print(info)
        self.ui.textBrowser.append("<font color=\"#{}\"> {} </font> ".format(color_code, info))
        self.update()

    def select_csv(self):
        self.csv_path, fileType = QFileDialog.getOpenFileName(caption="请选择输入的csv文件",
                                                              directory='./',
                                                              filter="CSV Files (*.csv)")
        if not self.csv_path:
            return
        print('已经选择csv文件：{}'.format(self.csv_path))
        period_thres = int(self.ui.spinBox.value())
        topic = osp.basename(self.csv_path).strip('.csv')
        # 输出解析信息
        course_info, student_info = decode(self.csv_path, period_thres)
        self.redirect_print("主题：{}\n时间：{}\n班级：{}\n时长：{}\n"
                            .format(topic, course_info['time'], course_info['class'], course_info['period']),
                            color='b')
        truant = list(filter(lambda x: not x[1], student_info.items()))  # 旷课的学生
        self.redirect_print('考勤正常:{}/{}'.format(len(student_info) - len(truant), len(student_info)))
        if len(truant) > 0:
            self.redirect_print('考勤异常名单（包括为参与/观看直播时间小于{}分钟）:{}'
                                .format(period_thres, ','.join([t[0] for t in truant])))
        # label = ['考勤正常', '考勤异常（包括为参与/观看直播时间小于40分钟）']
        # data = [len(student_info), len(truant)]
        # print(label, data)
        # plt.pie(label, data, autopct='%1.2f%%')
        # plt.title("Pie chart")
        # # plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = ParseMainWindow()
    sys.exit(app.exec_())
