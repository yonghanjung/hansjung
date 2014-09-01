# Chatting Service 만들기 

## V0. 기본 세팅 

1. 우선 필요한 V1 파일은 템플릿은 템플릿으로 저장했다. 구조는 다음과 같다. 
	- .gitignore
	- app.yaml
	- appengine_config.py 
	- application
		- __init__.py 
		- api.py
		- generate_keys.py
		- settings.py
		- static 
			- css
				- main.css
			- img
				- favicon.ico
				- favicon.png
			- js 
				- main.js
			- robots.txt
		- templates
			- 404.html
			- 500.html
		- urls.py
	- index.html
	- requirement_dev.txt

* 우선 appengine_config.py는 이 프로젝트의 경로를 설정한다. 이 프로젝트는, lib에서 모든 모듈을 받아와 사용할 것이다. 
* __init__.py 는 각종 설정값을 지정한다. 이 프로젝트에서는, 현재 폴더를 Flask 프로젝트 폴더로 지정하고, setting에 설정값을 저장했다. 그리고 이 모든 설정들을 urls.py로 토스했다. <span style = "color : red"> 여기가 출발점. </span>
* 먼저 Terminal 을 appengine_config.py 가 실행된 곳에서 열고, 다음을 실행하면 된다. 
```terminal
pip install -t lib -Ur requirements_dev.txt
```

__ init.py __
```python 

from flask import Flask

app = Flask('application')
app.config.from_object('application.settings.Production')
```

__settings.py__

```python 
class Config(object):
	pass
	
class Production(object):
	DEBUG = False
	pass
```

__urls.py__

```python
from flask import render_template

from application import app 
# 이게 가능한 이유는 __init__.py에서 이 폴더 이름을 app으로 지정했기 때문이다. 

# Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

```

<hr>
## (Done) V1 --> V2. 어떤 프로그램일지 보기 위해서 UI를 먼저 짜자. 

__과제__

* 채널설정을 하자. (어차피 쓸거니까)
* UI를 만들자. 

우선 이 부분이 api와 관련된 부분이니까, api.py를 새로 만들자.

__api.py__

```python

from pusher import Pusher
from application import app
from flask import request, render_template, jsonify
from user_info import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET

p = Pusher(
	app_id = PUSHER_APP_ID
	key = PUSHER_KEY
	secret = PUSHER_SECRET
)

# 이렇게 짜는 예제 코드는 pusher.com 참조
# 이 함수는 pusher가 잘 돌아가는지 테스트. 
@app.route('/api/echo', methods=['GET','POST'])
def test_message():
	data = request.form
	p['test_channel'].trigger('echo', {'message' : data['message']})
	return jsonify({"status": 0})

```

다음은 자바스크립트 코드이다. 자바스크립트 코드로 UI를 잡아주기로 한다. 

__main.js__

