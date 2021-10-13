from bs4 import BeautifulSoup
import requests
import json
import wget
import os

course_id = int(input("Target Course ID: "))
init_lesson_id = int(input("Target Initial Lesson ID: "))
login_cookie_value = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhY2Nlc3MiLCJpYXQiOjE2MzQxMTY2MTAsImp0aSI6IjljN2YzMjJmLWJiYjEtNDg5NC04MTdiLTk4MjE3MWMxMGJiZiIsImlzcyI6InNrX3ZoZHQyamh4Iiwic3ViIjoiOWZiNTEwZTQtNTFlOS00M2EyLTg1OWUtZmE3NTMzNzU0NDA5In0.z7gNsHE6GTMjEJndGOO_1AN6RVRowVSFvhFQPUnB3kU'
continue_flag = False
hack_val = 1

base_dir = os.path.abspath(os.getcwd())
# print(base_dir)

def check_cont_flag(current_lesson_id):
    if int(current_lesson_id) == init_lesson_id:
        global hack_val
        hack_val = 0
        return True
    else:
        return False
        
def to_url(payload, target):
    if target.lower() == 'base':
        url = 'https://attain-online-japanese.teachable.com/courses/' + \
            str(payload[0]) + '/lectures/' + str(payload[1])
    elif target.lower() == 'wistia':
        url = 'https://fast.wistia.com/embed/medias/' + \
            str(payload[0]) + '.json'
    return url

def name_compact_name(the_string):
    remove_characters = ['\\','/',':','*','?','"','<','>','|']
    for character in remove_characters:
        the_string = the_string.replace(character, "")
    return the_string

ses = requests.session()
ses.cookies.set('sk_vhdt2jhx_access', login_cookie_value, domain='attain-online-japanese.teachable.com')

res = ses.get(to_url([course_id, init_lesson_id], 'base'))
souped_res = BeautifulSoup(res.content.decode('utf-8'), features='lxml')

set_of_lesson_titles = souped_res.find_all('div', attrs={'role': 'heading'})

for each_lesson_title in set_of_lesson_titles:
    res_lesson_title = each_lesson_title.text.strip()
    print(res_lesson_title)
    lesson_links = each_lesson_title.findNext('ul').find_all('a')
    num_lesson = 1
    
    for each_lesson_link in lesson_links:
        res_lesson_id = each_lesson_link.get('data-ss-lecture-id')
        
        if hack_val:
            continue_flag = check_cont_flag(res_lesson_id)

        if continue_flag:
            res_lesson_url = to_url([course_id, res_lesson_id], 'base')
            to_lesson = ses.get(res_lesson_url, timeout=(3.05, 27))
            in_lesson = BeautifulSoup(
                to_lesson.content.decode('utf-8'), features='lxml')
            res_current_lesson_name = each_lesson_link.find(
                'span', {'class': 'lecture-name'}).text.replace('\n', '').strip().replace('  ', '')
            print(res_current_lesson_name, res_lesson_url)
            # f = open(str(res_lesson_id) + '.html', 'w', encoding='utf-8')
            # f.write(str(in_lesson))
            # f.close()
            # wistia_id_element = in_lesson.find({'data-wistia-id': True})
            wistia_id_element = in_lesson.find(
                lambda tag: 'data-wistia-id' in tag.attrs)
            
            
            if wistia_id_element:
                res_wistia_id = wistia_id_element.get('data-wistia-id')
                res_wistia_url = to_url([res_wistia_id], 'wistia')
                to_wistia = requests.get(res_wistia_url)
                in_wistia = json.loads(to_wistia.text)
                to_download_url = in_wistia['media']['assets'][0]['url']
                to_directory = base_dir + '\\downloaded\\' + \
                    str(course_id) + '\\' + \
                    name_compact_name(res_lesson_title)
                res_filename = name_compact_name(res_current_lesson_name) + '.mp4'
                res_end_path = to_directory + '\\' + str(num_lesson) + '. ' + res_filename
                if not os.path.exists(to_directory):
                    os.makedirs(to_directory)
                wget.download(to_download_url, res_end_path)
                print('\n')
                print('#Downloaded to -->', res_wistia_url,
                    '-->', res_end_path)
                num_lesson += 1
                print('\n')
