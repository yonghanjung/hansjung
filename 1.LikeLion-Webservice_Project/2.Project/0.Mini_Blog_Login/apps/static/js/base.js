//시간을 재서 해당 시간만큼 프로그램에 딜레이를 주는 자바스크립트 코드
//Ajax를 받아오는 시간만큼 약간의 딜레이를 주기 위함
function sleep (milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

// 글이 작성된 시간을 Jinja가 표현하는 방식에 맞게 변환해주는 함수
//서버 위치의 시간으로 시간이 저장되므로 UTC 시간을 기준으로 저장한다.
function timeTo(time){

    var times = new Date();
    var resultString;

    var millisec;
    millisec = (new Date(time)).getTime();
    times.setTime(millisec);
    var month = times.getUTCMonth() + 1;
    if(month < 10){
        month = "0"+ month;
    }
    var date = times.getUTCDate();
    if(date < 10){
        date = "0" + date;
    }

    resultString = 
    times.getYear()+1900 + "-" + month + "-" + date + " "
    +times.getUTCHours() + ":" + times.getMinutes() + ":" + times.getSeconds();
    return resultString;
}


//글 번호를 받아 JSON을 이용해 Ajax로 서버에 요청한다.
function getArticle(number) {
    var EndArticle = false;
    //글번호인 number라는 값을 number라는 Json 키에 넣어 전송한다.
    $.ajax({
        url:"/more",
        dataType: 'JSON',
        data: {
            number : number
        },
        //전송에 성공하면 success 부분이 실행됨
        //매개변수 data는 성공하였을 때 서버로부터 받아온 값
        success: function(data) {
            if(data.id < 1){
                string = "<div class='well' id='article_"+ data.id 
                +"'><h1>마지막 글입니다.</h1></div>";
                $("#results").append(string);
                $("#morebtn").hide();
                EndArticle =true;
            }else{

                string = "<div class='well' id='article_"+ data.id 
                +"'><h1><a href='/article/detail/"+ data.id +"'>"
                + data.title +"</a></h1><h3>"+ data.author +"</h3><h6>"
                + timeTo(data.data_created)
                +"</h6><p> "
                + data.content +" </p> </div>";
                $("#results").append(string);
            }

        },
        //에러가 발생하면 다음의 부분이 실행
        error: function(status){
            string = "<div class='well' id='article_"+ data.id 
            +"'><h1>에러가 발생했습니다..</h1></div>";
            $("#results").append(string);
        }
    });
    return true;
}

$(document).ready(function() {
    var number = 0;
    var string;

    $.ajax({
        url:"/rows",
        dataType: 'JSON',
        success: function(data) {
            number = data.rows - 4;
        }
    });
    $('#load_more_button').bind('click', function() {
        for(var i = 0; i < 5; i++){
            sleep(200);
            number--;
            getArticle(number);
            if(number < 1){
                break;
            }
        }

        return false;
    });
});