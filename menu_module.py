import config

def run_menu():
    print("--------------------------------------------------")
    print("Welcome to Anime image extractor version 1.0.3")
    print("--------------------------------------------------" + "\n")
    prompt_tags()
    prompt_down_limit()

def prompt_tags():
    while True:
        if not config.tags:
            edit_tags()
            break
        tags = get_tags()
        print("You have set: " + tags + "As your default, do you wish to change it? [y/N]" + "\n")
        change_tag_input = input().lower()
        print("")
        if change_tag_input == "" or change_tag_input == "n":
            break
        elif change_tag_input == "y":
            edit_tags()
            break

def get_tags():
    tags = ""
    for tag in config.tags:
        tags = tags + tag + " "
    return tags

def edit_tags():
    while True:
        if config.tags:
            print("You have set: " + get_tags() + "what do you wish to do?:" + "\n")
        else:
            print("You have not set any tags")
        print("1 Add tag")
        print("2 Clear")
        print("3 Done" + "\n")
        change_tag_choice = input()
        print("")
        if change_tag_choice == "1" and len(config.tags) <= 1:
            new_tag_input = input("Enter tag: ")
            print("")
            config.tags.append(new_tag_input)
        elif change_tag_choice == "1" and len(config.tags) >= 2:
            print("You can not have more than 2 tags" + "\n")
        elif change_tag_choice == "2":
            config.tags = []
        elif change_tag_choice == "3":
            if config.tags:
                break

def prompt_down_limit():
    while True:
        if config.down_limit <= 0:
            edit_down_limit()
            break
        print("You have set: " + str(config.down_limit) + " As your default, do you wish to change it? [y/N]" + "\n")
        change_down_limit_input = input().lower()
        print("")
        if change_down_limit_input == "" or change_down_limit_input == "n":
            break
        elif change_down_limit_input == "y":
            edit_down_limit()
            break

def edit_down_limit():
    while True:
        user_input = input("Enter number of pictures you wish to download: ")
        print("")
        try:
            val = int(user_input)
            config.down_limit = val
            break
        except ValueError:
            print("That's not an int!" + "\n")