```javascript

// Enable pusher logging - don't include this in production
/*
Pusher.log = function(message) {
  if (window.console && window.console.log) {
    window.console.log(message);
  }
};
*/

$(document).ready(function() {
    var pusher = new Pusher(PUSHER_KEY)
        testChannel =pusher.subscribe('test_channel'),
        $messages = $('.messages'),
        $inputMessage = $('.inputMessage'),
        chatPage = $('.chat.page');

    /*
    //$.post는 아래의 형태와 같습니다.
    $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: success,
      dataType: dataType
    });
    */

    var initial_delay = 1500;
    setTimeout(function () {
        addChatMessage({'username':'이두희', 'message':'안녕?'});
    },initial_delay + 500)
    setTimeout(function () {
        addChatMessage({'username':'홍진호', 'message':'안녕?'});
    },initial_delay + 1000)
    setTimeout(function () {
        addChatMessage({'username':'홍진호', 'message':'두희야 요즘 눈물 셀카 연습하고 있다매.'});
    },initial_delay + 1500)
    setTimeout(function () {
        addChatMessage({'username':'이두희', 'message':'?????????ㅜㅜㅜㅜㅜㅜ'});
    },initial_delay + 2000)
    
    testChannel.bind('echo', function(data) {
        data['username'] = "김동우";
        addChatMessage(data);
    });

    setTimeout(function () {
        $.post('/api/echo', {"message":"Hello World!"});
    },initial_delay +  4000)
    setTimeout(function () {
        $.post('/api/echo', {"message":"나는 치킨을 먹고싶어"});
    },initial_delay +  5000)
    setTimeout(function () {
        $.post('/api/echo', {"message":"치킨은 언제 오는거야"});    
    },initial_delay +  6000)
    setTimeout(function () {
        $.post('/api/echo', {"message":"두희형 치킨 사주세요ㅠㅠ"});
    },initial_delay +  7000)

    function addChatMessage(data) {
        var $usernameDiv = $('<span class="username"></span>');
        $usernameDiv.css("color", getUsernameColor(data.username));
        $usernameDiv.text(data.username);

        var $messageBodyDiv = $('<span class="messageBody"></span>');
        $messageBodyDiv.text(data.message);

        var typingClass = data.typing ? 'typing' : '';
        var $messageDiv = $('<li class="message ' + typingClass + '"></li>');
        $messageDiv.append($usernameDiv)
            .append($messageBodyDiv)
            .data('username', data.username);

        addMessageElement($messageDiv);
    }

    function addMessageElement(el) {
        var $el = $(el);
        $messages.append($el);

        $messages[0].scrollTop = $messages[0].scrollHeight;
    }

    function getUsernameColor(username) {
        // Compute hash code
        var hash = 7;
        for (var i = 0; i < username.length; i++) {
            hash = username.charCodeAt(i) + (hash << 5) - hash;
        }
        // Calculate color
        var index = Math.abs(hash % 360);
        return "hsl(" + index + ", 77%, 60%)";
    }
});


```

그리고 index.html은 다음과 같이 작성하면 된다. 

__index.html__

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Likelion-last example</title>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
  <ul class="pages">
    <li class="chat page">
      <div class="chatArea">
        <ul class="messages">

        </ul>
      </div>
      <input class="inputMessage" placeholder="Type here..."/>
    </li>
  </ul>

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="//js.pusher.com/2.2/pusher.min.js" type="text/javascript"></script>
<script src="/static/js/pusher_key.js"></script>
<script src="/static/js/main.js"></script>
</body>
</html>
```

< 내 코멘트 >
Javascript를 작성할 때, 우리는 보통 JS가 어디서 작동될 지 모른다. 이 문제를 방지하기 위해서, main.js 에서는 그 부분을 찾아서 직접 append 하도록 명령을 만들었다. (addMessageElement 부분)

[동우가 짠 V1 --> V2 소스코드]("https://github.com/kimdwkimdw/likelion-last-example/compare/V1...V2")

[완성작 V2]("http://v2.likelion-last.appspot.com/")

<hr> 

## V2 --> V3. 어떻게 생겼는지 알았다. 이제 pusher를 이용한 채팅을 구현하자. 

__api.py__ 의 test_message는, 실제로 pusher가 잘 작동되는지 확인하는 코드이다. 이제 다른 함수를 만들어서 실제로 메시지를 날리는 코드를 만들자. 

__api.py__

```python
# -*- coding: utf-8 -*-

from pusher import Pusher
from application import app
from flask import request, render_template, jsonify
from user_info import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET

p = Pusher(
    app_id = PUSHER_APP_ID,
    key = PUSHER_KEY,
    secret = PUSHER_SECRET
)

# 이렇게 짜는 예제 코드는 pusher.com 참조
# 이 함수는 pusher가 잘 돌아가는지 테스트. 
@app.route('/api/echo', methods=['GET','POST'])
def test_message():
    data = request.form
    p['test_channel'].trigger('echo', {'message' : data['message']})
    return jsonify({"status": 0})


# 이게 무슨 함수인지는 나중에 공부하자. 
def emit(action, data, broadcast = False):
	if broadcast:
		p['br'].trigger(action, data)
	else:
		p['private'].trigger(action, data)

def emit_new_message(data):
	emit('new_message', {'message' : data['message']}, broadcast = True)


