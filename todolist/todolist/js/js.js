//首先加载此函数，此函数的用途是加载localstorage内的数据
//如果有数据则显示，如果没有则不显示，实现页面刷新时数据还在
showData();


// 获取id对象的函数
function $(id){
  return document.getElementById(id);
}

var insert = document.getElementsByClassName('userinput')[0];
var oText = $('text');

// 试了onkeyup和onkeypress他妹的效果不好
oText.onkeydown = function(){
    //如果值不为空且监听事件的按钮是enter键时
    if(oText.value != '' && event.keyCode==13){
        var oLi = document.createElement('li');
        var data = loadData();
        temp = {"cont":oText.value.trim(),"done":false};
        data.push(temp);
        dumpData(data);
        showData();
        oText.value = '';
    }
};


//显示数据在页面上的函数
function showData(){
    var todolist = document.getElementsByClassName('todolist')[0];
    var endlist = document.getElementsByClassName('endlist')[0];
    var todocount = 0;
    var endcount = 0;
    var todostring = '';
    var endstring = '';
    var data = loadData();
    if(data){
        console.log(data.length);
        //倒序取，可以把最新的数据放在最前面
        for(var i=data.length-1;i>=0;i--){
        //for(var i=0;i<=data.length-1;i++){
        //for(var i in data){

            // 已完成事项
            if(data[i].done){
                endstring+="<li><input type='checkbox' onchange='update("+i+",\"done\",false)' checked='checked'>"
                +"<p class='words' id='p"+i+"' onclick='edit("+i+")'>"+data[i].cont
                +"</p><a href='javascript:remove("+i+")'>X</a></li>";
                //注意这里的javascript:remove，是冒号不是分好
                endcount++;

            //待办事项
            }else{
                todostring+="<li><input type='checkbox' onchange='update("+i+",\"done\",true)'>"
                +"<p class='words' id='p"+i+"' onclick='edit("+i+")'>"+data[i].cont
                +"</p><a href='javascript:remove("+i+")'>X</a></li>";
                todocount++;
            }
        }
        todolist.innerHTML = todostring;
        endlist.innerHTML = endstring;
        $('todocount').innerText = todocount;
        $('endcount').innerText = endcount;
    }else{  //如果本地仓库没有值则为默认的空
        todolist.innerHTML = '';
        endlist.innerHTML = '';
        $('todocount').innerText = 0;
        $('endcount').innerText = 0;
    }
}


//加载数据
function loadData(){
    //将字符串解析为json对象
    var data = JSON.parse(localStorage.getItem("todo"));
    if(data==null){
        return []
    }else{
        return data
    }
}

//保存数据

function dumpData(data){
    //如果有值
    if(data){
        //将json对象转为字符串，因为localstorage存储的是字符串
        localStorage.setItem('todo',JSON.stringify(data));
    }
}

//删除数据

function remove(arg){
    var data = loadData();
    //删除选中的数据并存储新的数据仅本地仓库
    data.splice(arg,1);  //splice、slice不同的用法注意区分，他妹的费了好多时间
    dumpData(data);
    showData();
}

//修改数据所属类型，待办和已完成
function update(i,key,value){
    var data = loadData();
    var tempdata = data.splice(i,1)[0];     //被取出的数据
    tempdata[key] = value;                  //将此数据赋予新的键值对
    data.splice(i,0,tempdata);              //将已修改的数添加进本地仓库
    dumpData(data);
    showData();
}

//编辑数据内容

function edit(i){
	var p = document.getElementById("p"+i);
	cont = p.innerHTML;                            //临时存放该数据
	p.innerHTML="<input id='input-"+i+"' value='"+cont+"' />";
	var input = document.getElementById("input-"+i);
	input.setSelectionRange(0,input.value.length); //设置input元素内文本范围，从0开始到输入的值的长度
	input.focus();                                 //聚焦，选中文本时，此时修改数据
	input.onblur =function(){                      //当聚焦取消时，非选中文本状态
		if(input.value.length == 0){
			p.innerHTML = cont;                    //如果数据为空恢复之前的数据
			alert("内容不能为空");
		}
		else{
			update(i,'cont',input.value);          //修改数据的值
		}
	};
}

// 清除数据
$('clear').onclick = function(){
    localStorage.clear();
    showData();
    //window.location.reload();
};
