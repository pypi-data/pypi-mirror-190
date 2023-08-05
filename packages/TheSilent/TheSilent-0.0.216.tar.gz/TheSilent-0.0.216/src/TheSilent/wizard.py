import TheSilent.TheSilent as ts

import argparse

og_parser = argparse.ArgumentParser(prog = "TheSilent")

#tools
og_parser.add_argument("--link_scanner", dest = "link_scanner", required = False, help = "[tool]: crawl urls")

#parameters
og_parser.add_argument("--crawl", dest = "crawl", required = False, help = "[parameter]: Crawl 'all' like google or crawl 'x' links. Defaults to all.")
og_parser.add_argument("--depth", dest = "depth", required = False, help = "[parameter]: How deep? Examples: depth 1 = https://www.example.com/index.html, depth 2 = https://www.example.com/images/image.png. Defaults to 1.")
og_parser.add_argument("--my_file", dest = "my_file", required = False, help = "[parameter]: Outputs urls to text file. Example: links.txt. defaults to none.")
og_parser.add_argument("--parse", dest = "parse", required = False, help = "[parameter]: Parse url for specific string. Example: .onion, .com, .org, etc. Defaults to none.")
og_parser.add_argument("--secure", dest = "secure", required = False, help = "[parameter]: https:// = True, http:// = False. Defaults to True")
og_parser.add_argument("--tor", dest = "tor", required = False, help = "[parameter]: Send get requests over tor. Defaults to False.")
og_parser.add_argument("--url", dest = "url", required = False, help = "[parameter]: The url. Example: example.com. Defaults to none.")

args = og_parser.parse_args()

if args.link_scanner == "True":
    if args.crawl == None:
        crawl = "link"

    if args.depth == None:
        depth = 1

    if args.my_file == None:
        my_file = " "

    if args.parse == None:
        parse = " "

    if args.secure == None:
        secure = True

    if args.tor == None:
        tor = False

    if args.url == None:
        print("ERROR! URL required! Use --url=example.com")

    if args.url != None:
        ts.link_scanner(args.url, secure = secure, tor = tor, depth = depth, my_file = my_file, crawl = crawl, parse = parse)
