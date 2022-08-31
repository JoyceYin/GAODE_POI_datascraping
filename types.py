from urllib.parse import quote
from urllib import request
import json
import xlwt

amap_web_key = '05bb38349486c6b753cf4c97c9e3be81'
poi_search_url = "http://restapi.amap.com/v3/place/text"
#poi_boundary_url = "https://ditu.amap.com/detail/get/detail"
#from transCoordinateSystem import gcj02_to_wgs84
#广州['荔湾区','越秀区','海珠区','天河区','白云区','黄埔区','番禺区','花都区','南沙区','从化区','增城区']
#广州、佛山、肇庆、深圳、东莞、惠州、珠海、中山、江门
cityname = '广州市'
nanning_areas = ['荔湾区','越秀区','海珠区','天河区','白云区','黄埔区','番禺区','花都区','南沙区','从化区','增城区']    #可各个城市各个区一起

classes = ['物流速递']


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
    return poilist

# 数据写入excel
def write_to_excel(poilist, cityname, classfield):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    sheet.write(0, 0, '用地类型（大类）')
    sheet.write(0, 1, '用地类型（中类）')
    sheet.write(0, 2, 'x')
    sheet.write(0, 3, 'y')
    sheet.write(0, 4, 'count')
    sheet.write(0, 5, 'name')
    sheet.write(0, 6, '类型')
    sheet.write(0, 7, '省')
    sheet.write(0, 8, '市')
    sheet.write(0, 9, '区')
    sheet.write(0, 10, '地址')


    for i in range(len(poilist)):
        location = poilist[i]['location']
        name = poilist[i]['name']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]
        leixing = poilist[i]['type']
        pname = poilist[i]['pname']
        city = poilist[i]['cityname']
        qu = poilist[i]['adname']
        address = poilist[i]['address']


        # 每一行写入
        sheet.write(i + 1, 0, 'W')      #用地类型（大类）
        sheet.write(i + 1, 1, ' ')     #用地类型（中类）
        sheet.write(i + 1, 2, lng)      #x
        sheet.write(i + 1, 3, lat)      #y
        sheet.write(i + 1, 4, 1)
        sheet.write(i + 1, 5, name)     #name
        sheet.write(i + 1, 6, leixing)  #类型
        sheet.write(i + 1, 7, pname)       #省
        sheet.write(i + 1, 8, city)  # 市
        sheet.write(i + 1, 9, qu)  # 区
        sheet.write(i + 1, 10, address)  #地址


    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'' + cityname + " " + classfield + '.xls')


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, types, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&types=' + quote(
        types) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    #print(quote(types))
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    #print(req_url)
    return data


for clas in classes:
    classes_all_pois = []
    for area in nanning_areas:
        pois_area = getpois(area, clas)
        print('当前城区：' + str(area) + ', 分类：' + str(clas) + ", 总的有" + str(len(pois_area)) + "条数据")
        classes_all_pois.extend(pois_area)
    print("所有城区的数据汇总，总数为：" + str(len(classes_all_pois)))

    write_to_excel(classes_all_pois, cityname, clas)

    print('================分类：'  + str(clas) + "写入成功")

