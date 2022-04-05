import requests, re, json, tqdm, os.path

# 1. Place cookie file from e.g. firefox extension while logged in to gumroad in this directory and name it cookies.txt
# 2. Make sure requirements are installed and LOCAL_PATH is adjusted and exists, also enter your CONTENT_URL


CONTENT_URL = "https://gumroad.com/d/c24cd29c161037a1808fae66d675b9e2" # sam hyde mde
DL_URL = CONTENT_URL.replace("/d/","/r/")
LOCAL_PATH = "/media/eight/bap/dl/"

def parseCookieFile(cookiefile):
    cookies = {}
    with open (cookiefile, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            if not re.match(r'^\# ', line) and len(line) > 10:
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies

session = requests.Session()
cookies = parseCookieFile("cookies.txt")
result = session.get(CONTENT_URL, cookies=cookies)
array = result.text.split("DownloadPage/FileList")
array = array[1].split("</div>")
array = array[0].replace("&quot;",'"')
array = array.split(' data-react-props="')[1]
array = array.split('" data-hydrate="t" data-react-cache-id="')[0]

for elem in tqdm.tqdm(json.loads(array)["files"]):
    filename = f'{LOCAL_PATH}{elem["file_name"]}.{elem["extension"]}'.replace(":","")
    if(os.path.isfile(filename)):
        pass
    else:
        r = requests.get(f"{DL_URL}/{elem['id']}", cookies=cookies, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(32 * 1024):
                f.write(chunk)