import json
from django.shortcuts import render
from django.http import JsonResponse

from .datamanager import Manager
from .read import get_subject, get_group_stud, fill_file


man = Manager()

def start_page(request):
    return render(request, 'elestapi/signin_page.html')


def signin(request):
    if request.method == "POST":
        data = request.POST

        username = data['username']
        password = data['password']
        ctoken = data['csrfmiddlewaretoken']
        
        res = man.get_name(username, password) #Словарь с ФИО
        if res == None:
            return render(request, 'elestapi/signin_page.html', {'exception':'Пользователь не найден'})

        if res['is_admin']:

            man.cursor.execute("SELECT * FROM users")
            teachers = []
            temp = man.cursor.fetchone()
            while temp != None:
                teachers.append(temp)
                temp = man.cursor.fetchone()
            teacter_list = []
            for item in teachers:
                teacter_list.append({"id":item[0], "login":item[1], "password":item[2], "f_name":item[3], "s_name":item[4], "t_name":item[5], "is_admin":item[6]})
            send_data = {'name' : res, 'csrfmiddlewaretoken' : ctoken, 'teachers':teacter_list}
            return render(request, 'elestapi/admin_page.html', send_data)
        else:

            dcsp = get_subject(res['s_name'] + " " + res['f_name'] + " " + res['t_name']) #Получаем дисциплины и предметы, которые ведет преподаватель;
            if(len(dcsp) > 0):
                cr = dcsp[0]['cource'].split()[0]
                dcsp[0]['cource'] = cr
                dists = [{
                        "subject":dcsp[0]['subject'], 
                        'cources':[{
                            'm_group':dcsp[0]['m_group'], 
                            'cource': dcsp[0]['cource'], 
                            'group': dcsp[0]['group'], 
                            'mark': dcsp[0]['mark']
                        }]
                }]
                
                for item in dcsp:
                    flag = True
                    for item2 in dists:
                        if item['subject'] == item2['subject']:
                            flag = False
                            cr = item['cource'].split()[0]
                            item['cource'] = cr
                            item2['cources'].append({
                                'm_group':item['m_group'], 
                                'cource': item['cource'], 
                                'group': item['group'], 
                                'mark': item['mark']
                            })

                    if(flag):
                        cr = item['cource'].split()[0]
                        item['cource'] = cr
                        dists.append({
                            "subject":item['subject'], 
                            'cources':[{
                                'cource': item['cource'], 
                                'group': item['group'], 
                                'mark': item['mark']
                            }]
                        })
                        
                for sub in dists:
                    course_rez = {
                        '1':[],
                        '2':[],
                        '3':[],
                        '4':[],
                    }
                    for crs in sub['cources']:
                        if 'm_group' in crs:
                            m_gr = crs['m_group']
                        else:
                            m_gr = ''
                        course_rez[crs['cource']].append({
                            'm_group':m_gr,
                            'group':crs['group'],
                            'mark':crs['mark'],
                        })

                    sub['cources'] = course_rez
                
                send_data = {'name' : res, 'csrfmiddlewaretoken' : ctoken, 'dischip':dists}
                return render(request, 'elestapi/home_page.html', send_data)
            
            send_data = {'name' : res, 'csrfmiddlewaretoken' : ctoken, 'dischip':[]}
            return render(request, 'elestapi/home_page.html', send_data)
    return render(request, 'elestapi/signin_page.html', {'exception':'Неверный запрос'})



def group_list(request):
    if request.method == "POST":
        data = request.body
        res = json.loads(data) #JSon в dict python
        res_data = res['about_group'].split("|")
        gr_mark = res_data[2].strip(" ")
        studs = get_group_stud(res_data[0], res_data[1], res['dischip'].strip(" "), gr_mark)
        if gr_mark.lower() == 'зачёт':
            return render(request, 'elestapi/group_list_zach.html', {'dischip':res['dischip'], 'about_group': res['about_group'], 'studs':studs}) 
        else:
            return render(request, 'elestapi/group_list_exz.html', {'dischip':res['dischip'], 'about_group': res['about_group'], 'studs':studs}) 
    return render(request, 'elestapi/signin_page.html', {'exception':'Неверный запрос'}) 


def all_group_dischip_list(request): #Список дисциплинs
    if request.method == "POST":
        data = request.body
        res = json.loads(data) #Фамилия имя отчество преподавателя;

        dcsp = get_subject(res['person_name']) #Получаем дисциплины и предметы, которые ведет преподаватель;
        if(len(dcsp) > 0):
            cr = dcsp[0]['cource'].split()[0]
            dcsp[0]['cource'] = cr
            dists = [{"subject":dcsp[0]['subject'], 'cources':[{'m_group':dcsp[0]['m_group'], 'cource': dcsp[0]['cource'], 'group': dcsp[0]['group'], 'mark': dcsp[0]['mark']}]}]
            for item in dcsp:
                flag = True
                for item2 in dists:
                    if item['subject'] == item2['subject']:
                        flag = False
                        cr = item['cource'].split()[0]
                        item['cource'] = cr
                        item2['cources'].append({'m_group':item['m_group'], 'cource': item['cource'], 'group': item['group'], 'mark': item['mark']})
                if(flag):
                    cr = item['cource'].split()[0]
                    item['cource'] = cr
                    dists.append({"subject":item['subject'], 'cources':[{'cource': item['cource'], 'group': item['group'], 'mark': item['mark']}]})

            for sub in dists:
                course_rez = {
                    '1':[],
                    '2':[],
                    '3':[],
                    '4':[],
                }
                for crs in sub['cources']:
                    if 'm_group' in crs:
                        m_gr = crs['m_group']
                    else:
                        m_gr = ''
                    course_rez[crs['cource']].append({
                        'm_group':m_gr,
                        'group':crs['group'],
                        'mark':crs['mark'],
                    })

                sub['cources'] = course_rez
            
            send_data = {'dischip':dists}
            return render(request, 'elestapi/dischip_list.html', send_data)
        
        send_data = {'dischip': []}
        return render(request, 'elestapi/dischip_list.html', send_data)
    return render(request, 'elestapi/signin_page.html', {'exception':'Неверный запрос'})




def create_teacher(request):
    if request.method == "POST":
        data = request.body
        about_teach = json.loads(data)
        res = man.create_teacher(about_teach)
        if res: #Если преподаватель добавлен;
            return JsonResponse({"response":'success add'})
        return JsonResponse({"response":'login is busy'})
    return render(request, 'elestapi/signin_page.html', {'exception':'Неверный запрос'})


def set_mark_for_gr(request):
    if request.method == "POST":
        data = request.body
        about_gr = json.loads(data)
        fill_file(about_gr['gr'], about_gr['dishic'], about_gr['mark'], about_gr['group_list'])
        return JsonResponse({"response":'Данные обновлены'})
    return render(request, 'elestapi/signin_page.html', {'exception':'Неверный запрос'})


def delete_teacher(request):
    if request.method == 'POST':
        data = request.body
        login = json.loads(data)['login']
        man.delete_teacher(login)
        return JsonResponse({"response":'Данные обновлены'})
    return render(request, 'elestapi/signin_page.html', {'exception':'Неверный запрос'})