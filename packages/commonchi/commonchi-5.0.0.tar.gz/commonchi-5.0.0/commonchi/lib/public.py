
# cxx增加
import datetime
import xlrd,random
import os
from time import sleep
import time
from commonchi.lib.utility import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_shijianchuo_p():
    nowtime = datetime.datetime.now()
    # 格式化当前时间,获取时间戳
    strtime = datetime.datetime.strftime(nowtime, "%Y/%m/%d %H:%M:%S")
    return strtime


#读取Excel表格中passed数量   2022.1.22修改
def num_pa(file_path,num_result):
    global p
    try:
        book = xlrd.open_workbook(file_path, 'rb')  # 打开Excel
        sheet = book.sheet_by_index(0)  # 获取第几个sheet页数据
        p=0
        for i in range(1, sheet.nrows):  # sheet.nrows获取列表中的每一行
            #获取32行值
            z=sheet.cell_value(i, num_result)  # 文件类型2
            if z=='PASS':
                p=p+1
        return p
    except:
        pass


#获取行数
def gain_excel_nrows( num_table,file_path):
    #filepath = 'D:\\Interface_automation\\ussm\\test\\file\\data.xls'
    # module_path = os.path.abspath('..')  # 获取上一级目录
    # #filepath = module_path + '/file/data.xls'
    # filepath = module_path + file_path
    date = xlrd.open_workbook(file_path, "r")
    table = date.sheets()[num_table]  # 打开第几张表
    num_rows = table.nrows  # 获取表的行数
    return num_rows


#判断文件夹是否存在，不存在，则新建
def determine_directory(path):
    #path='D:\Interface_automation\API\\report\\aagc'
    os.path.exists(path)
    try:
        os.mkdir(path)
        sleep(1)
    except:
        pass
    sleep(1)

def bj():
    m_path = os.path.abspath(os.path.join(os.getcwd(), "."))  # 获取本级目录
    # print(m_path)
    return m_path

def lj():
    m_path = os.path.abspath(os.path.join(os.getcwd(), ".."))  # 获取上级目录
    # print(m_path)
    return m_path

def sj():
    m_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 获取上两级目录
    # print(m_path)
    return m_path

def html_time():
    html_time_1 = time.strftime("_%Y-%m-%d-%H-%M-%S", time.localtime())
    return html_time_1

def time1():
    time_11 = time.strftime("%Y/%m/%d", time.localtime())
    return time_11

def report_p(product_name):
    # report_pa = report_path() + product_name + "\excelReport\\"
    report_pa=os.path.join(report_path() + product_name, "excelReport")
    return report_pa

def TARGET_FILE_dir(product_name):
    TARGET_FILE_d = report_path() + product_name +  "\excelReport"
    #print(TARGET_FILE_d)
    return TARGET_FILE_d

def TARGET_FILE(product_name,source_file):
    TARGET_F = os.path.join(report_p(product_name), product_name + html_time() + source_file)
    # TARGET_F=os.path.join(report_path() + product_name, "excelReport", product_name + html_time + source_file)
    return TARGET_F

def SOURCE_FILE(source_file):
    SOURCE_FILE = os.path.join(bj(), source_file)
    return SOURCE_FILE

def TEST_CONFIG():
    TEST_CONF= os.path.join(bj(), "config.ini")
    return TEST_CONF


def html_file(product_name):
    html_fi=report_path() + product_name + '\\' + product_name + html_time() + ".html"
    return html_fi

def html_FILE_dir(product_name):
    html_FILE_d=report_path() + product_name
    # print(html_FILE_d)
    return html_FILE_d


def time_1():
    for i in range(50):
        time_1 = datetime.datetime.strftime(datetime.datetime.now(), "%m%d%H")
        return time_1
def random_n():
    random_n = ''.join(random.sample('123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRESTUVWXYZ', 3))
    return random_n
def random_num():
    time_11=time_1()
    random_n1=random_n()
    random_num = time_11 + random_n1
    return random_num
def time_2():
    time_2 = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
    return time_2
def random_nu():
    random_nu = ''.join(random.sample('0123456789', 4))
    return random_nu
def random_nu1():
    random_nu = ''.join(random.sample('0123456789', 4))
    return random_nu

