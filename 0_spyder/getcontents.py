import requests
from lxml import etree
import re
def my_get(url):
    i = 0
    while i < 3:
        try:
            html = requests.get(url, timeout=5)
            return html
        except requests.exceptions.RequestException:
            i += 1
    return None


"""
获取新闻内容
输入url
输出[板块名，标题，作者，日期，新闻内容]/空
"""
# 板块名
# /html/body/div[2]/div[2]/div[1]/div
# /html/body/div[2]/div[2]/div[1]/div/a
# 标题
# /html/body/div[2]/h1
# 作者
# //*[@id="top_bar"]/div/div[2]/a
# //*[@id="top_bar"]/div/div[2]/span[2]/a
# //*[@id="top_bar"]/div/div[2]/span[2]
# 日期
# //*[@id="top_bar"]/div/div[2]/span
# //*[@id="top_bar"]/div/div[2]/span[1]
# 内容
# //*[@id="artibody"]/p[:]
# //*[@id="artibody"]/p[2]
def getcontents(url):
    # 发起HTTP GET请求并获取网页内容
    response = my_get(url)
    if response is None:
        return None
    html_content = response.content
    # 使用lxml库解析HTML内容
    html_tree = etree.HTML(html_content)

    # 板块名
    # 使用XPath表达式选择目标元素
    a_elements = html_tree.xpath('/html/body/div[2]/div[2]/div[1]/div/a')
    div_element = html_tree.xpath('/html/body/div[2]/div[2]/div[1]/div')
    if a_elements:
        # 如果存在<a>元素，则获取其值
        for a_element in a_elements:
            a_value = a_element.text
            # print("a:", a_value)
            bankuai = a_value
    elif div_element:
        # 如果不存在<a>元素，则获取<div>元素下的字符串
        for div in div_element:
            div_text = ''.join(div.xpath('.//text()'))
            # print("div:", div_text)
            bankuai = div_text
    else:
        # 如果匹配失败则退出
        return None
    # bankuai = html_tree.xpath('/html/body/div[2]/div[2]/div[1]/div | /html/body/div[2]/div[2]/div[1]/div/a')
    match = re.search(r'\b\w+\b', bankuai)
    bankuai = match.group(0)

    ## 标题
    title = html_tree.xpath('/html/body/div[2]/h1')
    title = title[0].text

    ## 作者
    author = ""
    author_elements = html_tree.xpath('//*[(@id="top_bar")]/div/div[2]/a | //*[(@id="top_bar")]/div/div[2]/span[2]/a | //*[@id="top_bar"]/div/div[2]/span[2]')
    for a in author_elements:
        if a.text:
            author = a.text

    ## 日期
    date = html_tree.xpath('//*[@id="top_bar"]/div/div[2]/span[1]')
    date = date[0].text

    ## 正文
    contents = ""
    ps = html_tree.xpath('//*[@id="artibody"]/p | //*[@id="artibody"]/p/span | //*[@id="artibody"]/p/font | //*[@id="artibody"]/p/a')
    for p in ps:
        try:
            contents += p.text
        except:
            pass
        try:
            contents += p.tail
        except:
            pass
    contents = re.sub(r'\s+', '', contents)

    ## 返回
    retval = [bankuai, title, author, date, contents]
    return retval

