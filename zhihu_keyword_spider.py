import hashlib
import random
import re
import time
from openpyxl import Workbook
import execjs
import requests


# ""101_3_2.0+/api/v4/search_v3?t=general&q=%E9%80%90%E6%9C%AC%E7%B2%BE%E5%8D%8E%E6%B2%B9&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0+"AGAdAZq8_xKPTh2HHoqLZKZttrX8sxfLhgM=|1619179846"""
# referer = "https://www.zhihu.com/search?type=content&q=%E9%80%90%E6%9C%AC%E7%B2%BE%E5%8D%8E%E6%B2%B9"
referer = "https://www.zhihu.com/org/ao-di-66-50/answers/by_votes?page=1"


def get_sign(page):
    a_url = f"/api/v4/search_v3?t=general&q=PMPM%E7%B2%BE%E5%8D%8E%E6%B2%B9&correction=1&offset={page}&limit=20&lc_idx=0&show_all_topics=0"
    # a_url = f"/api/v4/members/ao-di-66-50/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset={page}&limit=20&sort_by=voteups"
    f = "+".join(["101_3_2.0", a_url, '"AGAdAZq8_xKPTh2HHoqLZKZttrX8sxfLhgM=|1619179846"'])
    # f = "+".join(["101_3_2.0", a_url, '"ARDfnJrW2BKPTiZ_RrKZffJ2W3Zi5Wcbsuk=|1616569417"'])
    # print(f)
    fmd5 = hashlib.new('md5', f.encode()).hexdigest()
    with open('g_encrypt.js', 'r') as f:
        ctx1 = execjs.compile(f.read(), cwd=r'C:\python_project\zhihu_spider\node_modules')
        encrypt_str = ctx1.call('b', fmd5)
    return "2.0_" + encrypt_str

USER_AGENT_LIST = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
                   'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
                   'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
                   'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
                   'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
                   'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.7 Firefox/68.0 PaleMoon/28.16.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
                   'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
                   'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                   ]

headers = {
    "cookie": '_zap=82a033ff-4508-4626-ab2a-a420f6436dc9; d_c0="ARDfnJrW2BKPTiZ_RrKZffJ2W3Zi5Wcbsuk=|1616569417"; tshl=; _xsrf=0zBbAQXOtF2ZbGFMBLXZqRY1kGpNeSpq; tst=h; SESSIONID=5dfq837fVunumMDjEnwyIIvgBuXNiuK8hkx5QosYx16; JOID=W1sRBEpkNDtvcHQ3ZWr2KzEsWXt7W1deGEBNBwA6S1IZGzF5CMYIxwFyeTNgbDm52XsLxPRseeyB8Zejj0AQy2g=; osd=V1oQC09oNTpgdXg2ZGXzJzAtVn53WlZRHUxMBg8_R1MYFDR1CccHwg1zeDxlYDi41n4HxfVjfOCA8Jimg0ERxG0=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1626761874,1626919514,1626945711,1626945778; gdxidpyhxdE=7v6%2BvzlZPS%2Fyf%5CPr4cUm0ThLx2yZcZXLJvi60dx9KGw43GqMusYPGePEGrrqtAjs1lcu6PjWPKKNTI3cYdxmQuY9cbhsU4RoWiCfoH9NZah5DRf40aj95y%2B8OyU%2Fb6cZIILwVsimI0R0TNc6mQtimTfd4wDDXEpe07wM2c2DPZ9qzDCo%3A1626948248880; _9755xjdesxxd_=32; YD00517437729195%3AWM_NI=JZqDjmF5i8g%2Bu6kKOSDVMmEXgdXSnmRMFtR%2BMZorG1q5OM8zfxX6IPOv0UUuzxgjghD%2BMmMS6Se%2Bb%2B40vrrg2JJGuTM%2F0APRojOwpu5GFqgCcSW2WGUOviuY0KM%2B3EjFRHg%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed4b180fbf09ca2e93d88e78ba3d54b868b9babf4398d88fe8df87db4f0bed6c72af0fea7c3b92a8a86bfa5e96786eba7d9e621b7eaa5acce59888a838ec854a5bc98b4ed6792938a95d1218f86a193c63bb3eb81aebb72a6a898d7cc5c8daa00b6d87fbaa8a98be66488f5838ed059f68dabcce121f8f0ba93f16df29686a8f8608ff100a2d35aadb68198f37ff7998a92e649a18d99d3d64d9791ba8af853f49583ccb24faa9a9ea9e637e2a3; YD00517437729195%3AWM_TID=JtS8mKbAPHRERVQEFEN%2B2aDz1u0s0v8G; captcha_session_v2="2|1:0|10:1626947480|18:captcha_session_v2|88:S1V4RlgzQ2VLNnJ3QmxzU3ZybFpSay9WU2dkNVhQOC9ubHVtTnRtTjF0bnpEUVdpSmE3UFYrdHFVZHdUaDdVOQ==|abc8c4094b0cb6bc4f293b3f498a750b6ef3d152bb618861e6c2de4f9a3cf37f"; z_c0="2|1:0|10:1626947528|4:z_c0|92:Mi4xUjBuMENRQUFBQUFCRU4tY210YllFaWNBQUFDRUFsVk55TXdnWVFEYUNWcEg5cEI4TWFDSlBfX3JjbzFmNkx2MGtn|9ea342a5b798fb491874480adf9f683851259df4e3a895c7ac287ed2b7b85d82"; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1626947547; unlock_ticket="AGAmKj2BsA0nAAAAhAJVTeNG-WBuWak2pw1PpUNEcHL7EtCDfN6DsA=="; KLBRSID=57358d62405ef24305120316801fd92a|1626948552|1626941146',
    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "user-agent": random.choice(USER_AGENT_LIST),
    "x-zse-93": "101_3_2.0",
    "x-zse-96": "",
}
wb = Workbook()
ws = wb.active
ws.append(['用户名',
           '标题',
           '发布时间',
           '账号粉丝数',
           '账号链接',
           ])