@app.route('/api/call/<action_name>', methods = ['GET','POST'])
def api_call(action_name):
	data = request.form
	
	emit_new_message(data)
	
	return jsonify({"status": 0})

```

__main.js__

```javascript

$(document).ready(function() {
    var pusher = new Pusher(PUSHER_KEY)
        testChannel =pusher.subscribe('test_channel'),
		
		/* 추가되었다. */
		broadcast = pusher.subscribe('br'),
		$window = $(window),
		
		/* -------- */
		
        $messages = $('.messages'),
        $inputMessage = $('.inputMessage'),
        chatPage = $('.chat.page');

    /*
    //$.post는 아래의 형태와 같습니다.
    $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: success,
      dataType: dataType
    });
    */

    var initial_delay = 1500;
    setTimeout(function () {
        addChatMessage({'username':'이두희', 'message':'안녕?'});
    },initial_delay + 500)
    setTimeout(function () {
        addChatMessage({'username':'홍진호', 'message':'안녕?'});
    },initial_delay + 1000)
    setTimeout(function () {
        addChatMessage({'username':'홍진호', 'message':'두희야 요즘 눈물 셀카 연습하고 있다매.'});
    },initial_delay + 1500)
    setTimeout(function () {
        addChatMessage({'username':'이두희', 'message':'?????????ㅜㅜㅜㅜㅜㅜ'});
    },initial_delay + 2000)
    
    /* 이 부분은 수정 
	testChannel.bind('echo', function(data) {
        data['username'] = "김동우";
        addChatMessage(data);
    });
	 ------------- */
	
	broadcast.bind('new_message', function(data){
		data['username'] = "정용한";
		addChatMessage(data);
	})

	/* 이 부분 날아감 */ 
    setTimeout(function () {
        $.post('/api/echo', {"message":"Hello World!"});
    },initial_delay +  4000)
    setTimeout(function () {
        $.post('/api/echo', {"message":"나는 치킨을 먹고싶어"});
    },initial_delay +  5000)
    setTimeout(function () {
        $.post('/api/echo', {"message":"치킨은 언제 오는거야"});    
    },initial_delay +  6000)
    setTimeout(function () {
        $.post('/api/echo', {"message":"두희형 치킨 사주세요ㅠㅠ"});
    },initial_delay +  7000)
	
	/* ------------- */ 

    function addChatMessage(data) {
        var $usernameDiv = $('<span class="username"></span>');
        $usernameDiv.css("color", getUsernameColor(data.username));
        $usernameDiv.text(data.username);

        var $messageBodyDiv = $('<span class="messageBody"></span>');
        $messageBodyDiv.text(data.message);

        var typingClass = data.typing ? 'typing' : '';
        var $messageDiv = $('<li class="message ' + typingClass + '"></li>');
        $messageDiv.append($usernameDiv)
            .append($messageBodyDiv)
            .data('username', data.username);

        addMessageElement($messageDiv);
    }

    function addMessageElement(el) {
        var $el = $(el);
        $messages.append($el);

        $messages[0].scrollTop = $messages[0].scrollHeight;
    }

    function getUsernameColor(username) {
        // Compute hash code
        var hash = 7;
        for (var i = 0; i < username.length; i++) {
            hash = username.charCodeAt(i) + (hash << 5) - hash;
        }
        // Calculate color
        var index = Math.abs(hash % 360);
        return "hsl(" + index + ", 77%, 60%)";
    }
	
	function sendMessage(){
		var message = $inputMessage.val().trim();
		// if there is a non-empty message
		
		if (message){
			$inputMessage.val('');
			$.post('/api/call/new_message',{"message" : message});
		}
	}
	
	$window.keydown(function(event){
		if (event.which == 13){
			sendMessage();
		}
	})
	
});

```

[동우가 짠 V2 --> V3 소스코드]("https://github.com/kimdwkimdw/likelion-last-example/compare/V2...V3")

[완성작 V3]("http://v3.likelion-last.appspot.com/")


<hr>

## V3 --> V4. Pusher를 통해서 이제 얘기를 나눌 수 있다. 이제 닉네임을 받아서 활동할 수 있도록 해보자.

우리가 해야 할 일은 다음과 같다.

- 닉네임 적는 칸 만들기
- 닉네임을 받아서 말하는 사람에 넣기 

1. username을 변수로 넣기 

__api.py__

```python
# -*- coding: utf-8 -*-