def random_three():
    random_three = ''.join(random.sample('0123456789', 3))
    return random_three

def random_z():
    random_z = ''.join(random.sample('ABCDEFGHIGKLMNOPQRESTUVWXYZ', 4))
    return random_z
def pems_random():
    time_211=time_2()
    random_nu11=random_nu()
    random_z11=random_z()
    pems_random = time_211 + random_nu11 + random_z11
    return pems_random
def time_st():
    time_st = int(time.time() * 1000)
    #print(time_st)
    return time_st
def time_ots():
    time_ots = str(int(time.time()))
    #print(time_ots)
    return time_ots

def time_r():
    time_r = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    return time_r

def time_ny():
    time_r = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m")
    return time_r



def time_nyyc():
    time_r = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m")
    return time_r

def time_nyrsfmyc():
    time_r = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
    return time_r

def time_nyc():
    time_r = datetime.datetime.strftime(datetime.datetime.now(), "%Y")
    return time_r


# 定义10天后时间
def get_shijian_ten():
    # 获取当前时间
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=10)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date

# 定义1天后时间
def get_time_one():
    # 获取当前时间
    today = datetime.datetime.now()
    datedayOfWeek=today.weekday()
    if datedayOfWeek<4 or datedayOfWeek > 5:
        # 计算偏移量
        offset = datetime.timedelta(days=1)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y-%m-%d')
    else:
        # 计算偏移量
        offset = datetime.timedelta(days=3)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date



def get_next_month_otherday(month_str=None):
    # 获取下下一个月的第28天     get_next_month_otherday
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    if not month_str:
        # month_str = datetime.now().strftime('%Y-%m')
        month_str=datetime.datetime.now().strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    if month == 11:
        year += 1
        month = '01'
    elif month == 12:
        year += 1
        month = '02'
    else:
        month += 2
    return '{}-{}-28'.format(year, month)

def time_month():
    #获取当前月
    time_month = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m")
    return time_month
   #print(time_month())

def get_next_month(month_str=None):
    # 获取下一个月
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    if not month_str:
        # month_str = datetime.now().strftime('%Y-%m')
        month_str=datetime.datetime.now().strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    if month == 12:
        year += 1
        month = '01'
    else:
        month += 1
    return '{}-{}'.format(year, month)

def get_next2_month(month_str=None):
    # 获取下下一个月
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    if not month_str:
        # month_str = datetime.now().strftime('%Y-%m')
        month_str=datetime.datetime.now().strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    #if month ==11:
    if month == 11:
        year += 1
        month = '01'
    elif month == 12:
        year += 1
        month = '02'
    else:
        month += 2
    return '{}-{}'.format(year, month)



def time_3():
    time_3 = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
    return time_3




def random_six():
    random_six = ''.join(random.sample('0123456789', 6))
    return random_six

def random_cms():
    random_cms = ''.join(random.sample(
        ['0000275324', '0000087515', '0000060041', '0000001006', '0000001003', '0000001012', '0000001014', '0000001020',
         '0000001022', '0000001028', '0000001032', '0000001035', '0000001046', '0000001051', '0000001053', '0000001057',
         '0000001062', '0000001068', '0000001069', '0000001076', '0000001077', '0000001085', '0000001092', '0000001094',
         '0000001095', '0000001097', '0000001105', '0000001106', '0000001107', '0000001109', '0000001286', '0000001285',
         '0000001284', '0000001281', '0000001276', '0000001274', '0000001269', '0000001260', '0000001257'], 1))
    return random_cms
def random_cmsgwmc():
    random_cmsgwmc = ''.join(random.sample(
        ['中软国际董事局主席兼CEO', '副总监（主持工作）', 'CDT经理', '招聘副总裁', '集团副总裁', '集团总裁', '集团执行总裁', '招聘总裁', '总监', '事业部副总经理', '事业部总经理',
         '交付部经理', 'RDD副总裁', '业务部副总裁', '业务线副总裁', '业务群副总裁', '业务群总裁', '中软国际董事会执行委员会委员', '公司首席财务官CFO', '公司首席行政官CAO',
         '中软国际有限公司总裁', '中软国际有限公司副总裁', 'IIU总裁', 'IIU副总裁', 'RDD总裁', 'PDT经理', '招聘总裁', '招聘经理', '大区招聘经理'], 1))
    return random_cmsgwmc
