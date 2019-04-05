function refresh() {
  var urls = [{% url 'stockWatchlistRefresh' %},{% url 'forexWatchlistRefresh' %}
              , {% url 'MarketStatusView' %}];
  var divs = ['#box2', '#box1', '#box3'];
  for(i=0; i< divs.length;i++){
    $.ajax({
      url: urls[i],
      success: function(data) {
      $(divs[i]).html(data);
      }
    });
  }
};
$(function(){
  refresh();
  var int = setInterval("refresh()", 1000);
});