from pusher import Pusher
from application import app
from flask import request, render_template, jsonify
from user_info import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET

p = Pusher(
    app_id = PUSHER_APP_ID,
    key = PUSHER_KEY,
    secret = PUSHER_SECRET
)

# 이렇게 짜는 예제 코드는 pusher.com 참조
# 이 함수는 pusher가 잘 돌아가는지 테스트. 
@app.route('/api/echo', methods=['GET','POST'])
def test_message():
    data = request.form
    p['test_channel'].trigger('echo', {'message' : data['message']})
    return jsonify({"status": 0})


# 이게 무슨 함수인지는 나중에 공부하자. 
def emit(action, data, broadcast = False):
    if broadcast:
        p['br'].trigger(action, data)
    else:
        p['private'].trigger(action, data)

def emit_new_message(data):
#    emit('new_message', {'message' : data['message'] }, broadcast = True)
	 emit('new_message', { 'message': data['message'], 'username': data['username']}, broadcast=True)


@app.route('/api/call/<action_name>', methods = ['GET','POST'])
def api_call(action_name):
    data = request.form

    emit_new_message(data)

    return jsonify({"status": 0})

```


이제 로그인 페이지를 추가한다. 

__main.css__

```css
.login.page{
	background-color : #000;
}

.login.page .form{
	height : 100px ;
	margin-top : -100px;
	position : absolute;
	
	text-align : center;
	top : 50%;
	width : 100%;
}

.login.page .form .usernameInput{
	background-color : transparent;
	border :none;
	border-bottom: 2px solid #fff;
	outline: none;
	padding-bottom: 15px;
	text-align: center;
	width: 400px;
}

.login.page .title{
	font-size : 200%;
}

.login.page .usernameInput{
	font-size: 200%;
	letter-spacing: 3px;
}

.login.page .title, .login.page .usernameInput {
	color: #fff;
	font-weight: 100;
}

```

이제 username을 받도록 javascript를 추가한다. 

```javascript
$(document).ready(function() {
    var pusher = new Pusher(PUSHER_KEY)
        testChannel =pusher.subscribe('test_channel'),
        broadcast = pusher.subscribe('br'),
        $window = $(window),
		
		/* 추가 */
		$usernameInput = $('.usernameInput[name=username]'),
		/* ------ */
		
        $messages = $('.messages'),
        $inputMessage = $('.inputMessage'),
		/* 페이지 추가 */ 
		$loginPage = $('.login.page'),
        $chatPage = $('.chat.page');

	/* 변수 추가 */ 
	var username;
	
	$usernameInput.focus();

    /*
    //$.post는 아래의 형태와 같습니다.
    $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: success,
      dataType: dataType
    });
    */

	/* 이부분 날린다. 
    var initial_delay = 1500;
    setTimeout(function () {
        addChatMessage({'username':'이두희', 'message':'안녕?'});
    },initial_delay + 500)
    setTimeout(function () {
        addChatMessage({'username':'홍진호', 'message':'안녕?'});
    },initial_delay + 1000)
    setTimeout(function () {
        addChatMessage({'username':'홍진호', 'message':'두희야 요즘 눈물 셀카 연습하고 있다매.'});
    },initial_delay + 1500)
    setTimeout(function () {
        addChatMessage({'username':'이두희', 'message':'?????????ㅜㅜㅜㅜㅜㅜ'});
    },initial_delay + 2000)
	
	----------- */ 

   

    broadcast.bind('new_message', function(data){
        /* 이 줄 날림  
		data['username'] = "정용한";
		*/ 
        addChatMessage(data);
    })


    function addChatMessage(data) {
        var $usernameDiv = $('<span class="username"></span>');
        $usernameDiv.css("color", getUsernameColor(data.username));
        $usernameDiv.text(data.username);

        var $messageBodyDiv = $('<span class="messageBody"></span>');
        $messageBodyDiv.text(data.message);

        var typingClass = data.typing ? 'typing' : '';
        var $messageDiv = $('<li class="message ' + typingClass + '"></li>');
        $messageDiv.append($usernameDiv)
            .append($messageBodyDiv)
            .data('username', data.username);

        addMessageElement($messageDiv);
    }

    function addMessageElement(el) {
        var $el = $(el);
        $messages.append($el);

        $messages[0].scrollTop = $messages[0].scrollHeight;
    }

    function getUsernameColor(username) {
        // Compute hash code
        var hash = 7;
        for (var i = 0; i < username.length; i++) {
            hash = username.charCodeAt(i) + (hash << 5) - hash;
        }
        // Calculate color
        var index = Math.abs(hash % 360);
        return "hsl(" + index + ", 77%, 60%)";
    }

    function sendMessage(){
        var message = $inputMessage.val().trim();

		// if there is a non-empty message
        if (message){
            $inputMessage.val('');
            /* api.py 바뀌었으니까 이 부분 수정 
			$.post('/api/call/new_message',{"message" : message});
			*/ 
			
			$.post('/api/call/new_message',{
				"message" : message,
				"username" : username
			});	
        }
    }
	
	/* User 이름을 받는 부분을 추가한다. */ 
	function setUsername(){
		var __username = $usernameInput.val().trim();
		
		// if the username is valid
		if (__username){
			username = __username;
			$loginPage.fadeOut();
			$chatPage.show();
			$inputMessage.focus();
		}
	}
	/* -------------- */ 

    $window.keydown(function(event){
		// When user hit enter
        if (event.which == 13){
			/* user name 입력할 때 구분해야 하니까 이 부분 날린다. 
            sendMessage();
			*/ 
			if (username){
				sendMessage();
			}
			else{
				setUsername();
				$usernameInput.blur();
			}
        }
    })

});
```

__index.html__

```html

