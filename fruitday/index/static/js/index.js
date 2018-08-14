$(function(){
  //网页加载时要运行的操作
    //加载以及处理登录信息
  loadGoods();
  //异步加载商品列表
  check_login();

});

//异步加载商品类型以及商品列表
function loadGoods(){
  $.get('/all_type_goods/',function(data){
    var show = "";
    $.each(data,function(i,obj){
      var html="";
      html+="<div class='item'>";
      //将 obj.type 转换为 json 对象
      jsonType=JSON.parse(obj.type);
        html+="<p class='title'>";
          html+="<a href='#'>更多</a>";
          html+="<img src='/"+jsonType.picture+"'>";
        html+="</p>";
        html+="<ul>";
        console.log(jsonType);
        //将obj.goods由字符串转换为json数组
        jsonGoods=JSON.parse(obj.goods);
        //循环遍历jsonGoods中的每一项内容,构建<li></li>
        $.each(jsonGoods,function(j,good){
            if((j+1)%5==0){
                html += "<li class='no-margin'>";
            }else{
                html+="<li>"
            }
            html+=">";
              html+="<p>";
                html+="<img src='/"+good.fields.picture+"'>";
              html+="</p>";
              html+="<div class='content'>";
                html+="<a href='javascript:add_cart("+good.pk+");' class='cart'>";
                  html+="<img src='/static/images/cart.png'>";
                html+="</a>";
              html+="<p>";
                html+=good.fields.title;
              html+="</p>";
              html+="<span>";
                html+="&yen";
                html+=good.fields.price+"/";
                html+=good.fields.spec;
              html+="</span>";
              html+="</div>";
            html+="</li>";


        });
        html+="</ul>";
      html+="</div>";
      console.log(html);
      show += html;
    });
    console.log("******");
    console.log(show);
    //将拼好的show的内容填充到#main元素中
    $("#main").html(show);
  },'json');


}




function check_login(){
  $.get('/check_login/',function(data){
    var html="";
    //判断是否有登录信息
    if(data.loginStatus == 0){
      html+="<a href='/login/'>[登录]</a>";
      html+="<a href='/register/'>[注册有惊喜]</a>";
    }else{
      html+="欢迎:"+data.uname;
      html+="&nbsp;&nbsp;&nbsp;&nbsp;";
      html+="<a href='/logout/'>退出</a>";
    }
    $("#login-info").html(html);
  },'json');
}




/*
* 添加商品至购物车(异步)
* 参数good_id：需要添加至购物车的id
* */
function add_cart(good_id) {
   /*
   * 验证是否有用户处于用户状态，
   * 如果未处于登录状态，则给出提示
   *否则将信息传递给服务器 */
   $.get('/check_login',function(data) {
       if(data.loginStatus == 0){
           alert('请先登录');
       }else{
         //向add_cart发送异步请求，并将good_id作为参数传递过去
           $.post('/add_cart/',{
               'good_id':good_id,
               'csrfmiddlewaretoken':$.cookie('csrftoken')
               },
               function(data){
                if(data.status==1){
                  alert('添加购物车成功');
                }else{
                  alert('添加购物车失败');
                }

               },'json');
            }

       }
   ,'json');
}