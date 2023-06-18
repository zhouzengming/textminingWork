import time
from writer import *
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getcontents import *

def spy_news(year,month,day):
    # 配置chromium
    # 创建Chromium浏览器实例
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    options.binary_location = '/mnt/cgshare/firefox/firefox'  # 设置Chromium浏览器的二进制路径
    geckodriver_path = '/root/PycharmProjects/pythonProject/geckodriver'
    driver = webdriver.Firefox(options=options, executable_path=geckodriver_path)  # 指定Chromium WebDriver的路径

    # 创建Chrome浏览器实例
    # driver = webdriver.Chrome()
    # 打开网页
    url = "https://news.sina.com.cn/roll/"
    driver.get(url)
    driver.execute_script("newsList.review.click("+str(year)+","+str(month-1)+","+str(day)+")")
    # 设置显式等待时间
    wait = WebDriverWait(driver, 10)  # 设置为10秒，可以根据需要调整
    tmppage = ""
    try:
        while True:
            # 等待目标元素加载完成
            element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div/ul')))

            # 获取渲染后的页面内容
            html = driver.page_source
            if html == tmppage:
                break

            # 使用lxml解析HTML
            tree = etree.HTML(html)

            # 使用XPath定位ul元素
            ul_elements = tree.xpath('//ul')

            # 遍历获取ul元素下的li元素和其子级span[2]/a元素
            for ul_element in ul_elements:
                li_elements = ul_element.xpath('./li')
                # 遍历处理li元素数据
                for li_element in li_elements:
                    a_element = li_element.xpath('./span[2]/a')
                    # 处理a元素数据
                    if a_element:
                        text = a_element[0].text
                        href = a_element[0].get('href')
                        # print(href, text)
                        data = getcontents(href)
                        if data is None:
                            continue
                        filename = './news/'+str(year)+'-'+str(month)+'-'+str(day)+'.csv'
                        write(filename, data)
                        # time.sleep(0.1)
            tmppage = html
            driver.execute_script("newsList.page.next()")
    except Exception as e:
        print(str(e))
    # 关闭浏览器
    driver.quit()

# spy_news(2023,6,13)