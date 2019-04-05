function changeDivColor(){
var colors = ['rgba(0,0,0,0.9)', 'rgba(0,0,0,0.3)', 'rgba(0,0,0,0.6)', 'rgba(0,0,0,0.1)'];
var boxes = document.querySelectorAll(".boxes");
// for (i=0; i <boxes.length; i++)
//   {
//   boxes[i].style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
//   await sleep(100);
//   }
boxes[Math.floor(Math.random() * boxes.length)].style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
};
$(function(){
    changeDivColor();
    var int = setInterval("changeDivColor()", 100);
});
