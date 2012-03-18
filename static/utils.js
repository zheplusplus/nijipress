var NJPress = {};

NJPress.request = function(url, args, success) {
  $.ajax({
    type: 'POST',
    url: url,
    data: args,
    success: function(r) {
      success(eval('(' + r + ')'));
    }
  });
};

NJPress.reqList = function(url, args, successMappingFunc) {
  NJPress.request(url, args, function(result) {
    result.map(successMappingFunc);
  });
}

NJPress.pageArgs = function() {
  var result = {};
  var url = window.location.href;
  var parameters = url.slice(url.indexOf('?') + 1).split('&');
  for(var i = 0;  i < parameters.length; i++) {
    var p = parameters[i].split('=');
    result[p[0]] = p[1];
  }
  return result;
};

NJPress.escape = function(t) {
  return t.replace(/&/g, '&amp;').replace(/>/g, '&gt;').replace(/</g, '&lt;')
          .replace(/"/g, '&quot;');
};
