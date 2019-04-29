""" Here we are going to scrape krogers website and return a list of
    recent orders.
"""
import requests
import http.client
import time
import json

from .. import config_handler as config
from .. import utils
from .. import db_handler as db

def login_helper(s, headers):
    url = "https://www.kroger.com/resources/2f684f9498220a48b37d620bfcf736"

    payload = "{\"sensor_data\":\"7a74G7m23Vrp0o5c9075161.41-1,2,-94,-100,%s,uaend,12147,20030107,en-US,Gecko,3,0,0,0,382920,6104219,1920,1040,1920,1080,1920,517,1920,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:1,bat:1,x11:0,x12:1,8323,0.349519058174,778143052109,loc:-1,2,-94,-101,do_en,dm_en,t_en-1,2,-94,-105,0,-1,0,0,939,566,0;0,-1,0,0,1677,-1,0;1,2,0,0,2040,-1,0;-1,2,-94,-102,0,-1,0,0,939,566,0;0,-1,0,0,1677,-1,0;1,2,0,0,2040,-1,0;-1,2,-94,-108,0,2,780,16,0,4,-1;1,2,788,17,0,0,-1;-1,2,-94,-110,0,1,788,401,516;1,1,1583,296,515;2,1,1585,298,513;3,1,1586,299,512;4,1,1586,300,510;5,1,1587,300,509;6,1,1588,301,507;7,1,1589,301,506;8,1,1590,302,504;9,1,1591,304,503;10,1,1592,304,502;11,1,1593,305,501;12,1,1594,306,498;13,1,1595,306,497;14,1,1596,307,496;15,1,1597,307,495;16,1,1598,308,494;17,1,1599,310,493;18,1,1600,310,491;19,1,1601,311,490;20,1,1602,311,489;21,1,1603,312,488;22,1,1604,312,487;23,1,1605,313,486;24,1,1606,313,484;25,1,1607,314,483;26,1,1608,314,482;27,1,1609,315,479;28,1,1610,315,478;29,1,1611,315,477;30,1,1612,317,476;31,1,1613,317,475;32,1,1614,317,474;33,1,1615,318,472;34,1,1617,318,471;35,1,1617,318,470;36,1,1618,318,469;37,1,1619,319,468;38,1,1620,319,467;39,1,1621,320,465;40,1,1622,320,464;41,1,1623,320,463;42,1,1624,320,462;43,1,1625,321,461;44,1,1626,321,460;45,1,1627,321,458;46,1,1628,321,457;47,1,1629,321,456;48,1,1630,322,455;49,1,1631,322,454;50,1,1632,322,453;51,1,1633,322,451;52,1,1635,324,449;53,1,1635,324,448;54,1,1636,324,447;55,1,1637,324,445;56,1,1638,324,444;57,1,1639,325,443;58,1,1640,325,442;59,1,1641,325,441;60,1,1642,325,440;61,1,1643,325,438;62,1,1644,326,437;63,1,1645,326,435;64,1,1646,326,434;65,1,1648,326,432;66,1,1648,326,431;67,1,1649,326,430;68,1,1650,326,429;69,1,1651,327,429;70,1,1652,327,428;71,1,1653,327,427;72,1,1654,327,425;73,1,1655,327,424;74,1,1656,327,423;75,1,1657,327,422;76,1,1658,327,421;77,1,1659,327,420;78,1,1660,327,418;79,1,1661,327,417;80,1,1662,327,416;81,1,1663,327,415;82,1,1664,327,414;83,1,1666,327,413;84,1,1667,327,412;85,1,1669,327,410;86,1,1670,327,409;87,1,1672,327,408;88,1,1673,327,407;89,1,1675,327,406;90,1,1677,327,405;91,1,1680,327,403;92,1,1682,327,402;93,1,1683,326,401;94,1,1685,326,400;95,1,1688,326,399;96,1,1690,325,399;97,1,1691,325,398;98,1,1694,325,396;99,1,1701,325,395;166,3,2040,286,347,1677;169,4,2176,286,347,1677;170,2,2176,286,347,1677;171,3,2728,286,347,1677;172,4,2798,286,347,1677;173,2,2798,286,347,1677;298,3,3552,356,444,2040;301,4,3693,356,444,2040;302,2,3693,356,444,2040;303,3,3848,356,444,2040;304,4,3956,356,444,2040;305,2,3957,356,444,2040;306,3,4082,356,444,2040;307,4,4167,356,444,2040;308,2,4167,356,444,2040;309,3,4287,356,444,2040;310,4,4379,356,444,2040;311,2,4379,356,444,2040;312,3,4482,356,444,2040;313,4,4572,356,444,2040;314,2,4573,356,444,2040;315,3,4672,356,444,2040;316,4,4751,356,444,2040;317,2,4751,356,444,2040;318,3,4852,356,444,2040;319,4,4941,356,444,2040;320,2,4941,356,444,2040;783,3,12660,336,330,1677;-1,2,-94,-117,-1,2,-94,-111,0,57,-1,-1,-1;-1,2,-94,-109,0,55,-1,-1,-1,-1,-1,-1,-1,-1,-1;-1,2,-94,-114,-1,2,-94,-103,2,1364;3,2039;2,5889;3,12659;-1,2,-94,-112,https://www.kroger.com/signin?redirectUrl=/-1,2,-94,-115,1609,392575,0,57,55,0,394294,12660,0,1556286104218,4,16648,2,784,2774,19,0,12660,282234,1,2,50,801,-828908883,30261693-1,2,-94,-106,1,10-1,2,-94,-119,6,8,9,7,14,15,11,7,6,5,5,5,8,127,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-70,-1833641841;dis;,7,8;true;true;true;240;true;24;24;true;false;1-1,2,-94,-80,4958-1,2,-94,-116,30521140-1,2,-94,-118,182321-1,2,-94,-121,;1;14;0\"}" % headers['user-agent']

    return s.request("POST", url, data=payload, headers=headers)


