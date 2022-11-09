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

function pipeline_project(user, host, profile) {
  pipeline_run(user, host, profile, false, true);
}

function pipeline_task(user, host, profile) {
  pipeline_run(user, host, profile, true, true);
}

function pipeline_run(user, host, profile, need_task, need_project) {
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
  window.open('https://jupyter.' + host + '/hub/spawn?profile=' + profile + '&projects=' + projects + '&tasks=' + tasks);
  //DISABLE NAMED SERVERS FOR NOW - these do not work with the auth callback
  //Need username to spawn a named server
  //window.open('https://jupyter.' + host + '/hub/spawn/' + user + '/' + profile + '?profile=' + profile + '&projects=' + projects + '&tasks=' + tasks);
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
