#-*- coding: utf-8 -*-
import requests,sqlite3
from bs4 import BeautifulSoup




# li = tmp1.keys()

# d2 = {}
# for i in li:
#     if i in tmp2:
#         tmp1[i]['running_file'] = tmp2.get(i).get('Running')
#     else:
#         tmp1[i]['running_file'] = "Not Available"



# for i in  tmp2:
#     if i not in tmp1:
#         temp ={
#         'category' : tmp2.get(i).get('category') ,
#         'version' : "",
#         'name' : '',
#         'country' : [],
#         'instals' : "",
#         'developer' : "",
#         'app_id' : i,
#         'minos' : "None",
#         'running_file': tmp2.get(i).get('Running')
#         }
#         tmp1.update({i:temp})
#     else:
#         pass

# for i in tmp1:

#     print("'"+i+"':"+json.dumps(tmp1.get(i))+",")
# exit()










def fun():
    method = "get"

    url = 'http://affise.c2a.in/adminer.php?server=api-controller-new.co5catuidqd8.us-east-1.rds.amazonaws.com&username=python&db=apptracking_api&select=campaigns&columns%5B0%5D%5Bfun%5D=&columns%5B0%5D%5Bcol%5D=app_id&columns%5B1%5D%5Bfun%5D=&columns%5B1%5D%5Bcol%5D=Category&columns%5B2%5D%5Bfun%5D=&columns%5B2%5D%5Bcol%5D=running_file&columns%5B21%5D%5Bfun%5D=&columns%5B21%5D%5Bcol%5D=&where%5B1%5D%5Bcol%5D=&where%5B1%5D%5Bop%5D=%3D&where%5B1%5D%5Bval%5D=&order%5B0%5D=&limit=10000&text_length=100'

    headers = {
        "Cache-Control":"max-age=0",
        "Upgrade-Insecure-Requests":"1",
        "Origin":"http://affise.c2a.in",
        "Content-Type":"multipart/form-data; boundary=----WebKitFormBoundaryxCiD1uU7SdBGpcpY",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer":"http://affise.c2a.in/adminer.php?server=api-controller-new.co5catuidqd8.us-east-1.rds.amazonaws.com&username=python&db=apptracking_api&select=campaigns",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-US,en;q=0.9",
        "Cookie":"adminer_key=e838431d0b799642318ebbb319329f77; adminer_permanent=c2VydmVy-YXBpLWNvbnRyb2xsZXItbmV3LmNvNWNhdHVpZHFkOC51cy1lYXN0LTEucmRzLmFtYXpvbmF3cy5jb20%3D-cHl0aG9u-YXBwdHJhY2tpbmdfYXBp%3AxUXrhooEYdIzGUoyy7p04w%3D%3D; adminer_sid=058rnfag2or3r926j8l3pupvl4; adminer_import=output%3Dtext%26format%3Dcsv%253B; c2a_id=9af2fb13a96c7db8a65e0de2fae26197; adminer_version=4.8.1",

        "User-Agent" : 'adminer_import=output%3Dfile%26format%3Dcsv; adminer_permanent=c2VydmVy-YXBpLWNvbnRyb2xsZXItbmV3LmNvNWNhdHVpZHFkOC51cy1lYXN0LTEucmRzLmFtYXpvbmF3cy5jb20%3D-cHl0aG9u-YXBwdHJhY2tpbmdfYXBp%3AfROmzN9IvfJsecRVLMPnPQ%3D%3D; adminer_sid=0ap4s9451rci4aajh47e6u3shc; c2a_id=b376dc6a007ec4267f4b6269406c3243; adminer_version=4.8.1'
    }









    files = [
    ('all', ('1')),
    ('output', ('text')),
    ('format', ('csv;')),
    ('export', ('Export')),
    # ('csv_file', ("",open('','U'),'application/octet-stream')),
    ('csv_file', ('text')),
    ('separator', ('csv;')),
    ('token', ('522803:346539')),
    ]
    res = requests.post(url=url,headers=headers,files=files)
    # print(res.text)
    return res.text

def get_db_connection():
    conn = sqlite3.connect('appdetails.db')
    # conn.row_factory = sqlite3.Row
    conn.execute("create table IF NOT EXISTS APP_details (PackageId TEXT PRIMARY KEY, Running TEXT, Category TEXT , version TEXT, minos TEXT , install TEXT , developer TEXT )")
    # conn.execute("create table IF NOT EXISTS daycheck (Day TEXT PRIMARY KEY)")
    # print("Table created successfully")  
    return conn





def get_data():
    # print('in get')
    t = fun()
    soup = BeautifulSoup(t,'html.parser')
    table = soup.find_all('form')
    # print(table[1])
    dic = {}
    for tr in table[1].find_all('tr'):
        metar = tr.find('td').get_text(separator='#')
        raw =metar.split('#')
        # print(raw)
        dic[raw[2]] = {}
        dic[raw[2]]['app_id'] = raw[2]
        try:
            dic[raw[2]]['category'] = raw[3]
        except:
            dic[raw[2]]['category'] = None
        try:
            dic[raw[2]]['Running'] = raw[4]
        except:
            dic[raw[2]]['Running'] = None

    if dic.get('app_id'):
        del dic['app_id']
    # print(len(dic.keys()))
    con = get_db_connection()

    lis = dic.keys()
    str2 = ''
                # new_list = []
    for i in lis:
        str2 = str2 +'"'+ i+'"'+','
    cur = con.cursor() 
    query = '''SELECT PackageId FROM APP_details WHERE PackageId in (''' +str2+''')'''
    query = query.replace(',)',')')
    cur.execute(query)  
    con.commit()
    rows = cur.fetchall() 
    # print(len(rows))
    insert_rows = []
    update_rows = []

    if len(rows) > 0 :
        for i in lis:
            if i in [j[0] for j in rows]:
                pass
                # update_rows.append("'"+str(i)+"'")

            else:
                # print("===in else==="*100)
                Name  = ''
                Running = dic.get(i).get('')
                Category = dic.get(i).get('category')
                version = ''
                country = ''
                minos = ''
                install = ''
                developer = ''
                SQL = "('"+i+"','"+str(Running)+"','"+str(Category)+"','"+str(version)+"','"+str(minos)+"','"+str(install)+"','"+str(developer)+ "')"
                # print('*'*100)
                # print(SQL)

                insert_rows.append(SQL)
    else:
        for i in lis:
            insert_rows.append(SQL)
    # print("---"*100)
    # print(insert_rows)
    # print("#"*100)
    # print(update_rows)
    if len(insert_rows) > 0:
        values = ', '.join(map(str, insert_rows))
        sql = "INSERT INTO APP_details VALUES {}".format(values)
        # print("*"*1000)
        # print(sql)
        cur = con.cursor() 
        cur.execute(sql)  
        con.commit()