def random_cmszj():
    random_cmszj = ''.join(
        random.sample(['9级', '10级', '11级', '16级', '19级', '20级', '21级', '23级', '25级', '29级', '30级'], 1))
    return random_cmszj
def random_cmsgwjb():
    random_cmsgwjb = ''.join(random.sample(['M1', 'M2', 'M3', 'M4', 'M5', 'M6'], 1))
    return random_cmsgwjb
def random_cmsdeptno():
    random_cmsdeptno = ''.join(random.sample(
        ['500031', '100011', '100065', '500060', '500021', '500054', '100010', '100012', '100020', '100021', '100023',
         '100024', '100025', '100026', '100035', '100036', '100037', '100038', '100045', '100046', '100047', '101006',
         '500147', '101007', '101008'], 1))
    return random_cmsdeptno
def time_cms():
    time_cms = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    return time_cms
def random_cmsxgbrma():
    random_cmsxgbrma = ''.join(random.sample(
        ['0000001012', '0000293837', '0000001077', '0000001069', '0000001068', '0000001109', '0000001107', '0000001105',
         '0000001094', '0000001097', '0000001085', '0000295525', '0000045451', '0000211377', '0000081042', '0000061667',
         '0000230702', '0000218807', '0000057965', '0000087331', '0000100308', '0000016880', '0000039419', '0000001191',
         '0000001717', '0000140384', '0000001646', '0000167514', '0000001014', '0000001020', '0000001022', '0000001028',
         '0000001032', '0000001035', '0000001046', '0000001051', '0000001053', '0000001057', '0000001062', '0000001068',
         '0000001069', '0000001076', '0000001077', '0000001085', '0000001092', '0000001094', '0000001095',
         '0000001097'], 1))
    return random_cmsxgbrma
def random_cmsxgbrmb():
    random_cmsxgbrmb = ''.join(random.sample(
        ['0000001057', '0000001053', '0000001051', '0000001201', '0000001085', '0000295525', '0000057965', '0000087331',
         '0000100308', '0000016880', '0000039419', '0000001191', '0000001717', '0000140384', '0000001646', '0000167514',
         '0000001014', '0000001020', '0000001105', '0000001106', '0000001107', '0000001109', '0000001286', '0000001285',
         '0000001284', '0000001281', '0000001276', '0000001274', '0000001269', '0000001260', '0000001257'], 1))
    return random_cmsxgbrmb
def random_cmsxgbrmc():
    random_cmsxgbrmc = ''.join(random.sample(
        ['0000230702', '0000001191', '0000001717', '0000140384', '0000001646', '0000075337', '0000256431', '0000009909',
         '0000238459', '0000238459', '0000013333', '0000001161', '0000246368', '0000126764', '0000097033', '0000169714',
         '0000148054', '0000201351', '0000018687', '0000002456'], 1))
    return random_cmsxgbrmc
def random_cmsxgbrmd():
    random_cmsxgbrmd = ''.join(random.sample(
        ['0000174825', '0000034740', '0000160632', '0000067688', '0000040111', '0000200210', '0000006235', '0000128466',
         '0000052901', '0000194007', '0000129331', '0000023911', '0000247336', '0000086076', '0000274133', '0000032399',
         '0000201164', '0000155487', '0000107230', '0000161927'], 1))
    return random_cmsxgbrmd

def time_xny():
    # 获取当前时间
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=31)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m')
    return re_date

def id_card():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--window-size=1920,1080')
        try:
            driver = webdriver.Chrome(r'C:\Users\lvshaobo\AppData\Local\Google\Chrome\Application\chromedriver.exe',chrome_options=chrome_options)
        except:
            driver = webdriver.Chrome(chrome_options=chrome_options)
        sleep(0.1)
        driver.get('http://www.chineseidcard.com/?region=110101&birthday=20000307&sex=1&num=5&r=36')
        sleep(1)
        driver.find_element_by_xpath('//button[@id="submit_btn"]').click()
        sleep(0.2)
        card_number = driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]/table[2]/tbody/tr[1]/td').text
        sleep(0.5)
        return card_number
    except:
        pass

    # bj()
# lj()
# sj()


# print(id_card())