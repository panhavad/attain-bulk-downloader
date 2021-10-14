from bs4 import BeautifulSoup
import requests
import json
import wget
import os

course_id = int(input("Target Course ID: "))
init_lesson_id = int(input("Target Initial Lesson ID: "))
login_cookie_value = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhY2Nlc3MiLCJpYXQiOjE2MzQyMjY5NTgsImp0aSI6IjU2MDhmN2E0LWY5MjAtNDk0MC05YjM0LTI4NTVkMjdhMTgwNiIsImlzcyI6InNrX3ZoZHQyamh4Iiwic3ViIjoiMmZiOGFkN2MtMWQyMS00MGY4LTgyYWEtMzgxZDY3ZGUyMDEzIn0.tIdrZ2yPgECmqjBa9AZP12KsLWJg3l28TCvjfM_X4V0'
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
    elif target.lower() == 'pdf':
        url = 'https://cdn.filestackcontent.com/' + \
            str(payload[0])
    return url

def name_compact_name(the_string):
    remove_characters = ['\\','/',':','*','?','"','<','>','|','\n','  ']
    for character in remove_characters:
        the_string = the_string.replace(character, "")
    return the_string

ses = requests.session()
ses.cookies.set('sk_vhdt2jhx_access', login_cookie_value, domain='attain-online-japanese.teachable.com')

res = ses.get(to_url([course_id, init_lesson_id], 'base'))
souped_res = BeautifulSoup(res.content.decode('utf-8'), features='lxml')

set_of_lesson_titles = souped_res.find_all('div', attrs={'role': 'heading'})
res_course_name = name_compact_name(souped_res.find('div', {'class': 'course-sidebar-head'}).find('h2').text)

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
            res_current_lesson_name = name_compact_name(each_lesson_link.find(
                'span', {'class': 'lecture-name'}).text)
            print(res_current_lesson_name, res_lesson_url)
            # f = open(str(res_lesson_id) + '.html', 'w', encoding='utf-8')
            # f.write(str(in_lesson))
            # f.close()
            # wistia_id_element = in_lesson.find({'data-wistia-id': True})
            
            
            #download pdf
            pdf_id_element = in_lesson.find(
                lambda tag: 'data-pdfviewer-id' in tag.attrs)
            #download video
            wistia_id_element = in_lesson.find(
                lambda tag: 'data-wistia-id' in tag.attrs)

            #check dir
            to_directory = base_dir + '\\downloaded\\' + \
                    str(res_course_name) + '\\' + \
                    name_compact_name(res_lesson_title)
            if not os.path.exists(to_directory):
                    os.makedirs(to_directory)
            
            #start download
            if wistia_id_element or pdf_id_element:
                if wistia_id_element:
                    res_wistia_id = wistia_id_element.get('data-wistia-id')
                    res_wistia_url = to_url([res_wistia_id], 'wistia')
                    to_wistia = requests.get(res_wistia_url)
                    in_wistia = json.loads(to_wistia.text)
                    to_download_url = in_wistia['media']['assets'][0]['url']
                    
                    res_filename = name_compact_name(res_current_lesson_name) + '.mp4'
                    res_end_path = to_directory + '\\' + str(num_lesson) + '. ' + res_filename
                    if not os.path.exists(res_end_path):
                        wget.download(to_download_url, res_end_path)
                        print('\n')
                        print('#Downloaded to -->', res_wistia_url,
                            '-->', res_end_path)
                        print('\n')
                    else:
                        print('\n')
                        print('!!Existed')
                        print('\n')
                    
                elif pdf_id_element:
                    res_pdf_id = pdf_id_element.get('data-pdfviewer-id')
                    res_pdf_url = to_url([res_pdf_id], 'pdf')
                    res_filename = name_compact_name(res_current_lesson_name) + '.pdf'
                    res_end_path = to_directory + '\\' + str(num_lesson) + '. ' + res_filename
                    if not os.path.exists(res_end_path):
                        wget.download(res_pdf_url, res_end_path)
                        print('\n')
                        print('#Downloaded to -->', res_pdf_url,
                            '-->', res_end_path)
                        print('\n')
                    else:
                        print('\n')
                        print('!!Existed')
                        print('\n')
                num_lesson += 1
