import requests
import random,time
from eva import map_draw as mp

def get_info(name, page_num):
    url = ' https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    """
    从指定的url中通过requests请求携带请求头和请求体获取网页中的信息,
    :return:
    """
    url1 = 'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=&fromSearch=true&suginput='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    for page in range(1, page_num + 1):
        if page % 6 == 0:
            time.sleep(60)
        # 请求参数
        data = {
            'first': 'true',
            'pn': page,
            'kd': name}
    # 保存参数的字典
    city_all = {}
    money_all = {}
    education_all = {}
    workyear_all = {}
    good_all = {}
    s = requests.Session()
    print('建立session：', s, '\n\n')
    s.get(url=url1, headers=headers, timeout=3)
    cookie = s.cookies
    print('获取cookie：', cookie, '\n\n')
    res = requests.post(url, headers=headers, data=data, cookies=cookie, timeout=3)
    res.raise_for_status()
    res.encoding = 'utf-8'
    page_data = res.json()
    result_json = res.json()['content']['positionResult']['result']
    for index, result in enumerate(result_json):
        # 统计地区分布
        city_all[result['city']] = city_all.get(result['city'], 0) + 1
        # 统计公司-薪资
        money_all[result['companyFullName']] = result['salary']
        # 统计学历需求
        education_all[result['education']] = education_all.get(result['education'], 0) + 1
        # 统计工作经验情况
        workyear_all[result['workYear']] = workyear_all.get(result['workYear'], 0) + 1
        # 待遇情况
        good_all[result['positionAdvantage']] = random.randint(1, 20)

    print('完成{}页.'.format(page))
    # {'杭州': 5, '深圳': 15, '苏州': 5, '广州': 5, '上海': 5, '北京': 40}
    print('请求响应结果：', page_data, '\n\n')
    return city_all, money_all, education_all, workyear_all, good_all


    # return page_data
def remain(name,page):
    # 循环每一页获取数据
    city_all, money_all, education_all, workyear_all, good_all = get_info(name, page)

    # 地区柱状图展示
    mp.create_Bar_charts(city_all, '地区分布').render('eva/templates/eva/charts/Regional_distribution_bar.html')

    # 地区geo展示
    mp.create_geo_charts(city_all, '地区分布').render('eva/templates/eva/charts/Regional_distribution_geo.html')

    # 学历要求
    mp.create_Pie_charts(education_all, '学历情况').render('eva/templates/eva/charts/学历情况.html')

    # 工作经验
    mp.create_Pie_charts(workyear_all, '工作经验').render('eva/templates/eva/charts/工作经验.html')

    # 薪资待遇
    mp.create_clound_charts(good_all, '薪资待遇').render('eva/templates/eva/charts/薪资待遇.html')

    print('统计完成...')

#
# if __name__ == '__main__':
#     remain()


