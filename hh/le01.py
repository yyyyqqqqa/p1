import pandas as pd
import numpy as np,re




df = pd.read_excel(r'C:\Users\ASUS\Desktop\WeChat Files\yi962800840\FileStorage\File\2020-04\2020-4-2-14-37-28-21987139040700-采购公告搜索_中国政府采购网-采集大学的数据-后羿采集器.xlsx',encoding='utf-8')

df = df.replace(np.nan,'')

lambda x :x*2
res1 = df[list(df.keys())[-2]]
res2 = df[list(df.keys())[3]]

cg_time_list = []
cg_ren_list = []
cg_jg_list = []

for i in range(len(res2)):
    row = res2[i]
    row = row.replace('\xa0', ' ')
    cg_time = re.findall(r'(.+?)\n',row)
    cg_time_list.append(cg_time[0] if cg_time else '')
    cg_ren = re.findall(r'.+?采购人：(.+?)\n', row)
    cg_ren_list.append(cg_ren[0] if cg_ren else '')
    cg_jg = re.findall(r'.+?代理机构：(.+?)\n', row)
    cg_jg_list.append(cg_jg[0] if cg_jg else '')

#
# df['采购人'] = cg_ren_list
# df['代理机构'] = cg_jg_list
# df['采购时间'] = cg_time_list
#
#
# lianxiren_list = []
# phone_list = []
# cgdw_list = []
# cgdwdz_list = []
# zglxfs_list = []
# for i in range(len(res1)):
#     res = res1[i]
#     lianxiren = re.findall(r'项目联系人,(.+?),项目联系电话',res)
#     lianxiren_list.append(lianxiren[0] if lianxiren else '')
#     phone = re.findall(r'项目联系电话,(.+?),采购单位',res)
#     phone_list.append(phone[0] if phone else '')
#     cgdw = re.findall(r'采购单位,(.+?),采购单位地址',res)
#     cgdw_list.append(cgdw[0] if cgdw else '')
#     cgdwdz = re.findall(r'采购单位地址,(.+?),采购单位联系方式',res)
#     cgdwdz_list.append(cgdwdz[0] if cgdwdz else '')
#     zglxfs = re.findall(r'采购单位联系方式,(.+)',res)
#     zglxfs_list.append(zglxfs[0] if zglxfs else '')
#
#
#
# df['项目联系人'] = lianxiren_list
# df['项目联系电话'] = phone_list
# df['采购单位'] = cgdw_list
# df['采购单位地址'] = cgdwdz_list
# df['采购单位联系方式'] = zglxfs_list
#
#
#
# del df['字段3_字段4_字段5_字段6_字段7_字段8_字段9_字段10_字段11_字段12']
# del df['字段2']
#
#
# df.to_excel('新的.xlsx',index=False)
#








