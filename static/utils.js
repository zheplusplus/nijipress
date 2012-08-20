var NJPress = {};

NJPress.newNode = function(tag) {
  return document.createElement(tag);
};

NJPress.request = function(url, args, success) {
  $.ajax({
    type: 'POST',
    url: url,
    data: JSON.stringify(args),
    success: function(r) {
      success(JSON.parse(r));
    }
  });
};

NJPress.reqList = function(url, args, successMappingFunc) {
  NJPress.request(url, args, function(result) {
    result.map(successMappingFunc);
  });
};

NJPress.location = function() {
  var L = window.location;
  var port = (L.port == '80' || L.port == '') ? '' : (':' + L.port);
  return L.protocol + '//' + L.hostname + port + L.pathname;
};

NJPress.pageArgs = function() {
  var result = {};
  var url = window.location.href;
  var begin = url.indexOf('?') + 1;
  var end = url.indexOf('#');
  if (end == -1) end = url.length;
  var parameters = url.slice(begin, end).split('&');
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

NJPress.loadTagsIn = function(node) {
  NJPress.reqList('/json/posttags', {}, function(tag) {
    var a = NJPress.newNode('a');
    a.innerHTML = NJPress.escape(tag.name);
    a.href = '/?tag=' + encodeURIComponent(tag.name);
    a.style.fontSize = (8 + 16 * tag.rate) + 'px';
    node.appendChild(a);
  });
};

NJPress.loadPosts = function(nodeRecv) {
  NJPress.reqList('/json/recentposts', {}, function(post) {
    var div = NJPress.newNode('div');
    if (post.id != undefined) {
      var a = NJPress.newNode('a');
      a.innerHTML = post.title;
      a.href = '/?p=' + post.id;
      div.appendChild(a);
    }
    if (post.preview) {
      var article = NJPress.newNode('article');
      article.innerHTML = post.preview;
      div.appendChild(article);
    }
    if (post.content) {
      var article = NJPress.newNode('article');
      article.innerHTML = post.content;
      div.appendChild(article);
    }
    if (div.childNodes.length == 1) {
      return nodeRecv(div.childNodes[0]);
    }
    nodeRecv(div);
  });
};

NJPress.addComment = function(comment, commentsHead, commentsTable) {
  commentsHead.html('Comments:');
  var row = commentsTable.insertRow(-1);
  row.className = 'comment';

  var icon = row.insertCell(-1);
  icon.style.width = '48px';
  icon.style.verticalAlign = 'top';
  var iconImg = document.createElement('img');
  iconImg.src = 'http://0.gravatar.com/avatar/' + comment.email_md5 + '?s=48';
  iconImg.style.borderRadius = '4px';
  icon.appendChild(iconImg);

  var content = row.insertCell(-1);
  content.className = 'text';
  var commentHead = document.createElement('p');
  commentHead.className = 'comment_head';
  if (comment.author) {
    commentHead.innerHTML = NJPress.escape(comment.author).bold();
  } else {
    commentHead.innerHTML = 'Anonymous '.italics();
  }

  if (comment.url.length > 0) {
      var link = document.createElement('a');
      link.innerHTML = NJPress.escape('<^>');
      link.href = comment.url;
      commentHead.appendChild(link);
  }

  commentHead.innerHTML += ' said,';
  var postDate = document.createElement('span');
  postDate.className = 'date';
  postDate.innerHTML = ' at ' + comment.date + ' (UTC)'.sub();
  commentHead.appendChild(postDate);
  content.appendChild(commentHead);

  var contentBody = document.createElement('p');
  contentBody.className = 'comment_content';
  contentBody.innerHTML = comment.content;
  content.appendChild(contentBody);
};

NJPress.loadComments = function(postId, commentsHead, commentsTable) {
  const URI = '/json/loadcomments';
  NJPress.reqList(URI, { post: postId }, function(comment) {
    NJPress.addComment(comment, commentsHead, commentsTable);
  });
};

NJPress.valuesOf = function(arr) {
  return arr.map(function(i) { return arr[i].value; }).toArray().join(' ');
};

NJPress.replaceStyle = function(style) {
  $('link').toArray().filter(function(c) {
    return c.type === 'text/css';
  }).map(function(c) {
    var paths = c.href.split('/');
    c.href = '/static/' + style + '/' + paths[paths.length - 1];
  });
  localStorage.style = style;
};
