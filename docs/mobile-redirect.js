(function(){
  var mob=/Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  var sa=window.matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
  if(mob&&!sa) window.location.replace('/app.html');
})();
