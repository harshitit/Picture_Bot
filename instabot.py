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

#this function is used to search most recent post ID
def recent_post_id():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ( ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    return user_info['data'][0]['id']

#this function is used to search another user most recent post ID
def another_user_recent_post_id(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    return user_info['data'][0]['id']

#main function starts here
print '---WELCOME---\nTo PictureBot:'
choice1=choice2=True
while choice1 == True:
    ask_to_init=int(raw_input('PRESS:-\n1-> Sign In\n2-> Exit\n->'))
    if ask_to_init == 1:
        while choice2==True:
            ask_choice=int(raw_input('PRESS one of the following:\n1-> Show self details\n2-> Get another usedID\n3-> Show self most recent post ID\n4-> Show another user most recent post ID\n5-> Sign Out\n-> '))
            if ask_choice == 1:
                self_info()
            elif ask_choice == 2:
                another_username=raw_input('Enter username to search userID: ')
                print 'userID is '+ str(get_user_id(another_username))
            elif ask_choice == 3:
                print 'postID is '+ str(recent_post_id())
            elif ask_choice == 4:
                another_username = raw_input('Enter username to get most recent postID: ')
                print 'postID is '+ str(another_user_recent_post_id(another_username))
            elif ask_choice == 5:
                choice2=False
            else:
                print 'WRONG CHOICE'
    elif ask_to_init == 2:
        choice1=False
    else:
        print 'WRONG CHOICE'
