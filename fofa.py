import requests,os,sys,base64,json,re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def fofa_work():
    config= os.path.abspath(os.path.dirname(__file__)) + '/config.ini'
    login= open(config,'r').readlines()
    email = str(login[2][6::]).encode('UTF-8').decode('UTF-8').replace("\n","")
    key = str(login[4][4::]).encode('UTF-8').decode('UTF-8').replace("\n","")
    fofa_txt = "./fofa.txt"
    fofa_dir = []
    with open(fofa_txt,encoding="UTF-8") as infile:
        while True:
            dirdic = infile.readline().strip()
            if(len(dirdic)==0):break
            fofa_dir.append(dirdic)
        for line in fofa_dir:
            cha_base64 = base64.b64encode(line.encode('UTF-8')).decode('UTF-8')
            size = 10000
            fofa_page= 1
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
            }
            url = "https://fofa.so/api/v1/search/all?email={}&key={}&qbase64={}&size={}&page={}&fields=ip,host,port,domain,title,country,province,city,country_name,server,protocol,banner,lastupdatetime".format(email,key,str(cha_base64),size,int(fofa_page))

            rs = requests.get(url,stream=True,allow_redirects=False,verify=False,headers=headers)
            rs_text = rs.text
            res = json.loads(rs_text)
            error = res['error']
            size = res['size']
            if error:
                errmsg = res['errmsg']
                if '401 Unauthorized' in errmsg:
                    print('警告','用户名或API 无效！或者是该账户未充值升级vip会员')
            ips = []
            hosts = []
            ports = []
            domains = []
            titles = []
            codes = []
            for i in res['results']:
                ip = i[0]
                ips.append(ip)
                host = i[1]
                if "http://" in host or "https://" in host:
                    pass
                else:
                    host = "http://"+host
                hosts.append(host)
                port = i[2]
                ports.append(port)
                domain = i[3]
                domains.append(domain)
                title = i[4]
                titles.append(title)
                code = i[11]
                zc = re.findall(r'<hr><center>(.*?)</center>',code,re.S)
                zc = str(zc).replace("[","").replace("]","").replace("'","").replace("'","")
                codes.append(zc)
                print(host)
            print(len(hosts))

            filename = 'target.txt'
            with open(filename, 'a') as file_object:
                file_object.write("\n".join(hosts))

if __name__ == "__main__":
    fofa_work()
