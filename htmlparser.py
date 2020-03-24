#设想功能 ：将下载下来的网页解析，分离出注入点，和网页中过的URL
import re
from config import xsschecker
from utils import extractScripts

def htmlParser(response,encoding):
    rawResponse=response #raw response returned by requests
    response=response.text  #返回的response中的html源码内容
    if encoding:#如果用户指定了编码，则进行将probe进行编码
        response=response.replace(encoding(xsschecker),xsschecker)
    reflections=response.count(xsschecker)#判断html中返回了多少个检测指针

    position_and_context={}#指的是：
    environment_details={}#指的是：
    clean_response=re.sub(r'<!--[.\s\S]*?-->','',response)#将response中的注释清空
    script_checkable=clean_response#转换为可以检查的response内容
    for  script in extractScripts(script_checkable):#将html中的javascript代码提取出来
        #每个输出点的环境都作为一个字典occcurences存储，position：表示输出点在页面中的第几个字符处 context:输出位置点的执行环境（script、attribute,
        # html comment等）
        #details:执行环境的具体信息：tag:输出点在什么标签、type:输出点是参数名还是参数值（name、value） quote:输出点用什么包裹起来的（单引号、双引号）
        #value:参数值 name:参数值




        occurences=re.finditer(r'(%scurrentChar=occurence.group()[i]:.*?)$' %xsschecker,script)#finditer返回一个可迭代对象

        #判断xsschecker是否在script标签对里面
        if occurences:
            for occcurence in occurences:
                thisPosition=occurence.start(1)#thisPosition为输出点在页面中过的第几个字符处
                position_and_context[thisPosition]='script'#代表输出点的执行环境为javascript
                enviroment_details[thisPosition]={}
                enviroement_details[thisPosition]['details']={'quote':''}#输出点是用什么包裹起来的
                for i in range(len(occurence.group())):#遍历每一个字符 判断输出点是由什么包裹起来的 <script>v3dm0s</script>
                    currentChar=occurence.group()[i]
                    if currentChar in ('/','`','"','\'') and not escaped(i,occurence.group()):#在单引号、双引号、顿号里，且未被转义
                        enviroment_details[thisPosition]['details']['quote']=currentChar
                    elif currentChar in (')',']','}','}') and not escaped(i,occurence.group()):
                        break
                script_checkable=script_checkable.replace(xsschecker,'',1)
                # 总结：
                # 1.判断输出点是否在script标签对里面
                # 2.返回输出点在返回包原文的位置
                # 3.判断输出点是用什么包裹起来的（单引号、双引号、`号）


    #如果输出点在属性中如：<input name=keyword value="v3dm0s">
    if len(position_and_context)<reflections:#如果判断的输出点个数小于输出点个数
        attribute_context=re.finditer(r'<[^>]*?(%s)[^>]*?>' %xsschecker,clean_response)#找出xsschecker所在的标签
        for occurence in attribute_context:
            match=occurence.group[0]
            thisPosition=occurence.start(1)
            parts=re.split(r'\s',match)#以空白字符分割 分割成如：['<input','name=keyword','value="v3dmos">']
            tag=parts[0][1:] #tag:'input'   将标签提取出来
            for part in parts:
                if xsschecker in part:# xsschecker参数所在的部分
                    Type,quote,name,value='','','',''
                    if '=' in part:
                        quote=re.search(r'=([\'~"])?',part).group(1)#判断由什么符号包裹
                        name_and_value=part.split('=')[0],'='.join(part.split('=')[1:])
                        if xsschecker ==name_and_value[0]:
                            Type='name'#注入点的类型是参数名
                        else:
                            Type='value'#注入点的类型是参数值
                        name=name_and_value[0]
                        value=name_and_value[1].rstrip('>').rstrip(quote).lstrip(quote)#例如"v3dmos"> 将其变为v3dmos
                    else:
                         Type='flag'
                    position_and_context[thisPosition]='attribute'
                    environment_details[thisPosition]={}
                    environment_details[thisPosition]['details']={'tag':tag,'type':Type,'quote':quote,'value':value,'name':name}



    #如果输出点在html中
    if len(position_and_context)<reflections:
        html_context=re.finditer(xsschecker,clean_response)
        for occurence in html_context:
            thisPosition=occurence.start()
            if thisPosition not in position_and_context:
                position_and_context[occurence.start()]='html'
                environment_details[thisPosition]={}
                environment_details[thisPosition]['details']={}

    if len(position_and_context)<reflections:
        comment_context=re.finditer(r'<--[\s\S]*?(%s)[\s\S]*?-->' %xsschecker,response)
        for occurence in comment_context:
            thisPosition=occurence.start(1)
            position_and_context[thisPosition]='comment'
            environment_details[thisPosition]={}
            environment_details[thisPosition]['details']={}
    database={}

    #将输出点数据存入数据库
    for i in sorted(position_and_context):
        database[i]={}
        database[i]['position']=i
        database[i]['context']=position_and_context[i]#表示页面执行环境：script标签 attribute html 注释四种类型
        database[i]['details']=environment_details[i]['details']#上下文环境的详细信息

    #标记无法执行的环境：style template textarea title noembed noscript
    bad_context=re.finditer(r'(?s)(?i)<(style|template|textarea|title|noembed|noscript)>[.\s\S]*(%s)[.\s\S]*</\1>' % xsschecker, response)
    non_executable_contexts=[]
    for each in bad_context:
        non_executable_contexts.append([each.start(),each.end(),each.group(1)])

    if non_executable_contexts:
        for key in database.keys():
            position=database[key]['position']
            badTag=isBadContext(position,non_executable_contexts)
            if badTag:
                database[key]['details']['badTag']=badTag
            else:
                database[key]['details'['badTag']]=''
    return database



#检查是否为转义字符
def escaped(position, string):
    usable = string[:position][::-1]
    match = re.search(r'^\\*', usable)
    if match:
        match = match.group()
        if len(match) == 1:
            return True
        elif len(match) % 2 == 0:
            return False
        else:
            return True
    else:
        return False


def isBadContext(position, non_executable_contexts):
    badContext = ''
    for each in non_executable_contexts:
        if each[0] < position < each[1]:
            badContext = each[2]
            break
    return badContext






#总结： 解析请求参数
# 对参数值进行无害字符串替换，发包
# 在返回包源码中搜索输出点
#标记输出点的上下文环境
#上下文环境例子：{455: {'position': 455, 'context': 'attribute', 'details': {'tag': 'input', 'type': 'value', 'quote': '"', 'value': 'v3dm0s', 'name': 'value'}}}























