from bs4 import BeautifulSoup
import requests
import threading
import time
import argparse

all_visited_urls = set()
to_visit_urls = set()
all_threads = []

class myThread (threading.Thread):
    def __init__(self, webpage):
        threading.Thread.__init__(self)
        self.webpage = webpage

    def run(self):
      get_webpage(self.webpage)

def get_webpage(url):
    if not url.startswith("http"): # checks if https exists in the beginning of the url, if not, then prefix the url
        url = "https://"+url
    try:
        source_code = requests.get(url).text
    except requests.exceptions.RequestException as err: # some urls are no longer valid (i.e.: support.rescale.com), handles those cases
        print(err)
        raise SystemExit(err)
    soup = BeautifulSoup(source_code, "html.parser") # load the html code as machine readable, comparable to json.loads
    all_a_tags = set()
    tag_count = 0 # limit the number of tags gathered from each page (i.e: facebook has too many embedded links)
    for each_tag in soup.findAll("a", href=True):
        if each_tag["href"].startswith("http"): # filters the urls to only add absolute URLs
            all_a_tags.add(each_tag["href"])
            tag_count += 1
        if tag_count > 25:
            break
    if len(all_a_tags) != 0:
        current_a_tags = "\n" + url + "\n\t" + "\n\t".join(all_a_tags)
        print(current_a_tags) # print the sub tags found in each page
        
        global to_visit_urls
        to_visit_urls.update(all_a_tags.difference(all_visited_urls)) # add newly found URLs to the to_visit set
    global all_threads
    all_threads.pop() # thread is ending, so alert main process that space is available to spin up a new thread

# Driver code
if __name__ == '__main__':
    # starts crawling and prints output
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", "-u", help="The start url to start web crawling with", required=True) # parses the starting url
    parser.add_argument("-thread_count", "-tc", help="The # of sub-threads to spawn", default=2, type=int) # sets the number of threads to spawn
    args = parser.parse_args()
    to_visit_urls.add(args.url) # adds the starting url to the set of need to visit urls
    while True: # starts the infinte loop
        if len(all_threads) < args.thread_count: # continues to spawn more threads if we are not at the preset thread count limit
            curr_url = list(to_visit_urls)[0] # pick a url randomly from the set of nonvisited urls
            curr_thread = myThread(curr_url)
            all_threads.append(curr_thread) # keep a count of the threads being executed currently in a list
            curr_thread.start() # starts the execution of thread
            if len(all_threads) == 1: # during initial start, wait a few seconds for the links to be extracted from original site
                time.sleep(2)
            all_visited_urls.add(curr_url) # add this url as a page that is already visited
            to_visit_urls.remove(curr_url) # remove current url from the to visit set, so that we dont loop
