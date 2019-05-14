// 获取id对象函数
function $(id){
  return document.getElementById(id);
}

var insert = document.getElementsByClassName('userinput')[0];
var oText = $('text');
var userinput = document.getElementsByClassName('userinput')[0];

// 试了onkeyup，他妈的效果不好
oText.onkeydown = function(){
    //如果值不为空且监听事件的按钮是enter键时
    if(oText.value != '' && event.keyCode==13){
        var oLi = document.createElement('li');
        oLi.innerText = oText.value.trim();
        userinput.appendChild(oLi);
        oText.value = '';
    }


    var number1 = document.getElementsByClassName('number1')[0];
    if(userinput.length){
        number1.innerHTML = userinput.length;
    }
};
