function changeColor(){
var colors = ['rgba(0,0,0,0.9)', 'rgba(0,0,0,0.3)', 'rgba(0,0,0,0.5)', 'rgba(0,0,0,0.7)']
var boxes = document.querySelectorAll(".boxes")
for (i=0; i <boxes.length; i++)
  {
  boxes[i].style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
  }
};
$(function(){
    changeColor();
    var int = setInterval("changeColor()", 4000);
});
