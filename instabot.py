import requests
import urllib
from keys import ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'

# this function is used the get self details
def self_info():
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
  user_info = requests.get(request_url).json()
  if user_info['meta']['code'] == 200:
    print user_info
  else:
    print 'Status code other than 200 received!'

# this function is used to search userID with the help of username
def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
  user_info = requests.get(request_url).json()
  if user_info['data']:
      return user_info['data'][0]['id']
  else:
      print '------Username NOT found------\nStatus code other than 200 received!'
      return 0

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

# this function is used to download post and search most recent post ID
def recent_post_id():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ( ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            download_post(user_info['data'][0]['id'], user_info['data'])
            print 'The post was downloaded successfully....'
            return user_info['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

# this function is used to download post and search another user most recent post ID
def another_user_recent_post_id(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id,ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    user_choice = int(raw_input('Choose the type of post to download:-\n1-> Most recent post\n2-> Minimum number of likes\n3-> Maximum number of likes\n4-> Posts with certain tag\n5-> Exit\n-> '))
    if user_id > 0:
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

# this is used to get insta_user postID
def get_media_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id is not None:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
        media_info = requests.get(request_url).json()
        if media_info['meta']['code'] == 200:
            if len(media_info['data']):
                return media_info['data'][0]['id']
        else:
            return None
    else:
        return None

# this function is used to like a post
def like_post(insta_username):
    media_id = get_media_id(insta_username)
    if media_id is not None:
        request_url = (BASE_URL + 'media/%s/likes') % (media_id)
        payload = {'access_token': ACCESS_TOKEN}
        post_like = requests.post(request_url, payload).json()
        if post_like['meta']['code'] == 200:
            print 'You\'ve successfully liked the post...'
        else:
            print 'Sorry! There was an error liking the post.'
    else:
        return

# this function give us a list of comments
def get_comments_list(insta_username):
    post_id = get_media_id(username)
    print post_id
    if post_id is not None:
        request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (post_id, ACCESS_TOKEN)
        comments_info = requests.get(request_url).json()
        if comments_info['meta']['code'] == 200:
            if len(comments_info['data']):
                comments_list = []
                for index in range(len(comments_info['data'])):
                    comment_dict = {comments_info['data'][index]['id']: comments_info['data'][index]['text']}
                    comments_list.append(comment_dict)
                return comments_list
            else:
                print 'No comments...'
        else:
            print 'Status code other than 200 received'
    else:
        return

# this function is used to post a comment
def comment_on_post(insta_username):
    media_id = get_media_id(insta_username)
    if media_id is not None:
        request_url = (BASE_URL + 'media/%s/comments') % media_id
        comment = raw_input('Enter your comment: ')
        payload = {'access_token': ACCESS_TOKEN, 'text': comment}
        spawn_comment = requests.post(request_url, payload).json()
        if spawn_comment['meta']['code'] == 200:
            print 'Your comment was posted successfully..'
        else:
            print 'Sorry, your comment couldn\'t be posted.'
    else:
        'There was an error posting your comment..\n-------TRY AGAIN-------'

# main function starts here
print '---WELCOME---\nTo PictureBot:'
choice1=choice2=True
while choice1 == True:
    ask_to_init=int(raw_input('\nPRESS:-\n1-> Sign In\n2-> Exit\n->'))
    if ask_to_init == 1:
        while choice2==True:
            ask_choice=int(raw_input('\nPRESS one of the following:\n1-> Show self details\n2-> Get another usedID\n3-> Download self most recent post and post ID\n4-> Download another user most recent post and post ID\n5-> Like a post\n6-> Get list of comments\n7-> Comment on a post\n8-> Sign Out\n-> '))
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
                username=raw_input('\nEnter username: ')
                like_post(username)
            elif ask_choice == 6:
                username = raw_input('\nEnter username: ')
                print get_comments_list(username)
            elif ask_choice ==7:
                username = raw_input('\nEnter username: ')
                comment_on_post(username)
            elif ask_choice == 8:
                choice2=False
            else:
                print 'WRONG CHOICE'
    elif ask_to_init == 2:
        choice1=False
    else:
        print 'WRONG CHOICE'
