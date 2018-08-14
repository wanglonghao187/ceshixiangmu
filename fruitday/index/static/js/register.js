$(function(){
    //为#formReg绑定的submit事件
    $("#formReg").submit(function(){
        if($("#upwd").val() != $('#cpwd').val()){
            alert('两次密码不一致,请重新输入')
            return false;
        }
        //判断用户手机号是否已经存在
        if(check_phone()=='用户名已经存在'){
            //如果返回值为1，表示手机号码已经存在，阻止表单提交
            return false;
        }
        return true;

    });
    //为name=uphone的元素绑定blur事件
    $("input[name='uphone']").blur(function(){
        alert('进来了');
      // $.get(url,data,callback,type);
        check_phone();
    });
});


  /*
  *验证手机号码是否存在的操作(异步)
  * 返回值：{status：状态码,msg:状态文本}*/
  function check_phone() {

      $.get('/checkphone',"uphone="+$("input[name='uphone']").val(),function(data){
            //data:成功时响应的数据
            data = JSON.parse(data);
            // console.log(data);
            $("#uphone-show").html(data.msg);

        });

  }