<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Likelion-last example</title>
  <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
  <ul class="pages">
    <li class="chat page">
      <div class="chatArea">
        <ul class="messages">

        </ul>
      </div>
      <input class="inputMessage" placeholder="Type here..."/>
    </li>
	
	<li class = "login page">
		<div class = "form">
			<h3 class="title">What's your nickname?</h3>
			<input class="usernameInput" type="text" name="username" maxlength="14">
		</div>
	</li>
	
  </ul>

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="//js.pusher.com/2.2/pusher.min.js" type="text/javascript"></script>
<script src="/static/js/pusher_key.js"></script>
<script src="/static/js/main.js"></script>
</body>
</html>


```

[동우가 짠 V3 --> V4 소스코드]("https://github.com/kimdwkimdw/likelion-last-example/compare/V3...V4")

[완성작 V4]("http://v4.likelion-last.appspot.com/")

<hr>

## V4 --> V5. 이제 ajax를 통해서 서버 응답이 돌아오면 ajax 시작하도록 하자 

#### ajax가 뭐였더라? 
사전적인 설명은, 대화형 웹 어플리케이션 제작을 위해서 사용하는 웹개발 기법이다. HTML, JS, Json을 합쳐서 화면바꿈 없이 필요한 데이터만 받아내는 기법이다. 

기존의 웹어플리케이션은 form data로 데이터를 받고, Controller에서 이를 채워서 다시 내보내기 때문에, 화면의 새로고침이 불가피했다. 반면에, Ajax 기법은 필요한 데이터만을 서버에서 받아낼 수 있다. 

클라이언트 쪽에서는 Javascript가 쓰이고, 이를 Json형태로 받아낸다. 

#### 코딩코딩 

__api.py__

```python
# -*- coding: utf-8 -*-

from pusher import Pusher
from application import app
from flask import request, render_template, jsonify
from user_info import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET

p = Pusher(
    app_id=PUSHER_APP_ID,
    key=PUSHER_KEY,
    secret=PUSHER_SECRET
)

# 이렇게 짜는 예제 코드는 pusher.com 참조
# 이 함수는 pusher가 잘 돌아가는지 테스트. 
@app.route('/api/echo', methods=['GET', 'POST'])
def test_message():
    data = request.form
    p['test_channel'].trigger('echo', {'message': data['message']})
    return jsonify({"status": 0})


