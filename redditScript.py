import urllib3
import json
import myTextWrap
import math
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
sizex, sizey = myTextWrap.getTerminalSize()
sizex = math.floor(sizex * 0.8)



def recursivePrint(parent, indents, baseDict, tracker):

    for child in parent:
        if(tracker != len(baseDict[1]['data']['children'])):
            if(baseDict[1]['data']['children'][tracker] == child):
                tracker += 1
                indents = 0
        #print(child['data']['body'])
        wrappedParent = myTextWrap.wrap(
            "> " + child['data']['author'] + ' : ' + str(child['data']['ups']) + ' points: ' + child['data']['body'], sizex)
        myTextWrap.printList(wrappedParent, indents)
        print()
        if 'data' in child['data']['replies']:
            indents += 1
            recursivePrint(child['data']['replies']['data']
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
    chooseIndex = int(input("enter the index of the post you want to view \n"))
    inputURL = subredditPosts[chooseIndex]['data']['url']

    postAndReplies(inputURL,subredditPosts)


#initial repliesdict screenx
def postAndReplies(url, subredditPosts):

    base = http.request('GET', url + '.json')
    pageDict = json.loads(base.data.decode('utf-8'))
    title = pageDict[0]['data']['children'][0]['data']['title']
    post = pageDict[0]['data']['children'][0]['data']['selftext']

    print('\n' + title + '\n')
    wrappedPost = myTextWrap.wrap(post, sizex)
    print()
    myTextWrap.printList(wrappedPost, 0)

    print("Comments: \n")
    recursivePrint(pageDict[1]['data']['children'], 0, pageDict, 0)
    x = input('0 to exit, 1 to change subreddits, 2 to change posts \n')
    if x == '1':
        subredditChoice()
    elif x == '2':
        print()
        for i in range(len(subredditPosts)):
            print(str(i) + ": " + subredditPosts[i]['data']['title'])
        chooseIndex = int(input("enter the index of the post you want to view \n"))
        inputURL = subredditPosts[chooseIndex]['data']['url']
        postAndReplies(inputURL, subredditPosts)
    
    


subredditChoice()
