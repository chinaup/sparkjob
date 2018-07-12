import requests
from bs4 import BeautifulSoup
import xlwt

if __name__ == '__main__':
    k = 1  # 参数k代表存储到excel的行数
    wb = xlwt.Workbook()  # 创建工作簿
    f = wb.add_sheet("招聘信息")  # 创建工作表
    '''
    下方的循环是将Excel表格中第一行固定
    Excel表第一行的前五列分别对应 职位、公司、工作地点、薪水、发布日期
    '''
    raw = ['职位', '公司', '工作地点', '薪水', '发布日期']
    for i in range(len(raw)):
        f.write(0, i, raw[i])
        '''
        write函数中第一个参数表示存储到多少行
        第二各参数存储到多少列表，第三个参数代表存储到对应行列的值
        '''
    for num in range(1,178):
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,spark,2,%d.html' % num
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        req = requests.get(url = url, headers = headers)
        req.encoding = 'GBK'
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        job_url = bf.find_all(class_='el')
        bf_job = BeautifulSoup(str(job_url), 'lxml')

        t1 = bf_job.select('.t1 span a')
        t2 = bf_job.select('.t2 a')
        t3 = bf_job.select('.t3')
        t4 = bf_job.select('.t4')
        t5 = bf_job.select('.t5')

        for i in range(0,len(t2)):
            job = t1[i].get('title')
            company = t2[i].get('title')
            place = t3[i+1].text
            money = t4[i+1].text
            date = t5[i+1].text
            print(job)
            f.write(k, 0, job)
            f.write(k, 1, company)
            f.write(k, 2, place)
            f.write(k, 3, money)
            f.write(k, 4, date)
            k += 1  # 每存储一行 k值加1

    wb.save('jobinfo.csv')  # 写完后掉用save方法进行保存