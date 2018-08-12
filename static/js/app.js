function userinfo(start,end){
  $.ajax({  
    type: "GET",
    url: USERDATA,
    data: {'start':start,'end':end},
    dataType: "json",
    success: function(res) {
      data = "<ul class='list-group'>"
      for (var i = 0; i < res.data.length; ++i) {
          data = data + '<div class="panel panel-default"><div class="panel-heading" style="background-color: #2b2b2b; color: #8c8c8c">' + '<img style="width: 50px;height: 50px" src="' + res.data[i].avatar + '">' +' &nbsp;&nbsp;&nbsp;&nbsp; ' + res.data[i].username +'</div>' +
              '<div class="panel-body">' +
              '<table class="table table-striped"><tr><th>REPOSITORY</th><th>TITLE</th><th>DESCRIPTION</th></tr>'
          for (var j = 0; j < res.data[i].public_repos.length; ++j){
            data = data + '<tr><td><a href="repo?repo='+ res.data[i].public_repos[j].full_name + '">' + res.data[i].public_repos[j].full_name + '</a></td><td>'+ res.data[i].public_repos[j].name + '</td><td>'+ res.data[i].public_repos[j].description + '</td></tr>'
          }
          data = data+'</table></div></div></ul>'
      }
      data = data + '<a style= "padding: 8px 16px;display: inline-block; text-decoration: none;" ' +
          'href=' + '"' + res.prev +'"' + ' class="prev">&laquo; Previous</a>'
      data = data + '<a style= "padding: 8px 16px;display: inline-block;text-decoration: none;" ' +
          'href=' + '"' + res.next +'"' + ' class="next">Next &raquo;</a>'
      $('#github_user').html(data);
    },
    error: function(res){
      console.log(res);
    }
  });
}
