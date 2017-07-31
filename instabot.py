import requests
import urllib
from keys import ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'

#this function is used the get self details
def self_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code'] == 200:
    print user_info
  else:
    print 'Status code other than 200 received!'

#this function is used to search userID with the help of username
def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
  user_info = requests.get(request_url).json()
  if user_info['data']:
      return user_info['data'][0]['id']
  else:
    print 'Username NOT found\nStatus code other than 200 received!'

# this function is used to download media like image and video
def download_post(post_id, user_posts):
    for e in user_posts:
        if post_id == e['id']:
            if e['type'] == 'image' or e['type'] == 'carousel':
                name = e['id'] + '.jpeg'
                url = e['images']['standard_resolution']['url']
                urllib.urlretrieve(url, name)
            elif e['type'] == 'video':
                name = e['id'] + '.mp4'
                url = e['videos']['standard_resolution']['url']
                urllib.urlretrieve(url, name)

#this function is used to download post and search most recent post ID
def recent_post_id():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ( ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            download_post(user_info['data'][0]['id'], user_info['data'])
            print "The post was downloaded successfully!"
            return user_info['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

#this function is used to download post and search another user most recent post ID
def another_user_recent_post_id(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    user_choice = int(raw_input('Choose the type of post to download:-\n1-> Most recent post\n2-> Minimum number of likes\n3-> Maximum number of likes\n4-> Posts with certain tag\n5-> Exit\n-> '))
    if user_id is not None:
        if user_info['data']:
            if len(user_info) == 0:
                print 'User does\'t have enough posts'
                return
            else:
                post_id = 0
                if user_choice == 1:
                    post_id = user_info['data'][0]['id']
                elif user_choice == 2:
                    min_likes = user_info['data'][0]['likes']['count']
                    for e in user_info['data']:
                        if min_likes > e['likes']['count']:
                            min_likes = e['likes']['count']
                            post_id = e['id']
                elif user_choice == 3:
                    max_likes = user_info['data'][0]['likes']['count']
                    for e in user_info['data']:
                        if max_likes < e['likes']['count']:
                            max_likes = e['likes']['count']
                            post_id = e['id']
                elif user_choice == 4:
                    tag = raw_input("Enter the tag you want to search: ")
                    for e in user_info['data']:
                        if tag in e['tags']:
                            post_id = e['id']
                elif user_choice == 5:
                    print ''
                    return
                if len(post_id):
                    download_post(post_id, user_info['data'])
                    print 'Post successfully downloaded:)'
                    print 'postID is '+ str(post_id)
                else:
                    print 'Sorry no post found:('
    else:
       print 'Status code other than 200 received:('

#main function starts here
print '---WELCOME---\nTo PictureBot:'
choice1=choice2=True
while choice1 == True:
    ask_to_init=int(raw_input('\nPRESS:-\n1-> Sign In\n2-> Exit\n->'))
    if ask_to_init == 1:
        while choice2==True:
            ask_choice=int(raw_input('\nPRESS one of the following:\n1-> Show self details\n2-> Get another usedID\n3-> Download self most recent post and post ID\n4-> Download another user most recent post and post ID\n5-> Sign Out\n-> '))
            if ask_choice == 1:
                self_info()
            elif ask_choice == 2:
                another_username=raw_input('\nEnter username to search userID: ')
                print '-> userID is '+ str(get_user_id(another_username))
            elif ask_choice == 3:
                print '-> postID is '+ str(recent_post_id())
            elif ask_choice == 4:
                another_username = raw_input('\nEnter username to get most recent postID: ')
                another_user_recent_post_id(another_username)
            elif ask_choice == 5:
                choice2=False
            else:
                print 'WRONG CHOICE'
    elif ask_to_init == 2:
        choice1=False
    else:
        print 'WRONG CHOICE'
