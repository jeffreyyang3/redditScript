import urllib3
import json
import myTextWrap
import math
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
sizex, sizey = myTextWrap.getTerminalSize()
sizex = math.floor(sizex * 0.8)
line = ''
for i in range(sizex - 1):
    line += '-'

#to do: reject bad input, deal with "show more", use urllib instead of urllib3 so can be used on timeshare
#order: subreddit choice, post and replies, choice between new subreddit, same or exit

def recursivePrint(parent, indents, baseDict, tracker): #clean up later

    for child in parent:  # workaround to indent new parent comments correctly
        if(tracker != len(baseDict[1]['data']['children']) and
                baseDict[1]['data']['children'][tracker] == child):  # sees if comment is new parent comment
                tracker += 1
                indents = 0
        #print(child['data']['body'])
        if 'author' in child['data']:
            wrappedParent = myTextWrap.wrap(
                "> " + child['data']['author'] + ' : ' + str(child['data']['ups'])
                + ' points: ' + child['data']['body'], sizex) #move to function later
            myTextWrap.printList(wrappedParent, indents)
        print()
        if 'replies' in child['data'] and 'data' in child['data']['replies']:
            indents += 1
            recursivePrint(child['data']['replies']['data']
                               # do the same for all child comments in order, one more indent per recursion level
                           ['children'], indents, baseDict, tracker)


def subredditChoice():
    subreddit = input("enter subreddit name \n")

    subredditRequest = http.request(
        'GET', 'https://www.reddit.com/r/' + subreddit + '.json')
    postsDict = json.loads(subredditRequest.data.decode('utf-8'))
    subredditPosts = postsDict['data']['children']
    print()
    for i in range(len(subredditPosts)):
        print(str(i) + ": " + subredditPosts[i]['data']['title'])
    print('\n' + line)
    chooseIndex = int(input("enter the index of the post you want to view \n"))
    print()
    if(subredditPosts[chooseIndex]['data']['is_self']):
        inputURL = subredditPosts[chooseIndex]['data']['url']
    else:
        inputURL = 'https://www.reddit.com' + subredditPosts[chooseIndex]['data']['permalink']

    postAndReplies(inputURL,subredditPosts)


#initial repliesdict screenx
def postAndReplies(url, subredditPosts):

    base = http.request('GET', url + '.json')
    pageDict = json.loads(base.data.decode('utf-8'))
    title = pageDict[0]['data']['children'][0]['data']['title']
    if pageDict[0]['data']['children'][0]['data']['is_self']:
        post = pageDict[0]['data']['children'][0]['data']['selftext']
    else:
        post = "Link: " + pageDict[0]['data']['children'][0]['data']['url']


    print('Post: \n' + title + '\n')
    wrappedPost = myTextWrap.wrap(post, sizex)
    print()
    myTextWrap.printList(wrappedPost, 0)
    print(line)

    print("Comments: \n")
    recursivePrint(pageDict[1]['data']['children'], 0, pageDict, 0)
    
    x = input('0 to exit, 1 to change subreddits, 2 to change posts \n') 
    print(line + '\n')
    if x == '1':
        subredditChoice()
    elif x == '2':
        print()
        for i in range(len(subredditPosts)):
            print(str(i) + ": " + subredditPosts[i]['data']['title'])
        chooseIndex = int(input("enter the index of the post you want to view \n"))
        print()
        inputURL = subredditPosts[chooseIndex]['data']['url']
        postAndReplies(inputURL, subredditPosts)
    
    


subredditChoice()
