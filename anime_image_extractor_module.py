import time
import http_module
import menu_module
import url_to_file_module
import config

def gen_url(tags,page):
    if page > 1000 or page < 1:
        return(None)
    if len(tags) == 0:
        url = config.base_donmai_url + "/posts.json?page=" + str(page) + "&limit=200"
    elif len(tags) == 1:
        url = config.base_donmai_url + "/posts.json?page=" + str(page) + "&limit=200&tags=" + tags[0]
    elif len(tags) == 2:
        url = config.base_donmai_url + "/posts.json?page=" + str(page) + "&limit=200&tags=" + tags[0] + "+" + tags[1]
    else:
        print("invalid number of tags")
        return(None)
    return url

def get_image_url(json_file):
    ret = {}
    if not json_file == []:
        for element in json_file:
            if "file_url" in element:
                if "large_file_url" in element and ".zip" in element["file_url"]:
                    title = element["id"]
                    url = config.base_donmai_url + element["large_file_url"]
                    ret[title] = url
                else:
                    title = element["id"]
                    url = config.base_donmai_url + element["file_url"]
                    ret[title] = url
        return ret
    else:
        return (None)

def run_image_downloader():
    menu_module.run_menu()
    http_module.download_count = 0
    http_module.error_count = 0
    tags = ""
    for tag in config.tags:
        tags = tags + " " + tag
    print("--------------------------------------------------")
    print("Starting downloads for:" + tags)
    print("--------------------------------------------------" + "\n")
    page = 1
    elapsed_time = 4
    total_dict = {}
    while http_module.download_count < config.down_limit and page <= 1000:
        start_time = time.time()
        if elapsed_time < 4:
            time.sleep(4)
        url = gen_url(config.tags,page)
        json = http_module.get_json(url)
        img_dict = get_image_url(json)
        if img_dict is None:
            break
        http_module.download_img(img_dict, "image/" + tags, config.down_limit)
        page += 1
        elapsed_time = time.time() - start_time
        total_dict.update(img_dict)
    url_to_file_module.write_dict(tags, "image/url/" + tags, total_dict)
    print("--------------------------------------------------")
    print("Done downloading" + tags + " Error Count: " + str(http_module.error_count))
    print("--------------------------------------------------" + "\n")
