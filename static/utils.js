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

NJPress.api = function(api, args, callback) {
  $.ajax({
    type: 'GET',
    url: '/api/' + api,
    data: args,
    success: function(r) {
      callback(null, JSON.parse(r));
    },
    error: callback
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
  return L.protocol + '//' + L.hostname + port;
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

NJPress.loadComments = function(commentsHead, commentsTable) {
  var splits = location.pathname.split('/');
  var postId = splits[splits.length - 1];
  NJPress.api('comments_for/' + postId, '', function(error, comments) {
    if (error) {
        commentsHead.text('Failed to load comments');
        return console.error(error);
    }
    for (var i = 0; i < comments.length; ++i) {
        NJPress.addComment(comments[i], commentsHead, commentsTable);
    }
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
    if (paths[5] === 'core.css') {
        return;
    }
    paths[4] = style;
    c.href = paths.join('/');
  });
  localStorage.style = style;
};

$(document).ready(function() {
  var styleArg = NJPress.pageArgs()['style'];
  if (styleArg && ['midnight', 'rainbow'].indexOf(styleArg) != -1) {
    localStorage.style = styleArg;
  } else if (!localStorage.style) {
    localStorage.style = NJPress.style;
  }
  NJPress.replaceStyle(localStorage.style);

  var cb = $('.menu input[type="checkbox"]');
  cb.each(function(i, e) {
    e.onchange = function() {
      clearSelection(i);
    };
  });
  function clearSelection(i) {
    cb.each(function(j, e) {
      if (i !== j) {
        e.checked = false;
      }
    });
  }
  $('body').click(function(e) {
    clearSelection(-1);
  });
  $('#top-menu').click(function(e) {
    e.stopPropagation();
  });

  NJPress.api('nav', {}, function(err, result) {
    if (err) {
      $('#loading-tags').text('Failed to load tags');
      $('#loading-posts').text('Failed to load recent posts');
      return console.error(err);
    }

    processTags($('#loading-tags').text('Post tags: '), result.tags);

    $('#loading-posts').remove();
    for (var i = 0; i < result.posts.length; ++i) {
      var post = result.posts[i];
      $('#recent-posts-list').append($('<li>').append(
        $('<a>').attr('href', '/p/' + post.id).html(post.title)));
    }
  });

  function processTags(element, tags) {
    var maxCount = 0;
    var allTags = Object.keys(tags);
    for (var i = 0; i < allTags.length; ++i) {
      maxCount = Math.max(tags[allTags[i]], maxCount);
    }

    var tagSizes = [];
    var max = 3;
    var factor = 2.5;
    for (var i = 0; i < allTags.length; ++i) {
      tagSizes.push({
        tag: allTags[i],
        size: max - factor * (maxCount - tags[allTags[i]]) / maxCount
      });
    }

    tagSizes.sort(function(a, b) {
      if (a.tag > b.tag) {
        return 1;
      }
      if (a.tag < b.tag) {
        return -1;
      }
      return 0;
    });

    for (var i = 0; i < tagSizes.length; ++i) {
      var t = tagSizes[i];
      element.append($('<a>').attr('href', '/tag/' + t.tag).text(t.tag).css('font-size', t.size.toFixed(2) + 'em'));
    }
  }
});
