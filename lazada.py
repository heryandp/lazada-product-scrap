# Lazada Product Scrapper v1.0
# heryandp
# https://github.com/heryandp

import requests as req
import os,glob, json,csv,time

# Base Url
base_url = "https://www.lazada.co.id/"

class lazada():
    def __init__(self, usernametoko):
        self.tokourl = base_url+usernametoko
        self.namatoko = usernametoko
        self.headerbrowser = {"User-Agent": "Mozilla/7.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        self.cookies = {"__wpkreporterwid_":"a36251fe-f6a0-40b6-20c4-4e8bb1b67ee8", "lzd_cid":"eac145b5-9666-43e4-e378-7cdc5f5021ce", "t_uid":"eac145b5-9666-43e4-e378-7cdc5f5021ce", "userLanguageML":"id", "lzd_sid":"19e1fea8be3808bf45c289a4e5bf0641", "_tb_token_":"7ee338d57a93d", "_bl_uid":"v3l5e6UI4LsxILq0yssCszLt01k2", "t_fv":"1659006682481", "miidlaz":"miidgg3a8t1g928224h36mm", "hng":"ID|id-ID|IDR|360","hng.sig":"to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8","EGG_SESS":"S_Gs1wHo9OvRHCMp98md7H-1EVQqDTv0NmqIeZvLuy7d9138RaicIjUip-xT3QW3mMiNB23xFyYfLvr6_ZPIZ4hzQ1gWpBHOHDBrbMPS6_kszbQP1xgvS_wvVE5C65GYkJLVD_Ri8DdUANwOsw9M2jyo5wBc1SCXSuwsmHjGpU0","_m_h5_tk":"fa0055fb1658798e1d1712cfe1dfe3f0_1659105513974","_m_h5_tk_enc":"8aeb6052e54a49839803113311a6e815","exlaz":"c_lzd_byr:mm_150030203_51200509_2010250508!id1585001:clkgi4al81g9520ov2opvc::","lzd_click_id":"clkgi4al81g9520ov2opvc","t_sid":"5RSL9j70JEfvIOj6zcBl3EbRu2TWRLXI","utm_channel":"NA","x5sec":"7b22617365727665722d6c617a6164613b32223a22383638616135356365633661383231616461333334376535346266643135383343496a436a356347454c50743666577876343676787745776e4f484873674e4141773d3d227d","l":"eBSL3I7rgEZ-q0hkBO5w-urza77tyLdfCsPzaNbMiInca6tVKQRo1NCHmb2MjdtjQt5bretzmMuaidh2r0aU-AMQcn-gxdARfTvB-e1..","isg":"BGZm2HQ6OBJILe9KEKL7Njz8t9zoR6oBYkbHVVAE6ggO0wPtuNKHEI_pK9ff-6IZ"}
        self.grab_produk()

    def grab_produk(self):
        print("=== GRABBING PRODUK ===")
        try:
            print("[+] Grab ID Seller ...")
            t_url_seller = self.tokourl+"/?ajax=true&from=wangpu&langFlag=id&page=1&pageTypeId=2&q=All-Products&style=list"
            t_pg_seller = req.get(t_url_seller,headers=self.headerbrowser,cookies=self.cookies,timeout=3000)
            t_data_seller = t_pg_seller.json()
            self.shopId = t_data_seller['mainInfo']['selectedFilters']['shopId']
            print('-> ',t_data_seller['mainInfo']['pageTitle']+" / "+t_data_seller['mainInfo']['selectedFilters']['shopId'])
        except:
            print("[!] Gagal mendapatkan ID Seller")
            exit()

        print("[+] Hapus file lama ...")
        if not os.path.exists("data"):
            os.makedirs("data")
        for filename in glob.glob("data/"+self.shopId+"_lazada*.json"):
            os.remove(filename)
        for filename in glob.glob(self.shopId+"_lazada.csv"):
            os.remove(filename)
        print("[+] Mulai download halaman ...")
        print("\x1B[3m" +"(delay 3 detik untuk menghindari anti-spam!)"+"\x1B[0m")
        i = 1
        while(True):
            print("-> download halaman "+ str(i))
            url_seller = self.tokourl+"/?ajax=true&from=wangpu&langFlag=id&page="+str(i)+"&pageTypeId=2&q=All-Products&style=list"
            pg_seller = req.get(url_seller,headers=self.headerbrowser,cookies=self.cookies,timeout=3000)
            pg_product = pg_seller.json()
            if pg_product['mainInfo']['totalResults'] == "0":
                break
            else:
                with open('data/'+self.shopId+"_lazada_"+str(i)+'.json','w',encoding='utf-8') as dmp:
                    json.dump(pg_product['mods']['listItems'],dmp)
            i = i+1
            time.sleep(2)
            
        # merging json
        print("[+] Merging data produk ...")
        data = []
        for f in glob.glob('data/'+self.shopId+'_lazada*.json'):
            with open(f,) as infile:
                data.extend(json.load(infile))
        with open('data/'+self.shopId+'_lazada_all.json','w') as outfile:
            json.dump(data, outfile)

        # create csv
        print("[+] Membuat csv data produk ...")
        f_data = []
        f = open('data/'+self.shopId+'_lazada_all.json')
        f_read = json.load(f)
        for i in f_read:
            try:
                p_now = int(float(i['price']))
                p_ori = int(float(i['originalPrice']))
                discount = (p_ori-p_now)/p_ori*100
            except KeyError:
                p_ori = p_now
                discount = 0
                
            f_data.append([
                i['sellerName'],
                i['itemId'],
                i['name'],
                i['image'],
                p_now,
                p_ori,
                discount,
                i['review'],
                i['ratingScore'],
                i['brandName'],
                i['itemUrl']
                ])
        f_header = ['seller','itemid','produk','image','harga','harga_ori','discount','ulasan','rating','brand','url']
        with open(self.shopId+'_lazada.csv', 'w',newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(f_header)
            writer.writerows(f_data)
        f.close()
        print("done! "+self.shopId+"_lazada.csv")

print("[ LAZADA-PRODUCT-GRABBER v1.0 by heryan ]")
print("[+] https://github.com/heryandp/lazada-product-scrap")
sname = input("[+] Masukkan username seller: https://www.lazada.co.id/")        
print("")
act = lazada(sname)