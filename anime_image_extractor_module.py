import time
import http_module
import menu_module
import url_to_file_module
import config

def gen_url(tags,page):
    if page > 1000 or page < 1:
        return(None)
    url = config.base_donmai_url + "/posts.json?page=" + str(page) + "&limit=200&tags=" + tags
    return url

def get_image_url(json_file):
    ret = {}
    if not json_file == []:
        for element in json_file:
            if "file_url" in element:
                if "large_file_url" in element and ".zip" in element["file_url"] and ".zip" not in element["large_file_url"] and element["is_deleted"] is False:
                    title = element["id"]
                    url = config.base_donmai_url + element["large_file_url"]
                    ret[title] = url
                elif ".zip" not in element["file_url"] and element["is_deleted"] is False:
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
    if len(config.tags) == 2:
        tags = config.tags[0] + "+" + config.tags[1]
    elif len(config.tags) == 1:
        tags = config.tags[0]
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
        url = gen_url(tags,page)
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
