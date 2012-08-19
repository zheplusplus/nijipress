NJPress.typoComment = function(comment, commentsTable) {
  var row = commentsTable.insertRow(-1);

  var icon = row.insertCell(-1);
  icon.style.width = '48px';
  icon.style.verticalAlign = 'top';
  icon.rowSpan = '2';
  var iconImg = NJPress.newNode('img');
  iconImg.src = 'http://0.gravatar.com/avatar/' + comment.email_md5 + '?s=48';
  iconImg.style.borderRadius = '4px';
  icon.appendChild(iconImg);

  row.insertCell(-1).innerHTML = comment.author;
  row.insertCell(-1).innerHTML = NJPress.escape(comment.url);
  row.insertCell(-1).innerHTML = NJPress.escape(comment.email);

  var post = row.insertCell(-1);
  var postLink = NJPress.newNode('a');
  postLink.href = '/?p=' + comment.post_id;
  postLink.innerHTML = comment.post_id;
  post.appendChild(postLink);

  var check = row.insertCell(-1);
  var checkbox = NJPress.newNode('input');
  checkbox.type = 'checkbox';
  checkbox.value = comment.id;
  check.appendChild(checkbox);

  row = commentsTable.insertRow(-1);
  row.insertCell(-1).innerHTML = comment.ipaddr;
  var date = row.insertCell(-1);
  date.colSpan = '4';
  date.innerHTML = comment.date;

  var content = commentsTable.insertRow(-1).insertCell(-1);
  content.colSpan = '6';
  content.innerHTML = comment.content;
  content.style.paddingLeft = '12px';

  var sep = commentsTable.insertRow(-1).insertCell(-1)
  sep.colSpan = '6';
  sep.style.height = '1px';
};

NJPress.loadPendingComments = function(commentsTable) {
  const URI = '/json/loadpendingcomments';
  NJPress.reqList(URI, {}, function(comment) {
    NJPress.typoComment(comment, commentsTable);
  });
};

NJPress.loadApprovedComments = function(commentsTable, start, counter) {
  const URI = '/json/loadapprovedcomments';
  NJPress.reqList(URI, { start: start }, function(comment) {
    NJPress.typoComment(comment, commentsTable);
    counter();
  });
};

NJPress.handleSelected = function(uri, selector) {
  var chk = $(selector);
  if (chk.length == 0) return;
  NJPress.request(uri, {
    ids: NJPress.valuesOf(chk),
  }, function(r) {
    window.location.reload();
  });
};