# 이게 무슨 함수인지는 나중에 공부하자. 
def emit(action, data, broadcast=False):
    if broadcast:
        p['br'].trigger(action, data)
    else:
        p['private'].trigger(action, data)


def emit_new_message(data):
    # emit('new_message', {'message' : data['message'] }, broadcast = True)
    emit('new_message', {
         'message': data['message'],
         'username': data['username'],
     }, broadcast=True)


# 이 부분 추가
@app.route('/api/start', methods=["POST"])
def api_start():
    data = request.form
    username = data['username']
    emit('user_joined', {'username': username}, broadcast=True)

    return jsonify({'status': 0})


# --------

@app.route('/api/call/<action_name>', methods=["POST"])
def api_call(action_name):
    data = request.form
    emit_new_message(data)
    return jsonify({"status": 0})
```

__main.js__

```javascript
$(document).ready(function() {
    /* 이 부분을 날린다. 왜냐하면, ajax를 통해서 서버응답을 전달하고 싶기 때문
    var pusher = new Pusher(PUSHER_KEY)
        testChannel =pusher.subscribe('test_channel'),
        broadcast = pusher.subscribe('br'),
        $window = $(window),
    */

    var $window = $(window),
        $usernameInput = $('.usernameInput[name=username]'),
        $messages = $('.messages'),
        $inputMessage = $('.inputMessage'),

        $loginPage = $('.login.page'),
        $chatPage = $('.chat.page');


    var username;
    $usernameInput.focus();

    /*
    //$.post는 아래의 형태와 같습니다.
    $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: success,
      dataType: dataType
    });
    */

    /* 이 부분도 날린다. Ajax 응답이 올 때마다 실행하고 싶기 때문이다
    broadcast.bind('new_message', function(data){
        addChatMessage(data);
    })
    */

    function startPusher(){
        var pusher = new Pusher (PUSHER_KEY),
            testChannel = pusher.subscribe('test_channel'),
            broadcast = pusher.subscribe('br');

        broadcast.bind('new_message', function(data){
            addChatMessage(data);
        });

        broadcast.bind('user_join', function(data){
            log(data.username + ' joined');
        });
    }


    function addChatMessage(data) {
        var $usernameDiv = $('<span class="username"></span>');
        $usernameDiv.css("color", getUsernameColor(data.username));
        $usernameDiv.text(data.username);

        var $messageBodyDiv = $('<span class="messageBody"></span>');
        $messageBodyDiv.text(data.message);

        var typingClass = data.typing ? 'typing' : '';
        var $messageDiv = $('<li class="message ' + typingClass + '"></li>');
        $messageDiv.append($usernameDiv)
            .append($messageBodyDiv)
            .data('username', data.username);

        addMessageElement($messageDiv);
    }

    function addMessageElement(el) {
        var $el = $(el);
        $messages.append($el);

        $messages[0].scrollTop = $messages[0].scrollHeight;
    }

    function getUsernameColor(username) {
        // Compute hash code
        var hash = 7;
        for (var i = 0; i < username.length; i++) {
            hash = username.charCodeAt(i) + (hash << 5) - hash;
        }
        // Calculate color
        var index = Math.abs(hash % 360);
        return "hsl(" + index + ", 77%, 60%)";
    }

    function sendMessage(){
        var message = $inputMessage.val().trim();

        // if there is a non-empty message
        if (message) {
             $inputMessage.val('');
             $.post('/api/call/new_message', {
                 "message": message,
                 "username": username
             });
         }
    }

    /* User 이름을 받는 부분을 추가한다. */
    function setUsername() {
         var __username = $usernameInput.val().trim();

         // If the username is valid
         if (__username) {
            $.post("/api/start", {
                    'username': __username,
                },
                function(data) {
                    if (data.status == 0) {
                        username = __username;
                        $loginPage.fadeOut();
                        $chatPage.show();
                        $inputMessage.focus();

                        startPusher();
                        connected = true;
                        // Display the welcome message
                        var message = "Welcome to Chat &mdash; ";
                        log(message);
                    } else {
                        alert("error");
                    }
                }, "json"
            );
         }
     }

    function log(message, options){
        var el = '<li class="log">' + message + '</li>';
        addMessageElement(el, options);
    }

    $window.keydown(function(event){
        // When user hit enter
        if (event.which == 13){
            if (username){
                sendMessage();
            }
            else{
                setUsername();
                $usernameInput.blur();
            }
        }
    })

});
```

[동우가 짠 V4 --> V5 소스코드]("https://github.com/kimdwkimdw/likelion-last-example/compare/V4...V5")

[완성작 V5]("http://v4.likelion-last.appspot.com/")


<hr>

## V5 --> V6 Typing을 인식하자. 

__api.py__

```python
# -*- coding: utf-8 -*-

