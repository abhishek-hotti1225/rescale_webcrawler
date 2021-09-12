## Rescale - Webcrawler

# Pre-Reqs:
1. python3

### Steps to run the program:
1. ./setup.sh
2. source venv/bin/activate
3. python web_crawler.py -u \<url> -tc \<thread_count> 
    1. Ex: python web_crawler.py -u rescale.com -tc 5

## Project
This project takes in an url and thread count number as input and then outputs all the href tags found in that page and then loops through the href tags to find href tags in the new pages. 

I choose to use a base Thread class, and not thread pools (ThreadPoolExecutor) as I felt it would be better to showcase my base understanding of how to handle  and keep track of running threads. I have added comments as I felt it would be beneficial to explain my thought process as the code executes through

Time to completion: 2 hours (9 PM - 11 PM)