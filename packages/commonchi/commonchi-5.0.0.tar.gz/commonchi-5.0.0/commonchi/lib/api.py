#定义接口自动化关键字类
import requests
import json
import sys,os
from commonchi.lib.get_mannjutoken import *
import configparser as cparser
from commonchi.lib.public import TEST_CONFIG


sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class SendRequests():
    """发送请求数据"""
    # 判断请求方式
    def sendRequests(self, s, data,token_1,cookie_2):
        try:
            method = data['method']
            url = data['url']
            #print(url)
            reade_mode = data['type']
            UseCase = data['UseCase']
            #encryption = data['encryption']
            h = data['headers']
            body_1 = data['body']
            par = data['params']
            contain_ch = data['contain_ch']
            ex_type = data['request_data_type']
            file = data['file']
            filename = data['filename']
            filepath = data['filepath']
            filetype = data['filetype']
            file_2 = data['file2']
            filename_2 = data['filename2']
            filepath_2 = data['filepath2']
            filetype_2 = data['filetype2']
            url_token=data['url_token']     #是否需要加token
            cookie_1=data['cookie_1']      #是否需要加cookie
            parametric=data['parametric']   #是否有逻辑关联
            msg = data['msg']
            #是否有逻辑关联
            #print(url_token)
            try:
                if parametric=='Yes':   #cxx220208
                    pass
                else:
                    if url_token == 'Yes':
                       # token_1 =data['token']   # Token的值
                        #token_1 = get_mannjutoken(product_name, lobnumber)  # Token的值
                        url = url + '&mannjuToken='+token_1
                        #print(url)
                    else:
                        url = url
                    if cookie_1=='Yes':
                        cookies=cookie_2
                    else:
                        cookies=None

                    if ex_type == 'File':
                        m_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 获取上两级目录
                        filepath = m_path + '\\file\\' + filepath
                        filepath_2 = m_path + '\\file\\' + filepath_2
                        if file_2 != '':

                            files_1 = {file: (filename, open(filepath, 'rb'), filetype),file_2: (filename_2, open(filepath_2, 'rb'), filetype_2)}

                        else:
                            files_1 = {file: (filename, open(filepath, 'rb'), filetype)}

                    else:
                        files_1 = None



                    #body_1 = body.encode("utf-8").decode("latin1")  #12.30
                    # if (body != '' or body != 'No') and contain_ch == 'Yes':   #12.30
                    if (body_1 != '' and body_1 != 'No'):
                        if contain_ch != 'Yes':  # contain_ch请求中是否包含汉字
                            body_1 = body_1.encode("utf-8").decode("latin1")
                            # str转换为dict
                            body_1 = json.loads(body_1)
                            if reade_mode == 'json':
                                # dict转换为json
                                body_1 = json.dumps(body_1)
                            else:
                                pass
                        else:
                            #pass   #12.30
                            body_1 = body_1.encode("utf-8")
                            body_1 = body_1.decode()
                            try:
                                body_1 = eval(body_1)
                            except:
                                body_1=json.loads(body_1)
                            # try:
                            #     body_1 = eval(body_1)
                            # except:
                            #     body_1=body_1.encode("utf-8").decode("latin1")
                            if reade_mode == 'json':
                                # dict转换为json
                                body_1 = json.dumps(body_1)
                            else:
                                pass
                    else:
                        pass
                    if h != 'No'and h !='':
                        try:
                            # str转换为dict
                            h = json.loads(h)
                        except:
                            h = None
                    else:
                        h = None
                    if par != 'No'and par != '':
                        try:
                            # str转换为dict
                            par = json.loads(par)
                        except:
                            par = None

                    else:
                        par = None

                    # if files_1 !='':
                    #     files=files_1
                    # else:
                    #     files=None
                    print("用例标题：%s" % UseCase)
                    print("请求方式：%s" % method)
                    print("请求url：%s" % url)
                    print("header：%s" % h)
                    print("params：%s" % par)
                    print("body：%s" % body_1)
                    print("文件：%s" % files_1)
                    print("cookie：%s" % cookies)
                    print("验证字段：%s" % msg)

                    res = s.request(method=method, url=url, headers=h, params=par, data=body_1, files=files_1,cookies=cookies,verify=None,auth=None, timeout=None, allow_redirects=True,proxies=None,hooks=None, stream=None, cert=None, json=None)
                    #res=requests.post(url=url,headers=h,data=body_1)
                    return res
            except:
                pass

        except:
            #print('api封装有误')
            pass

    def sendRequests_1(self, s, data,token_1,cookie_2):
        try:
            #2022/4/15
            cf = cparser.ConfigParser()
            TEST_CONFIG_1 = TEST_CONFIG()
            cf.read(TEST_CONFIG_1, encoding='UTF-8')
            ip = cf.get("tester", "ip")
            method = data['method']
            url = ip+data['url']
            UseCase = data['UseCase']
            #print(url)
            reade_mode = data['type']
            #encryption = data['encryption']
            h = data['headers']
            body_1 = data['body']
            par = data['params']
            contain_ch = data['contain_ch']
            ex_type = data['request_data_type']
            file = data['file']
            filename = data['filename']
            filepath = data['filepath']
            filetype = data['filetype']
            file_2 = data['file2']
            filename_2 = data['filename2']
            filepath_2 = data['filepath2']
            filetype_2 = data['filetype2']
            url_token=data['url_token']     #是否需要加token
            cookie_1=data['cookie_1']      #是否需要加cookie
            parametric=data['parametric']   #是否有逻辑关联
            msg = data['msg']
            #是否有逻辑关联
            #print(url_token)
            try:
                if parametric=='Yes':   #cxx220208
                    pass
                else:
                    if url_token == 'Yes':
                       # token_1 =data['token']   # Token的值
                        #token_1 = get_mannjutoken(product_name, lobnumber)  # Token的值
                        url = url + '&mannjuToken='+token_1
                        #print(url)
                    else:
                        url = url
                    if cookie_1=='Yes':
                        cookies=cookie_2
                    else:
                        cookies=None

                    if ex_type == 'File':
                        m_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 获取上两级目录
                        filepath = m_path + '\\file\\' + filepath
                        filepath_2 = m_path + '\\file\\' + filepath_2
                        if file_2 != '':

                            files_1 = {file: (filename, open(filepath, 'rb'), filetype),file_2: (filename_2, open(filepath_2, 'rb'), filetype_2)}

                        else:
                            files_1 = {file: (filename, open(filepath, 'rb'), filetype)}

                    else:
                        files_1 = None



                    #body_1 = body.encode("utf-8").decode("latin1")  #12.30
                    # if (body != '' or body != 'No') and contain_ch == 'Yes':   #12.30
                    if (body_1 != '' and body_1 != 'No'):
                        if contain_ch != 'Yes':  # contain_ch请求中是否包含汉字
                            body_1 = body_1.encode("utf-8").decode("latin1")
                            # str转换为dict
                            body_1 = json.loads(body_1)
                            if reade_mode == 'json':
                                # dict转换为json
                                body_1 = json.dumps(body_1)
                            else:
                                pass
                        else:
                            #pass   #12.30

                            body_1 = body_1.encode("utf-8")
                            body_1 = body_1.decode()
                            try:
                                body_1 = eval(body_1)
                            except:
                                body_1=json.loads(body_1)
                            # try:
                            #     body_1 = eval(body_1)
                            # except:
                            #     body_1=body_1.encode("utf-8").decode("latin1")
                            if reade_mode == 'json':
                                # dict转换为json
                                body_1 = json.dumps(body_1)
                            else:
                                pass
                    else:
                        pass
                    if h != 'No'and h !='':
                        try:
                            # str转换为dict
                            h = json.loads(h)
                        except:
                            h = None
                    else:
                        h = None
                    if par != 'No'and par != '':
                        try:
                            # str转换为dict
                            par = json.loads(par)
                        except:
                            par = None

                    else:
                        par = None

                    # if files_1 !='':
                    #     files=files_1
                    # else:
                    #     files=None
                    print("用例标题：%s" % UseCase)
                    print("请求方式：%s" % method)
                    print("请求url：%s" % url)
                    print("header：%s" % h)
                    print("params：%s" % par)
                    print("body：%s" % body_1)
                    print("文件：%s" % files_1)
                    print("cookie：%s" % cookies)
                    print("验证字段：%s" % msg)

                    res = s.request(method=method, url=url, headers=h, params=par, data=body_1, files=files_1,cookies=cookies,verify=None,auth=None, timeout=None, allow_redirects=True,proxies=None,hooks=None, stream=None, cert=None, json=None)
                    return res
            except:
                pass

        except:
            #print('api封装有误')
            pass





