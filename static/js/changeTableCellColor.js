function changeColor(){
var colorParm = document.getElementById("changeColor");
var x = document.getElementsByClassName("tableRowA");
    if (+colorParm.innerHTML > 0.20){
      for(var i=0; i<x.length; i++) {
      x[i].style.backgroundColor = "green";
    }
}else if (+colorParm.innerHTML < 0.20){
      for(var i=0; i<x.length; i++) {
      x[i].style.backgroundColor = "red";
    }}
// }else if(colorParm.innerHTML == "Buy"){
//       for(var i=0; i<x.length; i++) {
//       x[i].style.backgroundColor = "green";
//     }
// }
};
$(function(){
    changeColor();
    var int = setInterval("changeColor()", 10);
});