from pusher import Pusher
from application import app
# from flask import request, render_template, jsonify
# 이렇게 바꾸자
from flask import request, render_template, jsonify, session
from user_info import PUSHER_APP_ID, PUSHER_KEY, PUSHER_SECRET

p = Pusher(
    app_id=PUSHER_APP_ID,
    key=PUSHER_KEY,
    secret=PUSHER_SECRET
)

# 이렇게 짜는 예제 코드는 pusher.com 참조
# 이 함수는 pusher가 잘 돌아가는지 테스트. 
@app.route('/api/echo', methods=['GET', 'POST'])
def test_message():
    data = request.form
    p['test_channel'].trigger('echo', {'message': data['message']})
    return jsonify({"status": 0})


# 이게 무슨 함수인지는 나중에 공부하자. 
def emit(action, data, broadcast=False):
    if broadcast:
        p['br'].trigger(action, data)
    else:
        p['private'].trigger(action, data)


def emit_new_message(data):
    # emit('new_message', {'message' : data['message'] }, broadcast = True)
    emit('new_message', {
         'message': data['message'],
         'username': data['username'],
     }, broadcast=True)


@app.route('/api/start', methods=["POST"])
def api_start():
    data = request.form
    username = data['username']
	
	# 다음 추가 
	user_id = data['user_id']
	session['username'] = username
	session['user_id'] = user_id
	
    emit('user_joined', {'username': username}, broadcast=True)

    return jsonify({'status': 0})


# --------

@app.route('/api/call/<action_name>', methods=["POST"])
def api_call(action_name):
    data = request.form
	
    # emit_new_message(data)
	# 이 부분 추가하자 
	
	if action_name == "new_message":
		emit_new_message(data)
	elif action_name == "typing":
		emit_typing()
	elif action_name == "stop_typing":
		emit_stop_typing()
	
    return jsonify({"status": 0})
	
# Typing 인식하는 함수 만들자 
def emit_typing():
	emit('typing', {
        'username': session['username'],
        'user_id': session['user_id'],
    }, broadcast=True)


def emit_stop_typing():
    emit('stop_typing', {
        'username': session['username'],
        'user_id': session['user_id'],
    }, broadcast=True)

```

__main.js__

```javascript

