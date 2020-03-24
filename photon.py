import re
import concurrent.futures
from urllib.parse import urlparse

#from dom import dom
from utils import getUrl, getParams
from requester import requester
from get_form import get_form
#from plugins.retireJs import retireJs

def photon(seedUrl, headers, level, threadCount, delay, timeout, skipDOM):
    forms = []  # web forms
    processed = set()  # urls that have been crawled
    storage = set()  # urls that belong to the target i.e. in-scope
    schema = urlparse(seedUrl).scheme  # extract the scheme e.g. http or https
    host = urlparse(seedUrl).netloc  # extract the host e.g. example.com
    main_url = schema + '://' + host  # join scheme and host to make the root url
    storage.add(seedUrl)  # add the url to storage
    checkedDOMs = []

    def rec(target):
        processed.add(target)
        url = getUrl(target, True)

        params = getParams(target, '', True)#得到参数
        if '=' in target:  # if there's a = in the url, there should be GET parameters
            inps = []
            for name, value in params.items():
                inps.append({'name': name, 'value': value})
            forms.append({0: {'action': url, 'method': 'get', 'inputs': inps}})

        response = requester(url, params, headers, True, delay, timeout).text



        #retireJs(url, response)##检测<script>中是否存在漏洞



        # if not skipDOM:
        #     highlighted = dom(response)
        #     clean_highlighted = ''.join([re.sub(r'^\d+\s+', '', line) for line in highlighted])
        #     if highlighted and clean_highlighted not in checkedDOMs:
        #         checkedDOMs.append(clean_highlighted)
        #         logger.good('Potentially vulnerable objects found at %s' % url)
        #         logger.red_line(level='good')
        #         for line in highlighted:
        #             logger.no_format(line, level='good')
        #         logger.red_line(level='good')
        forms.append(get_form(response))#取出response中的所有form表单
        matches = re.findall(r'<[aA].*href=["\']{0,1}(.*?)["\']', response)
        for link in matches:  # iterate over the matches
            # remove everything after a "#" to deal with in-page anchors
            link = link.split('#')[0]
            if link.endswith(('.pdf', '.png', '.jpg', '.jpeg', '.xls', '.xml', '.docx', '.doc')):
                pass
            else:
                if link[:4] == 'http':
                    if link.startswith(main_url):
                        storage.add(link)
                elif link[:2] == '//':
                    if link.split('/')[2].startswith(host):
                        storage.add(schema + link)
                elif link[:1] == '/':
                    storage.add(main_url + link);
                else:
                    storage.add(main_url + '/' + link)
    for x in range(level):
        urls = storage - processed  # urls to crawl = all urls - urls that have been crawled
        # for url in urls:
        #     rec(url)
        threadpool = concurrent.futures.ThreadPoolExecutor(
            max_workers=threadCount)
        futures = (threadpool.submit(rec, url) for url in urls)
        print(processed)
        for i in concurrent.futures.as_completed(futures):
            pass
    return [forms, processed]
