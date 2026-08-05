import requests

def database():
    print(" Enter number Or Cnic \n")
    target = input("[∆] Enter number : ")
    cookies = {
        '_ga_V41WE16XXG': 'GS2.1.s1784967958$o1$g0$t1784967958$j60$l0$h0',
        '_ga': 'GA1.1.286497115.1784967959',
        'PHPSESSID': 't7ho1ql83b17lk1au7gkmmdq5b',
    }
    headers = {
        'authority': 'paksim.xyz',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur-PK;q=0.8,ur;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://paksim.xyz',
        'referer': 'https://paksim.xyz/',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'q': target,
    }
    try:
        resp = requests.post(
            'https://paksim.xyz/psg-search.php',
            cookies=cookies, headers=headers, data=data
        )
        result = resp.json()

        # Check if API returned success
        if result.get("ok") and "data" in result:
            records = result["data"]
            if isinstance(records, list) and len(records) > 0:
                for item in records:
                    print("══════════════════════════════")
                    print(f" [*] Number      : {item.get('nbr', 'N/A')}")
                    print(f" [*] Name        : {item.get('nam', 'N/A')}")
                    print(f" [*] CNIC        : {item.get('cni', 'N/A')}")
                    print(f" [*] Address     : {item.get('adr', 'N/A')}")
                    print("══════════════════════════════\n")
            else:
                print("[!] No records found in data.")
        else:
            print(f"[!] API returned error or invalid response ")

    except Exception as e:
        print(f"[!] Error: {e}")

database()