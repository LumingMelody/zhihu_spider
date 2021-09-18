"""
@version: 1.0
@author: luming
@contact: lumingmelody@gmail.com
@time: 2021/7/22 下午6:27
"""
import hashlib
import re
import time

import execjs
import requests
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append(['问题',
           '内容',
           '赞同',
           '评论',
           '回答时间'
           ])
payload = {}


def get_sign(page):
    # a_url = f"/api/v4/search_v3?t=general&q=PMPM%E7%B2%BE%E5%8D%8E%E6%B2%B9&correction=1&offset={page}&limit=20&lc_idx=0&show_all_topics=0"
    a_url = f"/api/v4/members/ao-di-66-50/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset={page}&limit=20&sort_by=voteups"
    # f = "+".join(["101_3_2.0", a_url, '"AGAdAZq8_xKPTh2HHoqLZKZttrX8sxfLhgM=|1619179846"'])
    f = "+".join(["101_3_2.0", a_url, '"ARDfnJrW2BKPTiZ_RrKZffJ2W3Zi5Wcbsuk=|1616569417"'])
    # print(f)
    fmd5 = hashlib.new('md5', f.encode()).hexdigest()
    with open('g_encrypt.js', 'r') as f:
        ctx1 = execjs.compile(f.read(), cwd=r'C:\python_project\zhihu_spider\node_modules')
        encrypt_str = ctx1.call('b', fmd5)
    return "2.0_" + encrypt_str


headers = {
    'authority': 'www.zhihu.com',
    'x-zse-93': '101_3_2.0',
    # 'x-ab-param': 'top_test_4_liguangyi=1;zr_slotpaidexp=1;se_ffzx_jushen1=0;tp_contents=1;tp_dingyue_video=0;tp_topic_style=0;tp_zrec=1;qap_question_visitor= 0;zr_expslotpaid=3;pf_adjust=1;qap_question_author=0;pf_noti_entry_num=2',
    # 'x-ab-pb': 'CogBYAsBC4wCbAPBAscC2AIbACoD7AqbC/8D8wNDAMICoQNtAokC9AMHDLkCogOgA7QKtAC1C1ADqwP0C2oB4AsEBEABjQHKAvYC6gO3A88L5AoqAk8D6AM0DJ8CwAKOA9cLNwxSCz8AaQGEAlcDiQx0AcwCMgN9AtcCVgwPCzsC3AtPAXIDRwDLAxJEAAAAAQEAAAABAQABABUBAAAEAAEVAAAAAAMAAAABAAABAAAACwALAAEAAAACAQAAAQEAAQAAAAAAAAEAAQEBAAABAAA=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    # 'x-requested-with': 'fetch',
    'x-zse-96': '',
    # 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'referer': 'https://www.zhihu.com/org/ao-di-66-50/answers/by_votes?page=1',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_zap=82a033ff-4508-4626-ab2a-a420f6436dc9; d_c0="ARDfnJrW2BKPTiZ_RrKZffJ2W3Zi5Wcbsuk=|1616569417"; tshl=; _xsrf=0zBbAQXOtF2ZbGFMBLXZqRY1kGpNeSpq; tst=h; SESSIONID=5dfq837fVunumMDjEnwyIIvgBuXNiuK8hkx5QosYx16; JOID=W1sRBEpkNDtvcHQ3ZWr2KzEsWXt7W1deGEBNBwA6S1IZGzF5CMYIxwFyeTNgbDm52XsLxPRseeyB8Zejj0AQy2g=; osd=V1oQC09oNTpgdXg2ZGXzJzAtVn53WlZRHUxMBg8_R1MYFDR1CccHwg1zeDxlYDi41n4HxfVjfOCA8Jimg0ERxG0=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1626761874,1626919514,1626945711,1626945778; gdxidpyhxdE=7v6%2BvzlZPS%2Fyf%5CPr4cUm0ThLx2yZcZXLJvi60dx9KGw43GqMusYPGePEGrrqtAjs1lcu6PjWPKKNTI3cYdxmQuY9cbhsU4RoWiCfoH9NZah5DRf40aj95y%2B8OyU%2Fb6cZIILwVsimI0R0TNc6mQtimTfd4wDDXEpe07wM2c2DPZ9qzDCo%3A1626948248880; _9755xjdesxxd_=32; YD00517437729195%3AWM_NI=JZqDjmF5i8g%2Bu6kKOSDVMmEXgdXSnmRMFtR%2BMZorG1q5OM8zfxX6IPOv0UUuzxgjghD%2BMmMS6Se%2Bb%2B40vrrg2JJGuTM%2F0APRojOwpu5GFqgCcSW2WGUOviuY0KM%2B3EjFRHg%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed4b180fbf09ca2e93d88e78ba3d54b868b9babf4398d88fe8df87db4f0bed6c72af0fea7c3b92a8a86bfa5e96786eba7d9e621b7eaa5acce59888a838ec854a5bc98b4ed6792938a95d1218f86a193c63bb3eb81aebb72a6a898d7cc5c8daa00b6d87fbaa8a98be66488f5838ed059f68dabcce121f8f0ba93f16df29686a8f8608ff100a2d35aadb68198f37ff7998a92e649a18d99d3d64d9791ba8af853f49583ccb24faa9a9ea9e637e2a3; YD00517437729195%3AWM_TID=JtS8mKbAPHRERVQEFEN%2B2aDz1u0s0v8G; captcha_session_v2="2|1:0|10:1626947480|18:captcha_session_v2|88:S1V4RlgzQ2VLNnJ3QmxzU3ZybFpSay9WU2dkNVhQOC9ubHVtTnRtTjF0bnpEUVdpSmE3UFYrdHFVZHdUaDdVOQ==|abc8c4094b0cb6bc4f293b3f498a750b6ef3d152bb618861e6c2de4f9a3cf37f"; z_c0="2|1:0|10:1626947528|4:z_c0|92:Mi4xUjBuMENRQUFBQUFCRU4tY210YllFaWNBQUFDRUFsVk55TXdnWVFEYUNWcEg5cEI4TWFDSlBfX3JjbzFmNkx2MGtn|9ea342a5b798fb491874480adf9f683851259df4e3a895c7ac287ed2b7b85d82"; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1626947547; unlock_ticket="AGAmKj2BsA0nAAAAhAJVTeNG-WBuWak2pw1PpUNEcHL7EtCDfN6DsA=="; KLBRSID=57358d62405ef24305120316801fd92a|1626948552|1626941146; KLBRSID=57358d62405ef24305120316801fd92a|1626949574|1626941146'
}


def get_zhihu_user(z_url, offset):
    headers['x-zse-96'] = get_sign(offset)
    response = requests.request("GET", z_url, headers=headers, data=payload).json()
    results = response['data']
    for result in results:
        question = result['question']['title']
        content = re.sub(r'<.*?>', '', result['content'])
        voteup_count = result['voteup_count']
        comment_count = result['comment_count']
        ts = result['updated_time']
        timeArray = time.localtime(ts)
        updated_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        ws.append([question, content, voteup_count, comment_count, updated_time])
    wb.save(r"D:\知乎\zhihu_奥迪.xlsx")


if __name__ == '__main__':
    url = "https://www.zhihu.com/api/v4/members/ao-di-66-50/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship&offset={}&limit=20&sort_by=voteups"
    offset = 0
    for i in range(1, 6):
        print(offset)
        get_zhihu_user(url.format(offset), offset)
        offset += 20
