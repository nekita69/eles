function hideblock(el){
    let e = el.parentNode.childNodes[3]
    e.classList.toggle('unactive');
}

function active_button_back(){ //Добавление/удаление кнопки "Назад";
    let bnt = document.getElementById("button_back");
    bnt.classList.toggle('unactive');
}

function open_group_list(el){ //Вывести список группы;
    //Находим CSRF-токен на странице
    let mt = document.getElementsByTagName('meta');
    let ctoken = ''; //CSRF-токен
    for(let i = 0; i < mt.length; i++){
        if(mt[i].getAttribute('name') == 'csrfmiddlewaretoken'){
            ctoken = mt[i].getAttribute('content');
        }
    }
    

    let dics = el.parentNode.parentNode.parentNode.parentNode.childNodes[1].childNodes[0].innerHTML;
    let about_group = el.childNodes[1].innerHTML;

    //Формируем JSON для запроса
    let json_request = {'dischip':dics, 'about_group':about_group};
    let jsonData = JSON.stringify(json_request);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'group_list', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', ctoken);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            
            //console.log(xhr.responseText);

            let dv = document.getElementsByClassName('my_main_block')[0];
            dv.innerHTML = ""; //Удаляем все содержимое блока;
            dv.innerHTML = xhr.responseText; //Устанавливаем полученную страницу;

        }
    };
    xhr.send(jsonData);


    active_button_back(); //Добавляем кнопку "Назад";
}



function back_home_page(){
    active_button_back(); //Удаляем кнопку "Назад";

    let mt = document.getElementsByTagName('meta');
    let ctoken = ''; //CSRF-токен
    for(let i = 0; i < mt.length; i++){
        if(mt[i].getAttribute('name') == 'csrfmiddlewaretoken'){
            ctoken = mt[i].getAttribute('content');
        }
    }

    let person_name = document.getElementsByClassName('person_name')[0].innerHTML; //Вытаскиваем имя;

    let json_request = {'person_name':person_name};
    let jsonData = JSON.stringify(json_request);

    //console.log(person_name);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'diship_list', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', ctoken);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

            let dv = document.getElementsByClassName('my_main_block')[0];
            dv.innerHTML = ""; //Удаляем все содержимое блока;
            dv.innerHTML = xhr.responseText; //Устанавливаем полученную страницу;

        }
    };
    xhr.send(jsonData);
}


function save_change_file(){ //Метод для сохранения данных в файл;
    res = confirm('Продолжить?');
    if (res){
        let hat = document.getElementsByClassName('group_list_header')[0].childNodes[1].childNodes[0].innerHTML;
        let about_gr = hat.split('|');
        //console.log(about_gr);

        //Находим CSRF-токен на странице
        let mt = document.getElementsByTagName('meta');
        let ctoken = ''; //CSRF-токен
        for(let i = 0; i < mt.length; i++){
            if(mt[i].getAttribute('name') == 'csrfmiddlewaretoken'){
                ctoken = mt[i].getAttribute('content');
            }
        }


        //Находим всех студентво 
        let studs = document.getElementsByClassName('list_item');
        let group_list = [];
        for(let i = 0; i < studs.length; i++){
            let child = studs[i].childNodes;
            stud_name = child[1].childNodes[2].innerHTML;
            let gr = {"name":stud_name, "mark":child[3].value};
            group_list.push(gr);
            //console.log(gr);
        }
        
        
        let json_request = {"dishic":about_gr[0], "m_gr":about_gr[1], "gr":about_gr[2], "mark":about_gr[3], "group_list":group_list};
        let jsonData = JSON.stringify(json_request);

        //console.log(person_name);
        let xhr = new XMLHttpRequest();
        xhr.open('POST', 'set_mark', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', ctoken);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                
                resp = JSON.parse(xhr.responseText);
                back_home_page(); //Вернуться на главную;
                alert(resp['response']); 

            }
        };
        xhr.send(jsonData);

    }
    else{

    }

}


function create_teacher(){ //Функция для создания преподавателя;
    //Находим CSRF-токен на странице
    let mt = document.getElementsByTagName('meta');
    let ctoken = ''; //CSRF-токен
    for(let i = 0; i < mt.length; i++){
        if(mt[i].getAttribute('name') == 'csrfmiddlewaretoken'){
            ctoken = mt[i].getAttribute('content');
        }
    }

    let log = document.getElementsByName('teacher_login')[0].value;
    document.getElementsByName('teacher_login')[0].value = "";
    let pass = document.getElementsByName('teacher_password')[0].value;
    document.getElementsByName('teacher_password')[0].value = "";
    let s_name = document.getElementsByName('teacher_s_name')[0].value;
    document.getElementsByName('teacher_s_name')[0].value = "";
    let f_name = document.getElementsByName('teacher_f_name')[0].value;
    document.getElementsByName('teacher_f_name')[0].value = "";
    let t_name = document.getElementsByName('teacher_t_name')[0].value;
    document.getElementsByName('teacher_t_name')[0].value = "";
    let is_admin = document.getElementsByName('teacher_is_admin')[0].checked;

    if(log != "" && pass != "" && s_name != "" && f_name != "" && t_name != ""){
        let json_request = {'login':log, 'password':pass, 'f_name':f_name, 's_name':s_name, 't_name':t_name, 'is_admin':is_admin};
        let jsonData = JSON.stringify(json_request);

        //console.log(person_name);
        let xhr = new XMLHttpRequest();
        xhr.open('POST', 'create_teacher', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', ctoken);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

                //let dv = document.getElementsByClassName('my_main_block')[0];
                //dv.innerHTML = ""; //Удаляем все содержимое блока;
                //dv.innerHTML = xhr.responseText; //Устанавливаем полученную страницу;
                resp = JSON.parse(xhr.responseText);
                if (resp['response'] == 'login is busy'){
                    alert('Выбранное имя пользователя занято');
                }
                else if(resp['response'] == 'success add'){
                    alert('Преподаватель добавлен');
                }
                //console.log(resp['response']);
            }
        };
        xhr.send(jsonData);
    }
}




function delete_teach(el){
    //Находим CSRF-токен на странице
    let mt = document.getElementsByTagName('meta');
    let ctoken = ''; //CSRF-токен
    for(let i = 0; i < mt.length; i++){
        if(mt[i].getAttribute('name') == 'csrfmiddlewaretoken'){
            ctoken = mt[i].getAttribute('content');
        }
    }
    
    //Удаляем со страницы;
    let parent = el.parentNode.parentNode.parentNode;
    let login = el.parentNode.parentNode.childNodes[1].childNodes[0].innerHTML;
    console.log(login);
    parent.removeChild(el.parentNode.parentNode);

    let json_request = {'login':login};
    let jsonData = JSON.stringify(json_request);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', 'delete_teacher', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', ctoken);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

            resp = JSON.parse(xhr.responseText);
            alert(resp['response']);
        }
    };
    xhr.send(jsonData);
}