def log_in(s, headers):
    s.request("GET", "https://www.kroger.com/signin?redirectUrl=/", headers=headers)
    login_helper(s, headers)
    payload = "{\n    \"email\": \"%s\",\n    \"password\": \"%s\",\n    \"rememberMe\": false\n}" % (config.get_value("kroger_username"), config.get_value("kroger_password"))
    response = s.request("POST", "https://www.kroger.com/auth/api/sign-in", data=payload, headers=headers)
    print(response.text)
    if (response.status_code == 403):
        login_helper(s, headers)
        response = s.request("POST", "https://www.kroger.com/auth/api/sign-in", data=payload, headers=headers)
    else:
        utils.log("Logged in with code %d" % response.status_code)
    print(response.status_code)
    return response.status_code
    
def get_results(s, headers):
    response = s.request("GET", "https://www.kroger.com/mypurchases/api/v1/receipt/summary/by-user-id", headers=headers)
    utils.log(response.text)
    print(("get_results %d" % response.status_code))
    j = json.loads(response.text)
    array = []
    for x in j:
        receiptId = x["receiptId"]
        
        userId = receiptId["userId"]
        storeNumber = receiptId["storeNumber"]
        transactionId = receiptId["transactionId"]
        if not db.is_receipt_generated(userId, storeNumber, transactionId):
            # Add it to the list we are returning
            array.append(receiptId)
            utils.log("Found receipt that hasn't been entered")
            print("Found receipt that hasn't been entered")
    return array
    
def get_receipt_results(s, headers, receipt):
    payload = "{\n    \"enhancedReceiptRequests\": [\n        {\n        \t\"userId\": \"%s\",\n            \"divisionNumber\": \"%s\",\n            \"storeNumber\": \"%s\",\n            \"transactionDate\": \"%s\",\n            \"terminalNumber\": \"%s\",\n            \"transactionId\": \"%s\",\n            \"shoppingContextDivision\": \"%s\",\n            \"shoppingContextStore\": \"%s\"\n        }\n    ]\n}" % (receipt["userId"], receipt["divisionNumber"], receipt["storeNumber"], receipt["transactionDate"], receipt["terminalNumber"], receipt["transactionId"], receipt["divisionNumber"], receipt["storeNumber"])

    response = s.request("POST", "https://www.kroger.com/mypurchases/api/v1/receipt/details", data=payload, headers=headers)
    utils.log("get receipt result code %d" % response.status_code)
    print(("get receipt result code %d" % response.status_code))
    data = {}
    data['receipt'] = receipt
    data['data'] = json.loads(response.text)
    return data
    
def get_valid_data():
    # Get kroger log in url
    headers = {
    'Content-Type': "application/json;charset=UTF-8",
    'user-agent': utils.random_useragent(),
    'cache-control': "no-cache",
    "referer": "https://www.kroger.com/signin?redirectUrl=/",
    "origin": "https://www.kroger.com",
    "authority": "www.kroger.com",
    "accept-language": "en-US,en;q=0.9",
    "upgrade-insecure-requests": "1"
    }
    with requests.Session() as s:
        if log_in(s, headers) == 200:
            time.sleep(2)
            results = get_results(s, headers)
            # Now we want to get the specifics on each receipt and return that
            data = []
            for receipt in results:
                data.append(get_receipt_results(s, headers, receipt))
            utils.log(str(data).encode("utf-8"))
            return data

def main():
    # Get kroger log in url
    headers = {
    'Content-Type': "application/json;charset=UTF-8",
    'user-agent': utils.random_useragent(),
    'cache-control': "no-cache",
    "referer": "https://www.kroger.com/signin?redirectUrl=/",
    "origin": "https://www.kroger.com",
    "authority": "www.kroger.com",
    "accept-language": "en-US,en;q=0.9",
    "upgrade-insecure-requests": "1"
    }
    with requests.Session() as s:
        if log_in(s, headers) == 200:
            time.sleep(2)
            results = get_results(s, headers)
            # Now we want to get the specifics on each receipt and return that
            data = []
            for receipt in results:
                data.append(get_receipt_results(s, headers, receipt))
            utils.log(str(data))
            print(str(data).encode("utf-8"))

if __name__ == '__main__':
    main()