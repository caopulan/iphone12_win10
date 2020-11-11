import requests
from config import *
import time
from win10toast import ToastNotifier


def get_Stores():
    headers = {"Refer": "https://reserve-prime.apple.com/CN/zh_CN/reserve/G/availability?&iUP=N",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"}
    url = "https://reserve-prime.apple.com/CN/zh_CN/reserve/G/stores.json"
    r = requests.get(url, headers=headers).json()["stores"]
    stores_dict = {}
    for store in r:
        stores_dict[store["storeNumber"]] = {"city": store["city"],
                                             "storeName": store["storeName"]}
    return stores_dict


Stores = get_Stores()
Beijing_Stores = [i for i in Stores.keys() if Stores[i]["city"] == "北京"]


def store_name(x): return Stores[x]["storeName"]


def get_Kucun(model_code, stores_list):
    url = f"https://reserve-prime.apple.com/CN/zh_CN/reserve/{model_code}/availability.json"
    try:
        r = requests.get(url).json()["stores"]
    except BaseException:
        return []

    success = []

    for store in stores_list:
        status = r[store]
        for model, availability in status.items():
            if availability["availability"]["contract"] == True and availability["availability"]["unlocked"] == True:
                success.append([store_name(store), colorCode[model]])
    return success


def main():
    count = 0
    while True:
        for model in models:
            # print(time.time())
            kucun = get_Kucun(model, Beijing_Stores)
            if kucun:
                text = ""
                for k in kucun:
                    text += k[0] + "-" + k[1] + "\n"
                print(text)
                toaster.show_toast(
                    "Hello World!!!", text, duration=10, threaded=True)

        count += 1
        print(count, time.time())
        time.sleep(1)


if __name__ == '__main__':
    toaster = ToastNotifier()
    models = ["A"]
    main()
