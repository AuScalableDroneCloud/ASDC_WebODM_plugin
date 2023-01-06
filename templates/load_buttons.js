PluginsAPI.Dashboard.addTaskActionButton(
    ['asdc/build/OpenButton.js'],
    function(args, OpenButton) {
	      return React.createElement(OpenButton, {task: args.task});
    }
);

/*
 * Disabled now in favour of a side menu button to mount the selected projects
 * PluginsAPI.Dashboard.addNewTaskButton(
    ['asdc/build/EditButton.js'],
    function(args, EditButton) {
	      //if (task.available_assets !== null && task.available_assets.length > 0){
        return React.createElement(EditButton, {
            projectId: args.projectId
        });
	  }
);*/

function file_browser(host, user) {
  let projects = new URLSearchParams(window.location.search).get('project_task_open');
  if (!projects || projects.length < 1) {
    alert('Please select project(s) to browse on right...')
    return;
  }
  spawnurl = `https://jupyter.${host}/hub/spawn?profile=base&projects=${projects}`;
  window.open(spawnurl)
  /*
  //SEE: https://jupyterhub.readthedocs.io/en/0.8.1/_static/rest-api/index.html
  killurl = `https://jupyter.${host}/hub/api/users/${user}/server`;
  //NOTE: @ in username may need encoding
  //https://jupyter.asdc.cloud.edu.au/hub/api/users/USERNAME/server
  //https://jupyter.asdc.cloud.edu.au/hub/api/users/USERNAME/servers/base
  console.log("URL: " + spawnurl);
  console.log("KILLURL: " + killurl);
  //First shutdown any existing server
  $.ajax({
    url: killurl,
    type: 'DELETE',
    success: function(result) {
      console.log("DELETED!");
      window.open(spawnurl)
      //$(".result").html(result);
      //alert( "Load was performed." );
      //location.reload();
    }
  });*/
}

function pipeline_project(url) {
  pipeline_run(url, false, true);
}

function pipeline_task(url) {
  pipeline_run(url, true, true);
}

function pipeline_run(url, need_task, need_project) {
  let projects = new URLSearchParams(window.location.search).get('project_task_open'); //.replaceAll(',','-');
  let tasks = new URLSearchParams(window.location.search).get('project_task_expanded'); //.replaceAll(',','-');
  if (need_task && (!tasks || tasks.length < 36)) {
    alert('Please first select input task(s) for this pipeline...')
    return;
  }
  if (need_project && (!projects || projects.length < 1)) {
    alert('Please first select input project(s) for this pipeline...')
    return;
  }

  //Replace the placeholders with data
  url = url.replaceAll("PROJECTS", projects || '')
  url = url.replaceAll("TASKS", tasks || '')

  console.log("URL: " + url);
  window.open(url)
}

function save_open_projects() {
  let projects = new URLSearchParams(window.location.search).get('project_task_open');
  //$.get("/api/plugins/asdc/saveprojects?projects=" + projects)
  $.get( "/api/plugins/asdc/saveprojects?projects=" + projects, function(data) {
    //$(".result").html( data );
    //alert( "Load was performed." );
    location.reload();
  });
}

function clear_open_projects() {
  $.get( "/api/plugins/asdc/clearprojects", function(data) {
    //$(".result").html(data);
    //alert( "Load was performed." );
    location.reload();
  });
}
