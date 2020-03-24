import re
import requests



# url='http://127.0.0.1/DVWA-master/vulnerabilities/xss_r/'
# response=requests.get(url).text
# #解析response得到其中的表单
def get_form(response):
    def e(string):
        return string.encode('utf-8')

    def d(string):
        return string.decode('utf-8')

    # remove the content between html comments
    response = re.sub(r'(?s)<!--.*?-->', '', response)#删除response中的注释
    forms = {}
    matches = re.findall(r'(?i)(?s)<form.*?</form.*?>',
                         response)  # extract all the forms
    num = 0
    for match in matches:  # everything else is self explanatory if you know regex：正则表达式
        page = re.search(r'(?i)action=[\'"](.*?)[\'"]', match)
        method = re.search(r'(?i)method=[\'"](.*?)[\'"]', match)
        forms[num] = {}
        forms[num]['action'] = d(e(page.group(1))) if page else ''
        forms[num]['method'] = d(
            e(method.group(1)).lower()) if method else 'get'
        forms[num]['inputs'] = []

        inputs = re.findall(r'(?i)(?s)<input.*?>', match)#找出所有input标签，不过这里是不是应该将response换为match???
        for inp in inputs:
            inpName = re.search(r'(?i)name=[\'"](.*?)[\'"]', inp)
            if inpName:
                inpType = re.search(r'(?i)type=[\'"](.*?)[\'"]', inp)
                inpValue = re.search(r'(?i)value=[\'"](.*?)[\'"]', inp)
                inpName = d(e(inpName.group(1)))
                inpType = d(e(inpType.group(1)))if inpType else ''
                inpValue = d(e(inpValue.group(1))) if inpValue else ''
                if inpType.lower() == 'submit' and inpValue == '':
                    inpValue = 'Submit Query'
                inpDict = {
                    'name': inpName,
                    'type': inpType,
                    'value': inpValue
                }
                forms[num]['inputs'].append(inpDict)
        num += 1
    return forms

#form的数据结构：
#forms[{'action':'form_action.asp','method':'get','inputs':[{'name':'inpName','type':'inpType','value':'inpValue'}]}]