#pfms
    def sendRequests_2(self, s, data,token_1,cookie_2):
        try:
            #2022/4/15
            cf = cparser.ConfigParser()
            TEST_CONFIG_1 = TEST_CONFIG()
            cf.read(TEST_CONFIG_1, encoding='UTF-8')
            ip = cf.get("tester", "ip")
            method = data['method']
            url = ip+data['url']
            UseCase=data['UseCase']

            #print(url)
            reade_mode = data['type']
            #encryption = data['encryption']
            h = data['headers']
            body_1 = data['body']
            par = data['params']
            contain_ch = data['contain_ch']
            ex_type = data['request_data_type']
            file = data['file']
            filename = data['filename']
            filepath = data['filepath']
            filetype = data['filetype']
            file_2 = data['file2']
            filename_2 = data['filename2']
            filepath_2 = data['filepath2']
            filetype_2 = data['filetype2']
            url_token=data['url_token']     #是否需要加token
            cookie_1=data['cookie_1']      #是否需要加cookie
            parametric=data['parametric']   #是否有逻辑关联
            msg = data['msg']
            try:
                timeout=data['timeout']
            except:
                pass
            #是否有逻辑关联
            #print(url_token)
            try:
                if parametric=='Yes':   #cxx220208
                    pass
                else:
                    if url_token == 'Yes':
                       # token_1 =data['token']   # Token的值
                        #token_1 = get_mannjutoken(product_name, lobnumber)  # Token的值
                        url = url + '&mannjuToken='+token_1
                        #print(url)
                    else:
                        url = url
                    if cookie_1=='Yes':
                        cookies=cookie_2
                    else:
                        cookies=None

                    if ex_type == 'File':
                        m_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 获取上两级目录
                        filepath = m_path + '\\file\\' + filepath
                        filepath_2 = m_path + '\\file\\' + filepath_2
                        if file_2 != '':

                            files_1 = {file: (filename, open(filepath, 'rb'), filetype),file_2: (filename_2, open(filepath_2, 'rb'), filetype_2)}

                        else:
                            files_1 = {file: (filename, open(filepath, 'rb'), filetype)}

                    else:
                        files_1 = None



                    #body_1 = body.encode("utf-8").decode("latin1")  #12.30
                    # if (body != '' or body != 'No') and contain_ch == 'Yes':   #12.30
                    if (body_1 != '' and body_1 != 'No'):
                        if contain_ch != 'Yes':  # contain_ch请求中是否包含汉字
                            body_1 = body_1.encode("utf-8").decode("latin1")
                            # str转换为dict
                            body_1 = json.loads(body_1)
                            if reade_mode == 'json':
                                # dict转换为json
                                body_2=body_1
                                body_1=''
                            else:
                                body_2=''
                        else:
                            body_1 = body_1.encode("utf-8")
                            body_1 = body_1.decode()
                            try:
                                body_1 = eval(body_1)
                            except:
                                body_1=json.loads(body_1)
                            if reade_mode == 'json':
                                # dict转换为json
                                #body_1 = json.dumps(body_1)
                                body_2=body_1
                                body_1=''

                            else:
                                body_2 = ''
                    else:
                        body_1 = ''
                        body_2=''
                    if h != 'No'and h !='':
                        try:
                            # str转换为dict
                            h = json.loads(h)
                        except:
                            h = h
                    else:
                        h = None
                    if par != 'No'and par != '':
                        try:
                            # str转换为dict
                            par = json.loads(par)
                        except:
                            par = None

                    else:
                        par = None

                    print("用例标题：%s" % UseCase)
                    print("请求方式：%s" % method)
                    print("请求url：%s" % url)
                    print("headers：%s" % h)
                    print("params：%s" % par)
                    print("body：%s" % body_1)
                    print("body：%s" % body_2)
                    print("文件：%s" % files_1)
                    print("cookie：%s" % cookies)
                    print("验证字段：%s" % msg)

                    res = s.request(method=method, url=url, headers=h, params=par, data=body_1,files=files_1,cookies=cookies,json=body_2,timeout=None,verify=None,auth=None, allow_redirects=True,proxies=None,hooks=None, stream=None, cert=None)
                    #res =  requests.post(url=url, json=body_2, cookies=cookie_2)
                    return res
            except:
                pass

        except:
            #print('api封装有误')
            pass


    def sendRequests_3(self, s, data,token_1,cookie_2):
        try:
            method = data['method']
            url = data['url']
            #print(url)
            reade_mode = data['type']
            #encryption = data['encryption']
            h = data['headers']
            UseCase = data['UseCase']
            # print('-------------')
            # print(h)
            body_1 = data['body']
            par = data['params']
            contain_ch = data['contain_ch']
            ex_type = data['request_data_type']
            file = data['file']
            filename = data['filename']
            filepath = data['filepath']
            filetype = data['filetype']
            file_2 = data['file2']
            filename_2 = data['filename2']
            filepath_2 = data['filepath2']
            filetype_2 = data['filetype2']
            url_token=data['url_token']     #是否需要加token
            cookie_1=data['cookie_1']      #是否需要加cookie
            parametric=data['parametric']   #是否有逻辑关联
            msg=data['msg']
            try:
                timeout=data['timeout']
            except:
                pass

            #是否有逻辑关联
            #print(url_token)
            try:
                if parametric=='Yes':   #cxx220208
                    pass
                else:
                    if url_token == 'Yes':
                       # token_1 =data['token']   # Token的值
                        #token_1 = get_mannjutoken(product_name, lobnumber)  # Token的值
                        url = url + '&mannjuToken='+token_1
                        #print(url)
                    else:
                        url = url

                    if cookie_1=='Yes':
                        cookies=cookie_2
                    else:
                        cookies=None

                    if ex_type == 'File':
                        m_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 获取上两级目录
                        filepath = m_path + '\\file\\' + filepath
                        filepath_2 = m_path + '\\file\\' + filepath_2
                        if file_2 != '':

                            files_1 = {file: (filename, open(filepath, 'rb'), filetype),file_2: (filename_2, open(filepath_2, 'rb'), filetype_2)}

                        else:
                            files_1 = {file: (filename, open(filepath, 'rb'), filetype)}

                    else:
                        files_1 = None



                    #body_1 = body.encode("utf-8").decode("latin1")  #12.30
                    # if (body != '' or body != 'No') and contain_ch == 'Yes':   #12.30
                    if (body_1 != '' and body_1 != 'No'):
                        if contain_ch != 'Yes':  # contain_ch请求中是否包含汉字
                            body_1 = body_1.encode("utf-8").decode("latin1")
                            # str转换为dict
                            body_1 = json.loads(body_1)
                            if reade_mode == 'json':
                                # dict转换为json
                                body_2=body_1
                                body_1=''
                            else:
                                body_2=''
                        else:
                            #pass   #12.30
                            body_1 = body_1.encode("utf-8")
                            body_1 = body_1.decode()
                            try:
                                body_1 = eval(body_1)
                            except:
                                body_1=json.loads(body_1)
                            # body_1=body_1.encode('utf-8').decode('unicode_escape')


                            if reade_mode == 'json':
                                # dict转换为json
                                #body_1 = json.dumps(body_1)
                                body_2=body_1
                                body_1=''

                            else:
                                body_2 = ''
                    else:
                        body_1 = ''
                        body_2=''
                    if h != 'No'and h !='':
                        try:
                            # str转换为dict
                            h = json.loads(h)
                        except:
                            h = h
                    else:
                        h = None
                    if par != 'No'and par != '':
                        try:
                            # str转换为dict
                            par = json.loads(par)
                        except:
                            par = None

                    else:
                        par = None

                    print("用例标题：%s" % UseCase)
                    print("请求方式：%s" % method)
                    print("请求url：%s" % url)
                    print("header：%s" % h)
                    print("params：%s" % par)
                    print("body：%s" % body_1)
                    print("body：%s" % body_2)
                    print("文件：%s" % files_1)
                    print("cookie：%s" % cookies)
                    print("验证字段：%s" % msg)
                    try:
                        print("超时：%s" % timeout)
                    except:
                        pass

                    res = s.request(method=method, url=url, headers=h, params=par, data=body_1,files=files_1,cookies=cookies,json=body_2,verify=None,auth=None, timeout=None, allow_redirects=True,proxies=None,hooks=None, stream=None, cert=None)
                    #res =  requests.post(url=url, json=body_2, cookies=cookie_2)
                    return res
            except:
                pass

        except:
            #print('api封装有误')
            pass



    def sendRequests_4(self, s, data,token_1, cookie_2):
        method = data['method']
        url = data['url']
        # print(url)
        reade_mode = data['type']
        # encryption = data['encryption']
        h = data['headers']
        body_1 = data['body']
        par = data['params']
        contain_ch = data['contain_ch']
        ex_type = data['request_data_type']
        file = data['file']
        filename = data['filename']
        filepath = data['filepath']
        filetype = data['filetype']
        file_2 = data['file2']
        filename_2 = data['filename2']
        filepath_2 = data['filepath2']
        filetype_2 = data['filetype2']
        url_token = data['url_token']  # 是否需要加token
        cookie_1 = data['cookie_1']  # 是否需要加cookie
        parametric = data['parametric']  # 是否有逻辑关联
        msg = data['msg']
        timeout = data['timeout']

        # 是否有逻辑关联
        # print(url_token)
        try:
            if parametric == 'Yes':  # cxx220208
                pass
            else:
                if url_token == 'Yes':
                    # token_1 =data['token']   # Token的值
                    # token_1 = get_mannjutoken(product_name, lobnumber)  # Token的值
                    url = url + '&mannjuToken=' + token_1
                    # print(url)
                else:
                    url = url

                if cookie_1 == 'Yes':
                    cookies = cookie_2
                else:
                    cookies = None

                if ex_type == 'File':
                    m_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 获取上两级目录
                    filepath = m_path + '\\file\\' + filepath
                    filepath_2 = m_path + '\\file\\' + filepath_2
                    if file_2 != '':

                        files_1 = {file: (filename, open(filepath, 'rb'), filetype),
                                   file_2: (filename_2, open(filepath_2, 'rb'), filetype_2)}

                    else:
                        files_1 = {file: (filename, open(filepath, 'rb'), filetype)}

                else:
                    files_1 = None

                # body_1 = body.encode("utf-8").decode("latin1")  #12.30
                # if (body != '' or body != 'No') and contain_ch == 'Yes':   #12.30
                if (body_1 != '' and body_1 != 'No'):
                    if contain_ch != 'Yes':  # contain_ch请求中是否包含汉字
                        body_1 = body_1.encode("utf-8").decode("latin1")
                        # str转换为dict
                        body_1 = json.loads(body_1)
                        if reade_mode == 'json':
                            # dict转换为json
                            body_2 = body_1
                            body_1 = ''
                        else:
                            body_2 = ''
                    else:
                        # pass   #12.30
                        body_1 = body_1.encode("utf-8")
                        body_1 = body_1.decode()
                        try:
                            body_1 = eval(body_1)
                        except:
                            body_1 = json.loads(body_1)
                        # body_1=body_1.encode('utf-8').decode('unicode_escape')


                        if reade_mode == 'json':
                            # dict转换为json
                            # body_1 = json.dumps(body_1)
                            body_2 = body_1
                            body_1 = ''

                        else:
                            body_2 = ''
                else:
                    body_1 = ''
                    body_2 = ''
                if h != 'No' and h != '':
                    try:
                        # str转换为dict
                        h = json.loads(h)
                    except:
                        h = h
                else:
                    h = None
                if par != 'No' and par != '':
                    try:
                        # str转换为dict
                        par = json.loads(par)
                    except:
                        par = None

                else:
                    par = None
        except:
            pass
        print("请求方式：%s" % method)
        print("请求url：%s" % url)
        print("header：%s" % h)
        print("params：%s" % par)
        print("body：%s" % body_1)
        print("body：%s" % body_2)
        print("文件：%s" % files_1)
        print("cookie：%s" % cookies)
        print("验证字段：%s" % msg)
        print("timeout：%s" % timeout)
        # url='http://test.chinasoftinc.com:8996'
        # headers={"mannjuToken":get_mannjutoken("aa",'87515'),"module":"YHR_APP","method":"ehr_saas/web/icss/attOverApplyWithRest/getOverRestApplyShowInfo.welinkEmp","httpMethod":"get"}
        res=requests.get(url,headers=h)
        return res

    def sendRequests_5(self, s, data, token_1, cookie_2):
        method = data['method']
        url = data['url']
        # print(url)
        reade_mode = data['type']
        # encryption = data['encryption']
        h = data['headers']
        body_1 = data['body']
        par = data['params']
        contain_ch = data['contain_ch']
        ex_type = data['request_data_type']
        file = data['file']
        filename = data['filename']
        filepath = data['filepath']
        filetype = data['filetype']
        file_2 = data['file2']
        filename_2 = data['filename2']
        filepath_2 = data['filepath2']
        filetype_2 = data['filetype2']
        url_token = data['url_token']  # 是否需要加token
        cookie_1 = data['cookie_1']  # 是否需要加cookie
        parametric = data['parametric']  # 是否有逻辑关联
        msg = data['msg']
        form = data['form']

        # 是否有逻辑关联
        # print(url_token)
        try:
            if parametric == 'Yes':  # cxx220208
                pass
            else:
                if url_token == 'Yes':
                    # token_1 =data['token']   # Token的值
                    # token_1 = get_mannjutoken(product_name, lobnumber)  # Token的值
                    url = url + '&mannjuToken=' + token_1
                    # print(url)
                else:
                    url = url

                if cookie_1 == 'Yes':
                    cookies = cookie_2
                else:
                    cookies = None

                if ex_type == 'File':
                    m_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))  # 获取上两级目录
                    filepath = m_path + '\\file\\' + filepath
                    filepath_2 = m_path + '\\file\\' + filepath_2
                    if file_2 != '':

                        files_1 = {file: (filename, open(filepath, 'rb'), filetype),
                                   file_2: (filename_2, open(filepath_2, 'rb'), filetype_2)}

                    else:
                        files_1 = {file: (filename, open(filepath, 'rb'), filetype)}

                else:
                    files_1 = None

                # body_1 = body.encode("utf-8").decode("latin1")  #12.30
                # if (body != '' or body != 'No') and contain_ch == 'Yes':   #12.30
                if (body_1 != '' and body_1 != 'No'):
                    if contain_ch != 'Yes':  # contain_ch请求中是否包含汉字
                        body_1 = body_1.encode("utf-8").decode("latin1")
                        # str转换为dict
                        body_1 = json.loads(body_1)
                        if reade_mode == 'json':
                            # dict转换为json
                            body_2 = body_1
                            body_1 = ''
                        else:
                            body_2 = ''
                    else:
                        # pass   #12.30
                        body_1 = body_1.encode("utf-8")
                        body_1 = body_1.decode()
                        try:
                            body_1 = eval(body_1)
                        except:
                            body_1 = json.loads(body_1)
                        # body_1=body_1.encode('utf-8').decode('unicode_escape')


                        if reade_mode == 'json':
                            # dict转换为json
                            # body_1 = json.dumps(body_1)
                            body_2 = body_1
                            body_1 = ''

                        else:
                            body_2 = ''
                else:
                    body_1 = ''
                    body_2 = ''
                if h != 'No' and h != '':
                    try:
                        # str转换为dict
                        h = json.loads(h)
                    except:
                        h = h
                else:
                    h = None
                if par != 'No' and par != '':
                    try:
                        # str转换为dict
                        par = json.loads(par)
                    except:
                        par = None

                else:
                    par = None
        except:
            pass
        m = MultipartEncoder(body_1)
        headers = {
            "Content-Type": m.content_type}
        print("请求方式：%s" % method)
        print("请求url：%s" % url)
        print("header：%s" % headers)
        print("params：%s" % par)
        print("body：%s" % body_1)
        print("body：%s" % body_2)
        print("文件：%s" % files_1)
        print("cookie：%s" % cookies)
        print("验证字段：%s" % msg)

        res = requests.post(url, data=m, headers=headers, cookies=cookies)
        # print(res.text)
        return res