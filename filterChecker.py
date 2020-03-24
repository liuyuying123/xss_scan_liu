from checker import checker

def filterChecker(url,params,headers,GET,delay,occurences,timeout,encoding):
    positions=occurences.keys()
    sortedEfficiencies={}
    #adding < >to environments anyway because they can be used in all contexts
    environments=set(['<','>'])
    for i in range(len(positions)):
        sortedEfficiencies[i]={}
    for i in occurences:
        occurences[i]['score']={}
        context=occurences[i]['context']
        if context=='comment':
            environments.add('-->')
        elif context=='script':
            environment.add(occurences[i]['details']['quote'])
            environments.add('</scRipT/>')
        elif context=='attribute':
            if occurences[i]['details']['type']=='value':
                if occurences[i]['details']['name']=='srcdoc':
                    environments.add('&lt')
                    environments.add('&gt')
            if occurences[i]['details']['quote']:
                environments.add(occurences[i]['details']['quote'])

    for environment in environments:#environment就是我们要打分的字符
        if environment:
            efficiencies=checker(url,params,headers,GET,delay,environment,positions,timeout,encoding)
            #这个是什么意思？？？
            efficiencies.extend([0]*(len(occurences)-len(efficiencies)))
            for occurence,efficiency in zip(occurences,efficiencies):
                occurences[occurence]['score'][environment]=efficiency

    return occurences
