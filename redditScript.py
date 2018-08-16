import urllib3
import json
import myTextWrap
import math
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
subreddit = input("enter subreddit name \n")
subredditRequest = http.request('GET', 'https://www.reddit.com/r/' + subreddit + '.json')
postsDict = json.loads(subredditRequest.data.decode('utf-8'))
subredditPosts = postsDict['data']['children']
print()
for i in range(len(subredditPosts)):
    print(str(i) + ": " + subredditPosts[i]['data']['title'])
chooseIndex = int(input("enter the index of the post you want to view \n"))
inputURL = subredditPosts[chooseIndex]['data']['url']
base = http.request('GET', inputURL + '.json')

pageDict = json.loads(base.data.decode('utf-8'))
title = pageDict[0]['data']['children'][0]['data']['title']
post = pageDict[0]['data']['children'][0]['data']['selftext']
postReplies = pageDict[1]['data']['children']


def printReplies(repliesDict, screenX):
    print("Comments: \n")
    for replies in repliesDict:
        wrappedParent = myTextWrap.wrap(
            "> " + replies['data']['author'] + ' : ' + str(replies['data']['ups']) + ' points: ' + replies['data']['body'], screenX)
        myTextWrap.printList(wrappedParent, 2)
        print()


        
        
        if 'data' in replies['data']['replies']:
            childReplies = replies['data']['replies']['data']['children'] # INDEX data body 
            for children in childReplies:
                wrappedChild = myTextWrap.wrap("> " +  children['data']['author'] + ' : ' + str(children['data']['ups']) + ' points: ' + children['data']['body'], screenX)
                myTextWrap.printList(wrappedChild, 4)
                print()

                #print(children['data']['body'])
        
        



# 1 data children (replies cutoff) INDEX data body for original comment
# 1 data children INDEX data replies data children INDEX data body for first degree reply
sizex, sizey = myTextWrap.getTerminalSize()
sizex = math.floor(sizex * 0.8)

print('\n' + title + '\n')
wrappedPost= myTextWrap.wrap(post, sizex)
print()
myTextWrap.printList(wrappedPost, 0)
print()
printReplies(postReplies, sizex)







