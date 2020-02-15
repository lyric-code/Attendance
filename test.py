import re
import os
import sys
import PyQt5
from pandas import read_csv


def decode(csv_path):
    """
    解析文件，返回键为姓名，值为是否参加的字典
    :param csv_path:
    :return:
    """
    course_info = {}
    csv = read_csv(csv_path, nrows=1, sep='\t', encoding='utf-16', header=1)
    course_info['直播时间'] = csv.loc[0, '直播时间']
    course_info['直播群'] = csv.loc[0, '直播群']
    course_info['直播时长'] = csv.loc[0, '直播时长']

    csv = read_csv(csv_path, sep='\t', encoding='utf-16', header=5)
    # print('{}\n{}\n{}\n{}'.format(csv.dtypes, csv.index, csv.columns, csv.describe()))
    student_info = {}
    csv = csv.sort_values(by='姓名')
    # print(csv)
    for index in csv.index:
        ori_name = csv.at[index, '姓名']
        if ori_name.endswith('(老师)'):
            continue
        watch = csv.at[index, '观看直播']
        is_watch = False if '未参与' in watch or int(watch.split(':')[1]) < 40 else True
        # print(ori_name, watch)
        name = re.sub(r"[爸爸|妈妈|哥哥|姐姐|家长]", '', ori_name)
        name = re.sub(r"\(.*\)", '', name)
        if name not in student_info.keys():
            student_info[name] = is_watch
        else:
            student_info[name] = student_info[name] or is_watch
    return course_info, student_info


if __name__ == '__main__':
   print(decode('./data/japan.csv'))