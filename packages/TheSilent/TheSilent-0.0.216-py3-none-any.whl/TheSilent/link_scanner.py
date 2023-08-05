from TheSilent.clear import *
from TheSilent.return_user_agent import *

import hashlib
import re
import requests

cyan = "\033[1;36m"
red = "\033[1;31m"

tor_proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}

#create html sessions object
web_session = requests.Session()

#fake user agent
user_agent = {"User-Agent" : return_user_agent()}

#increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

#increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

#crawls a website looking for links
def link_scanner(url, secure = True, tor = False, depth = 1, my_file = " ", crawl = "all", parse = " "):
    #crawl all!
    if crawl == "all":
        if secure == True:
            my_secure = "https://"

        if secure == False:
            my_secure = "http://"

        my_url = my_secure + url
        tracker = -1

        hash_list = []
        mal_links = []
        website_list = []
        website_list.append(my_url)

        clear()

        while True:
            hash_boolean = False
            length_count = 0

            counter = -1

            if parse != " ":
                while website_list:
                    counter += 1

                    try:
                        if parse not in website_list[counter]:
                            website_list.pop(counter)
                            counter -= 1

                    except IndexError:
                        break

            counter = -1

            if depth != "all":
                while website_list:
                    counter += 1

                    try:
                        if website_list[counter].count("/") - 2 > depth:
                            website_list.pop(counter)
                            counter -= 1

                    except IndexError:
                        break
                    
            try:
                tracker += 1

                if website_list[tracker] == "http://" or website_list[tracker] == "https://":
                    website_list.pop(tracker)
                    tracker -= 1

                if website_list[tracker].endswith("/"):
                    url_regex = re.findall("http://\S+?/|https://\S+?/", website_list[tracker])
                    my_url = url_regex[0]
                    url = url_regex[0]

                if not website_list[tracker].endswith("/"):
                    url_regex = re.findall("http://\S+?/|https://\S+?/", website_list[tracker] + "/")
                    my_url = url_regex[0]
                    url = url_regex[0]

                #crawl all links
                if url in website_list[tracker] or not url in website_list[tracker]:
                    if depth == "all":
                        website_list = list(dict.fromkeys(website_list))
                        
                        mal_boolean = False
                        
                        for mal in mal_links:
                            if mal == website_list[tracker]:
                                mal_boolean = True
                                website_list.pop(tracker)
                                tracker -= 1

                        find_my = re.search("https://\S+|http://\S+", str(website_list[tracker]))

                        if find_my and mal_boolean == False or website_list[tracker] == my_url and mal_boolean == False:
                            length_count = 0
                            
                            if tor == True:
                                stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120), stream = True)

                                for i in stream_boolean.iter_lines():
                                    length_count += len(i)

                            if tor == False:
                                stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

                                for i in stream_boolean.iter_lines():
                                    length_count += len(i)

                            if length_count > 100000000:
                                print(red + "too long" + ": " + str(website_list[tracker]))
                                mal_links.append(str(website_list[tracker]))
                                website_list.pop(tracker)
                                tracker -= 1

                            if length_count <= 100000000:
                                if tor == True:
                                    status = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).status_code

                                if tor == False:
                                    status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                                if status == 200 or status == 404:
                                    print(cyan + website_list[tracker])

                                    if tor == True:
                                        my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).text

                                    if tor == False:
                                        my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                                    sha1 = hashlib.sha1(my_request.encode("utf8")).hexdigest()

                                    for i in hash_list:
                                        if i == sha1:
                                            website_list.pop(tracker)
                                            print(red + "ERROR! Duplicate hash!")
                                            hash_boolean = True
                                            tracker -= 1
                                            break

                                    if hash_boolean == False:
                                        hash_list.append(sha1)

                                        if len(my_request) <= 100000000:
                                            #urls
                                            website = re.findall("http://|https://\S+", my_request)
                                            website = list(dict.fromkeys(website))

                                            for i in website:
                                                try:
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]
                                                    result = re.sub("[\"\']", "", result)

                                                except:
                                                    result = i
                                                    
                                                if url in i or not url in i:
                                                    website_list.append(re.sub("[\\\"\']", "", result))

                                            #href
                                            href = re.sub(" ", "", my_request)
                                            href = re.findall("href\s*=\s*[\"\']\S+?[\'\"]", href)
                                            href = list(dict.fromkeys(href))
                                            for i in href:
                                                try:
                                                    i = i.clean(" ", "")
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]

                                                except:
                                                    result = i
                                                
                                                result = re.sub("[\\\"\';=\s]|href", "", i)

                                                if result.startswith("http"):
                                                    if url in result or not url in result:
                                                        website_list.append(result)

                                                if result.startswith("http") == False and result[0] != "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + "/" + result)

                                                if result.startswith("http") == False and result[0] == "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + result)

                                            #action
                                            action = re.sub(" ", "", my_request)
                                            action = re.findall("action\s*=\s*[\"\']\S+?[\'\"]", action)
                                            action = list(dict.fromkeys(action))
                                            
                                            for i in action:
                                                try:
                                                    i = i.clean(" ", "")
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]

                                                except:
                                                    result = i
                                                    
                                                result = re.sub("[\\\"\';=\s]|action", "", i)

                                                if result.startswith("http"):
                                                    if url in result or not url in result:
                                                        website_list.append(result)

                                                if result.startswith("http") == False and result[0] != "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + "/" + result)

                                                if result.startswith("http") == False and result[0] == "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + result)

                                            #src
                                            src = re.sub(" ", "", my_request)
                                            src = re.findall("src\s*=\s*[\"\']\S+?[\'\"]", src)
                                            src = list(dict.fromkeys(src))

                                            for i in src:
                                                try:
                                                    i = i.clean(" ", "")
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]

                                                except:
                                                    result = i
                                                    
                                                result = re.sub("[\\\"\';=\s]|src", "", i)
                                                
                                                if result.startswith("http"):
                                                    if url in result or not url in result:
                                                        website_list.append(result)

                                                if result.startswith("http") == False and result[0] != "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + "/" + result)

                                                if result.startswith("http") == False and result[0] == "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + result)

                                            #slash
                                            slash = re.findall("[\'|\"]/\S+[\"|\']", my_request)

                                            for i in slash:
                                                my_search = re.search("http|\.com|\.edu|\.net|\.org|\.tv|www|http", i)

                                                if not my_search:
                                                    result = re.sub("[\"\']", "", i)
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", result)
                                                    result = result[0]
                                                    website_list.append(my_url + result)

                                else:
                                    print(red + str(status) + ": " + str(website_list[tracker]))
                                    mal_links.append(str(website_list[tracker]))
                                    website_list.pop(tracker)
                                    tracker -= 1

                        if not find_my:
                            mal_links.append(str(website_list[tracker]))
                            website_list.pop(tracker)
                            tracker -= 1
                            
                #crawl where depth is not equal to all
                if url in website_list[tracker] or not url in website_list[tracker]:
                    if depth != "all":
                        if website_list[tracker].count("/") - 2 <= depth:
                            website_list = list(dict.fromkeys(website_list))
                            
                            mal_boolean = False
                            
                            for mal in mal_links:
                                if mal == website_list[tracker]:
                                    mal_boolean = True
                                    website_list.pop(tracker)
                                    tracker -= 1

                            find_my = re.search("https://|http://", str(website_list[tracker]))

                            if find_my and mal_boolean == False or website_list[tracker] == my_url and mal_boolean == False:
                                if tor == True:
                                    stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120), stream = True)

                                    for i in stream_boolean.iter_lines():
                                        length_count += len(i)

                                else:
                                    stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

                                    for i in stream_boolean.iter_lines():
                                        length_count += len(i)

                                if length_count > 100000000:
                                    print(red + "too long" + ": " + str(website_list[tracker]))
                                    mal_links.append(str(website_list[tracker]))
                                    website_list.pop(tracker)
                                    tracker -= 1

                                if length_count <= 100000000:
                                    if tor == True:
                                        status = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).status_code

                                    if tor == False:
                                        status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                                    if status == 200 or status == 404:
                                        print(cyan + website_list[tracker])

                                        if tor == True:
                                            my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).text

                                        if tor == False:
                                            my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                                        sha1 = hashlib.sha1(my_request.encode("utf8")).hexdigest()

                                        for i in hash_list:
                                            if i == sha1:
                                                website_list.pop(tracker)
                                                print(red + "ERROR! Duplicate hash!")
                                                hash_boolean = True
                                                tracker -= 1
                                                break

                                        if hash_boolean == False:
                                            hash_list.append(sha1)
                                            
                                            if len(my_request) <= 100000000:
                                                #urls
                                                website = re.findall("http://|https://\S+", my_request)
                                                website = list(dict.fromkeys(website))

                                                for i in website:
                                                    try:
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]
                                                        result = re.sub("[\"\']", "", result)

                                                    except:
                                                        result = i
                                                        
                                                    if url in i or not url in i:
                                                        website_list.append(re.sub("[\\\"\']", "", result))

                                                #href
                                                href = re.sub(" ", "", my_request)
                                                href = re.findall("href\s*=\s*[\"\']\S+?[\'\"]", href)
                                                href = list(dict.fromkeys(href))
                                                for i in href:
                                                    try:
                                                        i = i.clean(" ", "")
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]

                                                    except:
                                                        result = i
                                                    
                                                    result = re.sub("[\\\"\';=\s]|href", "", i)

                                                    if result.startswith("http"):
                                                        if url in result or not url in result:
                                                            website_list.append(result)

                                                    if result.startswith("http") == False and result[0] != "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + "/" + result)

                                                    if result.startswith("http") == False and result[0] == "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + result)

                                                #action
                                                action = re.sub(" ", "", my_request)
                                                action = re.findall("action\s*=\s*[\"\']\S+?[\'\"]", action)
                                                action = list(dict.fromkeys(action))
                                                
                                                for i in action:
                                                    try:
                                                        i = i.clean(" ", "")
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]

                                                    except:
                                                        result = i
                                                        
                                                    result = re.sub("[\\\"\';=\s]|action", "", i)

                                                    if result.startswith("http"):
                                                        if url in result or not url in result:
                                                            website_list.append(result)

                                                    if result.startswith("http") == False and result[0] != "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + "/" + result)

                                                    if result.startswith("http") == False and result[0] == "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + result)

                                                #src
                                                src = re.sub(" ", "", my_request)
                                                src = re.findall("src\s*=\s*[\"\']\S+?[\'\"]", src)
                                                src = list(dict.fromkeys(src))

                                                for i in src:
                                                    try:
                                                        i = i.clean(" ", "")
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]

                                                    except:
                                                        result = i
                                                        
                                                    result = re.sub("[\\\"\';=\s]|src", "", i)
                                                    
                                                    if result.startswith("http"):
                                                        if url in result or not url in result:
                                                            website_list.append(result)

                                                    if result.startswith("http") == False and result[0] != "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + "/" + result)

                                                    if result.startswith("http") == False and result[0] == "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + result)

                                                #slash
                                                slash = re.findall("[\'|\"]/\S+[\"|\']", my_request)

                                                for i in slash:
                                                    my_search = re.search("http|\.com|\.edu|\.net|\.org|\.tv|www|http", i)

                                                    if not my_search:
                                                        result = re.sub("[\"\']", "", i)
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", result)
                                                        result = result[0]
                                                        website_list.append(my_url + result)

                                    else:
                                        print(red + str(status) + ": " + str(website_list[tracker]))
                                        mal_links.append(str(website_list[tracker]))
                                        website_list.pop(tracker)
                                        tracker -= 1
                                        
                    if not find_my:
                        mal_links.append(str(website_list[tracker]))
                        website_list.pop(tracker)
                        tracker -= 1
                        
            except IndexError:
                break

            except:
                print(red + "ERROR: " + str(website_list[tracker]))
                mal_links.append(str(website_list[tracker]))
                website_list.pop(tracker)
                tracker -= 1
                
        if parse == " ":
            website_list = list(dict.fromkeys(website_list))
            website_list.sort()

            clear()

            if my_file != " ":
                with open(my_file, "a") as file:
                    for i in website_list:
                        file.write(i + "\n")

            return website_list

        if parse != " ":
            website_list = list(dict.fromkeys(website_list))
            website_list.sort()

            my_list = []

            for i in website_list:
                if parse in i:
                    my_list.append(i)

            my_list = list(dict.fromkeys(my_list))
            my_list.sort()

            clear()

            if my_file != " ":
                with open(my_file, "a") as file:
                    for i in my_list:
                        file.write(i + "\n")

            return my_list

    #crawl 1
    if crawl != "all":
        if secure == True:
            my_secure = "https://"

        if secure == False:
            my_secure = "http://"

        my_url = my_secure + url
        tracker = -1

        hash_list = []
        mal_links = []
        website_list = []
        website_list.append(my_url)

        clear()

        while True:
            hash_boolean = False
            length_count = 0

            counter = -1

            if parse != " ":
                while website_list:
                    counter += 1

                    try:
                        if parse not in website_list[counter]:
                            website_list.pop(counter)
                            counter -= 1

                    except IndexError:
                        break

            counter = -1

            if depth != "all":
                while website_list:
                    counter += 1

                    try:
                        if website_list[counter].count("/") - 2 > depth:
                            website_list.pop(counter)
                            counter -= 1

                    except IndexError:
                        break
                    
            try:
                tracker += 1

                if website_list[tracker] == "http://" or website_list[tracker] == "https://":
                    website_list.pop(tracker)
                    tracker -= 1
                    
                if tracker >= crawl:
                    break

                if website_list[tracker].endswith("/"):
                    url_regex = re.findall("http://\S+?/|https://\S+?/", website_list[tracker])
                    my_url = url_regex[0]
                    url = url_regex[0]

                if not website_list[tracker].endswith("/"):
                    url_regex = re.findall("http://\S+?/|https://\S+?/", website_list[tracker] + "/")
                    my_url = url_regex[0]
                    url = url_regex[0]

                #crawl all links
                if url in website_list[tracker] or not url in website_list[tracker]:
                    if depth == "all":
                        website_list = list(dict.fromkeys(website_list))
                        
                        mal_boolean = False
                        
                        for mal in mal_links:
                            if mal == website_list[tracker]:
                                mal_boolean = True
                                website_list.pop(tracker)
                                tracker -= 1

                        find_my = re.search("https://\S+|http://\S+", str(website_list[tracker]))

                        if find_my and mal_boolean == False or website_list[tracker] == my_url and mal_boolean == False:
                            length_count = 0
                            
                            if tor == True:
                                stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120), stream = True)

                                for i in stream_boolean.iter_lines():
                                    length_count += len(i)

                            if tor == False:
                                stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

                                for i in stream_boolean.iter_lines():
                                    length_count += len(i)

                            if length_count > 100000000:
                                print(red + "too long" + ": " + str(website_list[tracker]))
                                mal_links.append(str(website_list[tracker]))
                                website_list.pop(tracker)
                                tracker -= 1

                            if length_count <= 100000000:
                                if tor == True:
                                    status = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).status_code

                                if tor == False:
                                    status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                                if status == 200 or status == 404:
                                    print(cyan + website_list[tracker])

                                    if tor == True:
                                        my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).text

                                    if tor == False:
                                        my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                                    sha1 = hashlib.sha1(my_request.encode("utf8")).hexdigest()

                                    for i in hash_list:
                                        if i == sha1:
                                            website_list.pop(tracker)
                                            print(red + "ERROR! Duplicate hash!")
                                            hash_boolean = True
                                            tracker -= 1
                                            break

                                    if hash_boolean == False:
                                        hash_list.append(sha1)

                                        if len(my_request) <= 100000000:
                                            #urls
                                            website = re.findall("http://|https://\S+", my_request)
                                            website = list(dict.fromkeys(website))

                                            for i in website:
                                                try:
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]
                                                    result = re.sub("[\"\']", "", result)

                                                except:
                                                    result = i
                                                    
                                                if url in i or not url in i:
                                                    website_list.append(re.sub("[\\\"\']", "", result))

                                            #href
                                            href = re.sub(" ", "", my_request)
                                            href = re.findall("href\s*=\s*[\"\']\S+?[\'\"]", href)
                                            href = list(dict.fromkeys(href))
                                            for i in href:
                                                try:
                                                    i = i.clean(" ", "")
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]

                                                except:
                                                    result = i
                                                
                                                result = re.sub("[\\\"\';=\s]|href", "", i)

                                                if result.startswith("http"):
                                                    if url in result or not url in result:
                                                        website_list.append(result)

                                                if result.startswith("http") == False and result[0] != "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + "/" + result)

                                                if result.startswith("http") == False and result[0] == "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + result)

                                            #action
                                            action = re.sub(" ", "", my_request)
                                            action = re.findall("action\s*=\s*[\"\']\S+?[\'\"]", action)
                                            action = list(dict.fromkeys(action))
                                            
                                            for i in action:
                                                try:
                                                    i = i.clean(" ", "")
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]

                                                except:
                                                    result = i
                                                    
                                                result = re.sub("[\\\"\';=\s]|action", "", i)

                                                if result.startswith("http"):
                                                    if url in result or not url in result:
                                                        website_list.append(result)

                                                if result.startswith("http") == False and result[0] != "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + "/" + result)

                                                if result.startswith("http") == False and result[0] == "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + result)

                                            #src
                                            src = re.sub(" ", "", my_request)
                                            src = re.findall("src\s*=\s*[\"\']\S+?[\'\"]", src)
                                            src = list(dict.fromkeys(src))

                                            for i in src:
                                                try:
                                                    i = i.clean(" ", "")
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                    result = result[0]

                                                except:
                                                    result = i
                                                    
                                                result = re.sub("[\\\"\';=\s]|src", "", i)
                                                
                                                if result.startswith("http"):
                                                    if url in result or not url in result:
                                                        website_list.append(result)

                                                if result.startswith("http") == False and result[0] != "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + "/" + result)

                                                if result.startswith("http") == False and result[0] == "/":
                                                    result = re.sub(url, "", result)
                                                    result = re.sub("www", "", result)
                                                    website_list.append(my_url + result)

                                            #slash
                                            slash = re.findall("[\'|\"]/\S+[\"|\']", my_request)

                                            for i in slash:
                                                my_search = re.search("http|\.com|\.edu|\.net|\.org|\.tv|www|http", i)

                                                if not my_search:
                                                    result = re.sub("[\"\']", "", i)
                                                    result = re.split("[%\(\)<>\[\],\{\};�|]", result)
                                                    result = result[0]
                                                    website_list.append(my_url + result)

                                else:
                                    print(red + str(status) + ": " + str(website_list[tracker]))
                                    mal_links.append(str(website_list[tracker]))
                                    website_list.pop(tracker)
                                    tracker -= 1

                        if not find_my:
                            mal_links.append(str(website_list[tracker]))
                            website_list.pop(tracker)
                            tracker -= 1
                            
                #crawl where depth is not equal to all
                if url in website_list[tracker] or not url in website_list[tracker]:
                    if depth != "all":
                        if website_list[tracker].count("/") - 2 <= depth:
                            website_list = list(dict.fromkeys(website_list))
                            
                            mal_boolean = False
                            
                            for mal in mal_links:
                                if mal == website_list[tracker]:
                                    mal_boolean = True
                                    website_list.pop(tracker)
                                    tracker -= 1

                            find_my = re.search("https://|http://", str(website_list[tracker]))

                            if find_my and mal_boolean == False or website_list[tracker] == my_url and mal_boolean == False:
                                if tor == True:
                                    stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120), stream = True)

                                    for i in stream_boolean.iter_lines():
                                        length_count += len(i)

                                else:
                                    stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

                                    for i in stream_boolean.iter_lines():
                                        length_count += len(i)

                                if length_count > 100000000:
                                    print(red + "too long" + ": " + str(website_list[tracker]))
                                    mal_links.append(str(website_list[tracker]))
                                    website_list.pop(tracker)
                                    tracker -= 1

                                if length_count <= 100000000:
                                    if tor == True:
                                        status = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).status_code

                                    if tor == False:
                                        status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                                    if status == 200 or status == 404:
                                        print(cyan + website_list[tracker])

                                        if tor == True:
                                            my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (60, 120)).text

                                        if tor == False:
                                            my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                                        sha1 = hashlib.sha1(my_request.encode("utf8")).hexdigest()

                                        for i in hash_list:
                                            if i == sha1:
                                                website_list.pop(tracker)
                                                print(red + "ERROR! Duplicate hash!")
                                                hash_boolean = True
                                                tracker -= 1
                                                break

                                        if hash_boolean == False:
                                            hash_list.append(sha1)
                                            
                                            if len(my_request) <= 100000000:
                                                #urls
                                                website = re.findall("http://|https://\S+", my_request)
                                                website = list(dict.fromkeys(website))

                                                for i in website:
                                                    try:
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]
                                                        result = re.sub("[\"\']", "", result)

                                                    except:
                                                        result = i
                                                        
                                                    if url in i or not url in i:
                                                        website_list.append(re.sub("[\\\"\']", "", result))

                                                #href
                                                href = re.sub(" ", "", my_request)
                                                href = re.findall("href\s*=\s*[\"\']\S+?[\'\"]", href)
                                                href = list(dict.fromkeys(href))
                                                for i in href:
                                                    try:
                                                        i = i.clean(" ", "")
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]

                                                    except:
                                                        result = i
                                                    
                                                    result = re.sub("[\\\"\';=\s]|href", "", i)

                                                    if result.startswith("http"):
                                                        if url in result or not url in result:
                                                            website_list.append(result)

                                                    if result.startswith("http") == False and result[0] != "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + "/" + result)

                                                    if result.startswith("http") == False and result[0] == "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + result)

                                                #action
                                                action = re.sub(" ", "", my_request)
                                                action = re.findall("action\s*=\s*[\"\']\S+?[\'\"]", action)
                                                action = list(dict.fromkeys(action))
                                                
                                                for i in action:
                                                    try:
                                                        i = i.clean(" ", "")
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]

                                                    except:
                                                        result = i
                                                        
                                                    result = re.sub("[\\\"\';=\s]|action", "", i)

                                                    if result.startswith("http"):
                                                        if url in result or not url in result:
                                                            website_list.append(result)

                                                    if result.startswith("http") == False and result[0] != "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + "/" + result)

                                                    if result.startswith("http") == False and result[0] == "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + result)

                                                #src
                                                src = re.sub(" ", "", my_request)
                                                src = re.findall("src\s*=\s*[\"\']\S+?[\'\"]", src)
                                                src = list(dict.fromkeys(src))

                                                for i in src:
                                                    try:
                                                        i = i.clean(" ", "")
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                                        result = result[0]

                                                    except:
                                                        result = i
                                                        
                                                    result = re.sub("[\\\"\';=\s]|src", "", i)
                                                    
                                                    if result.startswith("http"):
                                                        if url in result or not url in result:
                                                            website_list.append(result)

                                                    if result.startswith("http") == False and result[0] != "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + "/" + result)

                                                    if result.startswith("http") == False and result[0] == "/":
                                                        result = re.sub(url, "", result)
                                                        result = re.sub("www", "", result)
                                                        website_list.append(my_url + result)

                                                #slash
                                                slash = re.findall("[\'|\"]/\S+[\"|\']", my_request)

                                                for i in slash:
                                                    my_search = re.search("http|\.com|\.edu|\.net|\.org|\.tv|www|http", i)

                                                    if not my_search:
                                                        result = re.sub("[\"\']", "", i)
                                                        result = re.split("[%\(\)<>\[\],\{\};�|]", result)
                                                        result = result[0]
                                                        website_list.append(my_url + result)

                                    else:
                                        print(red + str(status) + ": " + str(website_list[tracker]))
                                        mal_links.append(str(website_list[tracker]))
                                        website_list.pop(tracker)
                                        tracker -= 1
                                        
                    if not find_my:
                        mal_links.append(str(website_list[tracker]))
                        website_list.pop(tracker)
                        tracker -= 1
                        
            except IndexError:
                break

            except:
                print(red + "ERROR: " + str(website_list[tracker]))
                mal_links.append(str(website_list[tracker]))
                website_list.pop(tracker)
                tracker -= 1
                
        if parse == " ":
            website_list = list(dict.fromkeys(website_list))
            website_list.sort()

            clear()

            if my_file != " ":
                with open(my_file, "a") as file:
                    for i in website_list:
                        file.write(i + "\n")

            return website_list

        if parse != " ":
            website_list = list(dict.fromkeys(website_list))
            website_list.sort()

            my_list = []

            for i in website_list:
                if parse in i:
                    my_list.append(i)

            my_list = list(dict.fromkeys(my_list))
            my_list.sort()

            clear()

            if my_file != " ":
                with open(my_file, "a") as file:
                    for i in my_list:
                        file.write(i + "\n")

            return my_list
