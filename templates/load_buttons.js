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

function open_url(url) {
  window.open(url);
}

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

function clear_old_storage() {
  console.log('Storage quota exceeded, removing old tus entries')
  //30 days ago and older
  var expiry = new Date().getTime() - (30 * 24 * 60 * 60 * 1000);
  for (var i = 0; i < localStorage.length; i++) {
    let key = localStorage.key(i);
    let val = localStorage.getItem(key);
    if (new Date(val.creationTime) < expiry) {
      console.log("Removing " + key);
      localStorage.removeItem(key);
    }
  }
}

//Clear expired localStorage entries from TUS if full
try {
  console.log('Checking localStorage...');
  let hasStorage = 'localStorage' in window

  // Attempt to store and read entries from the local storage
  const key = 'storageCheck'
  localStorage.setItem(key, 'asdc'.repeat(1000));
  localStorage.removeItem(key)
  console.log('done.');
} catch (e) {
  // If we try to access localStorage inside a sandboxed iframe, a SecurityError
  // is thrown. When in private mode on iOS Safari, a QuotaExceededError is
  // thrown (see #49)
  if (e.code === e.QUOTA_EXCEEDED_ERR) {
    clear_old_storage();
  } else {
    throw e
  }
}

//tus::tus-uppy-p1100077/jpg-1e-image/jpeg-4985344-1600850799723-https://tusd.asdc.cloud.edu.au/files/::126748795151:
//"{"size":4985344,
//  "metadata":{"relativePath":null,"name":"P1100077.JPG","type":"image/jpeg","filetype":"image/jpeg","filename":"P1100077.JPG"},
//  "creationTime":"Wed Jul 27 2022 17:29:29 GMT+1000 (Australian Eastern Standard Time)",
//  "uploadUrl":"https://tusd.asdc.cloud.edu.au/files/857076892a1159d8c2373107c85d2885"
//  }"