def Zhihu_spider(z_url, page, path):
    headers['x-zse-96'] = get_sign(page)
    print(headers['x-zse-96'])
    resp = requests.get(url=z_url, headers=headers).json()
    print(resp)
    try:
        results = resp['data']
        for result in results:
            print(result)
            type = result['type']
            # print(type)
            if type == "search_result":
                # print("*" * 20)
                if result['object']['type'] == 'answer' or result['object']['type'] == 'article':
                    title = re.sub(r'<.*?>', '', result['highlight']['title'])
                    # desc = re.sub(r'<.*?>', '', result['highlight']['description'])
                    timeStamp = result["object"]['created_time']
                    timeArray = time.localtime(timeStamp)
                    create_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
                    name = result["object"]['author']['name']
                    url_token = result["object"]['author']['url_token']
                    user_url = f"https://www.zhihu.com/people/{url_token}"
                    fans = result["object"]['author']['follower_count']
                    ws.append([name, title, create_time, fans, user_url])
                    wb.save(path)
            # if type == 'news':
            #     title = result['object']['meta']
            #     # desc = result['object']['desc']
            #     content_list = result['object']['content_list']
            #     for content in content_list:
            #         # comment = content['content']
            #         # new_content = re.sub(r'<.*?>', '', comment)
            #         name = content['author']['name']
            #         # gender = content['author']['gender']
            #         fans = content['author']['follower_count']
            #         timeStamp = content['created_time']
            #         timeArray = time.localtime(timeStamp)
            #         create_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            #         user_url = content['author']['url']
            # elif type == 'topic':
            #     name = result['object']['name']
            #     fans = result['object']['follower_count']
            #     # desc = result['object']['meta']['description1']
            #     title = result['object']['meta']['title']
            #     user_url = ""
            #     create_time = ""
            #
            # elif type == 'article':
            #     title = result['object']['title']
            #     # desc = result['object']['excerpt']
            #     timeStamp = result['object']['created_time']
            #     timeArray = time.localtime(timeStamp)
            #     create_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            #     # comment = result['object']['content']
            #     # new_content = re.sub(r'<.*?>', '', comment)
            #     name = result['object']['author']['name']
            #     fans = result['object']['author']['follower_count']
            #     user_url = result['object']['author']['url']
            #
            # elif type == 'answer':
            #     title = ""
            #     # desc = result['object']['excerpt']
            #     timeStamp = result['object']['created_time']
            #     timeArray = time.localtime(timeStamp)
            #     create_time = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            #     # comment = result['object']['content']
            #     # new_content = re.sub(r'<.*?>', '', comment)
            #     name = result['object']['author']['name']
            #     fans = result['object']['author']['follower_count']
            #     user_url = result['object']['author']['url']
    except Exception as e:
        print(e)


if __name__ == '__main__':
    keyword = "奥迪"
    path = r"D:\red_book\red_book_51wom\red_book_07_21\{}zhihu_07_22.xlsx".format(keyword)
    page = 0
    for i in range(1, 2):
        # url = f"https://www.zhihu.com/api/v4/search_v3?t=general&q={keyword}&correction=1&offset={page}&limit=20&lc_idx=0&show_all_topics=0"
        url = f"https://www.zhihu.com/api/v4/members/ao-di-66-50/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset=0&limit={page}&sort_by=voteups"
        Zhihu_spider(url, page=page, path=path)
        print(url)
        time.sleep(2)
        page += 20
    "https://www.zhihu.com/api/v4/members/ao-di-66-50/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset=0&limit=20&sort_by=voteups"
    "https://www.zhihu.com/api/v4/search_v3?t=general&q=%E6%BB%B4%E6%BB%B4&correction=1&offset=27&limit=20&lc_idx=27&show_all_topics=0&search_hash_id=eab8595976faa406f2695ba1b4961b41&vertical_info=0%2C1%2C1%2C0%2C0%2C0%2C0%2C0%2C1%2C1"
    "https://www.zhihu.com/api/v4/search_v3?t=general&q=%E6%BB%B4%E6%BB%B4&correction=1&offset=47&limit=20&lc_idx=47&show_all_topics=0&search_hash_id=eab8595976faa406f2695ba1b4961b41&vertical_info=0%2C1%2C1%2C0%2C0%2C0%2C0%2C0%2C1%2C1"
    "https://www.zhihu.com/api/v4/search_v3?t=general&q=%E6%BB%B4%E6%BB%B4&correction=1&offset=67&limit=20&lc_idx=67&show_all_topics=0&search_hash_id=eab8595976faa406f2695ba1b4961b41&vertical_info=0%2C1%2C1%2C0%2C0%2C0%2C0%2C0%2C1%2C1"
