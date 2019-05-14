$(function(){
    $('.user a').click(function(){
        addusers();
    });

    $('.realse').click(function(){
       addnews();
    });


    //发布页，添加新闻的函数
    function addnews(){
        if($('#news-curtain').length){ //如果html标签内有此元素，修改样式即可，不用再重复添加元素，增大html
            $('#news-curtain').css('display','block');
        }else{                         //如果没有，第一次加载网页的时候
            var newscurtain = document.createElement('div');
            //创建幕布
            newscurtain.id = 'news-curtain';
            var style1 = {
                width: '100%',
                height:document.body.scrollHeight,  //网页正文全文高,达到自适应网页高度
                background: 'rgba(0,0,0,0.5)',
                position:'absolute',
                'z-index':'9999999999'

            };
            $(newscurtain).css(style1);
            //创建分享新闻页面

            var news = document.createElement('div');
            var style2 = {
                width: '50%',
                height:'45%',  //网页正文全文高,达到自适应网页高度
                background:'#fff',
                'margin-top':'10%',
                'margin-left':document.body.scrollWidth/4,
                'border-radius':'8px',
                'border': '1px solid #abd6f0',
            };

            $(news).css(style2);
            news.id = 'news-share';

            var box = document.createElement('div');
            box.className = 'news-share-box';

            var p = document.createElement('div');
            p.id = 'news-share-title';
            p.innerHTML = '<span>分享新发现</span><input class="close" type="button" value="x">';
            box.appendChild(p);
            news.appendChild(box);

            var tabs = $('<div class="tab"></div>')[0];
            addtab(tabs);
            var datas = $('<div class="news-data"></div>')[0];
            addnewData(datas);

            var under = $('<div class="news-under"></div>')[0];
            addunder(under);
            //var tabs = document.createElement('div');
            //tabs.className = 'tab';
            //addtab(tabs);
            //var datas = document.createElement('div');
            //tabs.className = 'news-data';
            //addnewData(datas);

            $(news).append(tabs);
            $(news).append(datas);
            $(news).append(under);

            $(newscurtain).append(news);
            $('body').prepend(newscurtain);
        }
        //关闭幕布
        $('#news-share-title .close').click(function(){
            $('#news-curtain').css('display','none');
        })


        //tab选项卡点击事件
        for(let k=0;k<$('.tab a').length;k++){
            $($('.tab a')[k]).click(function(){
                $($('.tab a')[k]).addClass('active').siblings('a').removeClass('active');
                console.log($($('.news-data>div')[k]));
                $($('.news-data>div')[k]).css('display','block').siblings('div').css('display','none');
            })
        }

        $('.link').keyup(function(){
            console.log('test');
            if($('.link').val()){
                console.dir($('.disable'));
                $('.disable')[0].removeAttribute('disabled');
                $('.disable')[1].removeAttribute('disabled');
            }
        })
    }

    //登录注册函数

    function addusers(){
        if($('#curtain').length){ //如果html标签内有此元素，修改样式即可，不用再重复添加元素，增大html
            $('#curtain').css('display','block');
        }else {                  //如果没有则创建，第一次加载网页的时候
            var curtain = document.createElement('div');
            //创建幕布
            curtain.id = 'curtain';
            var style1 = {
                width: '100%',
                height: document.body.scrollHeight,  //网页正文全文高,达到自适应网页高度
                background: 'rgba(0,0,0,0.5)',
                position: 'absolute',
                'z-index': '9999999999'

            };
            $(curtain).css(style1);
            //创建登录注册页面

            var users = document.createElement('div');
            var style2 = {
                width: '50%',
                height: document.body.scrollHeight / 3,  //网页正文全文高,达到自适应网页高度
                position: 'fixed',
                'z-index': '9999999999',
                background: '#fff',
                'margin-top': '10%',
                'margin-left': document.body.scrollWidth / 4,
                'border-radius': '4px',
                'border': '1px solid #abd6f0'
            };

            $(users).css(style2);
            users.id = 'users';

            var box = document.createElement('div');
            box.className = 'users-box';

            var p = document.createElement('div');
            p.id = 'users-title';
            p.innerHTML = '<span>注册</span><span>登录</span><input class="close" type="button" value="x">';

            var regist = document.createElement('div');
            regist.className = 'regist';
            addregist(regist);

            var login = document.createElement('div');
            login.className = 'login';
            addlogin(login);

            box.appendChild(p);
            box.appendChild(regist);
            box.appendChild(login);

            users.appendChild(box);
            $(curtain).append(users);
            $('body').prepend(curtain);
        }

        //关闭幕布
        $('#users-title .close').click(function(){
            $('#curtain').css('display','none');
        })
    }
    //注册内容
    function addregist(registobj){
        var cont1 = '<div><input type="text" name="username" placeholder="您的账户名">'+
                '<div><input type="text" name="password" placeholder="您的密码"></div>'+
            '<span>立即注册</span>';
        registobj.innerHTML = cont1;
    }

    //登录内容
    function addlogin(loginobj){
        var cont2 = '<div class="active"><input type="text" name="username" placeholder="您的账户名">'+
                '<div><input type="text" name="password" placeholder="您的密码"></div>'+
                '<span>立即登录</span>';
        loginobj.innerHTML = cont2;
    }
    //function  addbtn(btnobj){
    //    var cont3 = '<input type="button" value="X">';
    //    btnobj.innerHTML =cont3;
    //}

    //发布页tab选项函数
    function addtab(tabobj){
        var cont4 = '<a class="active" href="javascript:void(0)">链接</a>' +
                    '<a href="javascript:void(0)">文字</a>' +
                    '<a href="javascript:void(0)">图片</a>';
        tabobj.innerHTML = cont4;
    }

    //发布页分类内容函数
    function  addnewData(dataobj){
        var cont5 = '<div style="display:block;"><p>添加链接：</p><input class="link" type="text" placeholder="http://">' +
            '<a href="#">获取标题</a>' +
            '<p>标题</p><input class="disable" type="text" disabled>' +
            '<p>添加摘要(必填)</p><input  class="disable" type="text" disabled></div>' +

            '<div><div class="textarea"><textarea maxlength="150" class="textarea">' +
            '</textarea><span>还可以输入150字</span></div></div>'+

            '<div><p>添加图片</p><a href="#">上传' +
            '<input type="file" accept="image/jpeg,image/png/,image/gif "></a>' +
            '<span>支持jpg、jpeg、gif、png格式，且不超过5MB</span>' +
            '<div class="textarea"><textarea maxlength="150"></textarea><span>还可以输入150字</span></div></div>';
        dataobj.innerHTML = cont5;
    }

    //发布页确认发布和清空按钮
    function addunder(underobj){
        var cont6 = '<div><span>发布到：</span><a href="#" class="active">42区</a><a href="#">段子</a>' +
            '<a href="#">挨踢1024</a><a href="#">你问我答</a></div>' +
            '<div class="under-btn"><a href="#">清空</a><a href="#">发布</a></div>';
        underobj.innerHTML = cont6;
    }


    //点赞
    for(let i=0;i<$('.praise').length;i++){
        $($('.praise')[i]).click(function(){
            //console.log(i);
            $('.praise')[i].style.backgroundPosition = '0 -20px';
        })
    }

    //显示、关闭评论
    for(let j=0;j<$('.discuss').length;j++){
        $($('.discuss')[j]).click(function(){
            this.style.backgroundPosition = '0 -80px';
            $($('.discuss-detail')[j]).css('display','block');
            closedetail($('.discuss-detail')[j],this);
            addis(j);
        });


    }

    //关闭评论函数
    function closedetail(obj,obj2){
        //$(obj.children[0])是右上角的X
        $(obj.children[0]).click(function(){
            $(obj).css('display','none');
            obj2.style.backgroundPosition = '0 -99px';
        });

        //$(obj.children[3])是右下角的收起
        $(obj.children[3]).click(function(){
            $(obj).css('display','none');
            obj2.style.backgroundPosition = '0 -99px';
        })
    }


    //根据用户的输入，判断数据真实状态，并把输入的数据添加到页面函数
    function addis(index){
        $($('.add')[index]).click(function(){
            var value = $($('.addiscuss')[index]).val();
            if(value) {
                //点击评论按钮提交
                var li = document.createElement('li');
                li.innerText = value;
                $($('.exist-discuss ul')[index]).append(li);    //添加到页面里
                $('.addiscuss')[index].value = '';              //清空input里的数据
            }else{
                alert('数据不能为空');
            }
        });
        $($('.form')[index]).keydown(function(evnet){
            if(evnet.keyCode==13) {
                var value = $($('.addiscuss')[index]).val();
                if(value){
                    //回车提交
                    var li = document.createElement('li');
                    li.innerText = value;
                    $($('.exist-discuss ul')[index]).append(li);    //添加到页面里
                    $('.addiscuss')[index].value = '';              //清空input里的数据
                }else{
                alert('数据不能为空');
                }
            }
        });
    }
});