$(document).ready(function() {
    var $window = $(window),
        $usernameInput = $('.usernameInput[name=username]'),
        $messages = $('.messages'),
        $inputMessage = $('.inputMessage'),

        $loginPage = $('.login.page'),
        $chatPage = $('.chat.page');


    //    var username;
    // user 이름은 이제 회원가입으로 받는다. 

    var username,
        connected = false,
        typing = false,
        lastTypingTime;

    // USER ID는 이제 이렇게 받아서 회원가입을 만든다. 
    var user_id = (function() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 10; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;
    })();

    $usernameInput.focus();

    /*
    //$.post는 아래의 형태와 같습니다.
    $.ajax({
      type: "POST",
      url: url,
      data: data,
      success: success,
      dataType: dataType
    });
    */

    function startPusher(){
        var pusher = new Pusher (PUSHER_KEY),
            testChannel = pusher.subscribe('test_channel'),
            broadcast = pusher.subscribe('br');

        broadcast.bind('new_message', function(data){
            addChatMessage(data);
        });

        broadcast.bind('user_join', function(data){
            log(data.username + ' joined');
        });

        /* 이 부분 추가됨 */ 
        broadcast.bind('typing', function(data) {
            if (data['user_id'] == user_id) return;
            addChatTyping(data);
        });

        // Whenever the server emits 'stop typing', kill the typing message
        broadcast.bind('stop_typing', function(data) {
            if (data['user_id'] == user_id) return;
            removeChatTyping(data);
        });
        /* ------- */        
    }


    function addChatMessage(data) {
        var $usernameDiv = $('<span class="username"></span>');
        $usernameDiv.css("color", getUsernameColor(data.username));
        $usernameDiv.text(data.username);

        var $messageBodyDiv = $('<span class="messageBody"></span>');
        $messageBodyDiv.text(data.message);

        // 이 부분 추가됨 
        var typingClass = data.typing ? 'typing' : ''; 
        var $messageDiv = $('<li class="message ' + typingClass + '"></li>');
        $messageDiv.append($usernameDiv)
             .append($messageBodyDiv)
             .data('username', data.username);

        if (data.typing) {
            $messageDiv.hide().fadeIn(150);
        }
        // ------------

         addMessageElement($messageDiv);



        var $messageDiv = $('<li class="message ' + typingClass + '"></li>');
        $messageDiv.append($usernameDiv)
            .append($messageBodyDiv)
            .data('username', data.username);

        addMessageElement($messageDiv);
    }

    function addMessageElement(el) {
        var $el = $(el);
        $messages.append($el);

        $messages[0].scrollTop = $messages[0].scrollHeight;
    }

    function getUsernameColor(username) {
        // Compute hash code
        var hash = 7;
        for (var i = 0; i < username.length; i++) {
            hash = username.charCodeAt(i) + (hash << 5) - hash;
        }
        // Calculate color
        var index = Math.abs(hash % 360);
        return "hsl(" + index + ", 77%, 60%)";
    }

    function sendMessage(){
        var message = $inputMessage.val().trim();

        // if there is a non-empty message
        if (message) {
             $inputMessage.val('');
             $.post('/api/call/new_message', {
                 "message": message,
                 "username": username
             });
         }
    }

    /* User 이름을 받는 부분을 추가한다. */
    function setUsername() {
         var __username = $usernameInput.val().trim();

         // If the username is valid
         if (__username) {
            $.post("/api/start", {
                    'username': __username,
                    // 추가 
                    'user_id': user_id,
                },
                function(data) {
                    if (data.status == 0) {
                        username = __username;
                        $loginPage.fadeOut();
                        $chatPage.show();
                        $inputMessage.focus();

                        startPusher();
                        connected = true;
                        // Display the welcome message
                        var message = "Welcome to Chat &mdash; ";
                        log(message);
                    } else {
                        alert("error");
                    }
                }, "json"
            );
         }
     }

    function log(message, options){
        var el = '<li class="log">' + message + '</li>';
        addMessageElement(el, options);
    }

    // Typing을 인식하자. 

    function addChatTyping(data) {
        data.typing = true;
        data.message = 'is typing';
        $('.typing.message').remove();
        addChatMessage(data);
    }

    function removeChatTyping(data) {
        $('.typing.message').fadeOut(function() {
            $(this).remove();
        });
    }

    function updateTyping() {
        var TYPING_TIMER_LENGTH = 400; // ms
        if (connected) {
            if (!typing) {
                typing = true;
                $.post('/api/call/typing');
            }
            lastTypingTime = (new Date()).getTime();

            setTimeout(function() {
                var typingTimer = (new Date()).getTime();
                var timeDiff = typingTimer - lastTypingTime;
                if (timeDiff >= TYPING_TIMER_LENGTH && typing) {
                    $.post('/api/call/stop_typing');
                    typing = false;
                }
            }, TYPING_TIMER_LENGTH);
        }
    }



    $window.keydown(function(event){
        // When user hit enter
        if (event.which == 13){
            if (username){
                sendMessage();
            }
            else{
                setUsername();
                $usernameInput.blur();
            }
        }
    });

    // 이 부분 추가 
    $inputMessage.on('input', function() {
        updateTyping();
    });

});

```


