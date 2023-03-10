PluginsAPI.Dashboard.addTaskActionButton(
    ['asdc/build/OpenButton.js'],
    function(args, OpenButton) {
        //console.log("PIPELINES: {{pipelines}}";
        //return React.createElement(OpenButton, {task: args.task, pipelines: '{{pipelines}}'});
        const doc = new DOMParser().parseFromString('{{pipelines}}', "text/html");
        return React.createElement(OpenButton, {task: args.task, pipelines: doc.documentElement.textContent});
    }
);

function open_url(url) {
  let projects = new URLSearchParams(window.location.search).get('project_task_open');
  url = url.replaceAll("PROJECTS", projects || '')
  window.open(url);
}

function file_browser(host, user) {
  let projects = new URLSearchParams(window.location.search).get('project_task_open');
  if (!projects || projects.length < 1) {
    alert('Please select project(s) to browse on right...')
    return;
  }
  let next = encodeURIComponent('/user-redirect/lab/tree/projects');
  spawnurl = `https://jupyter.${host}/hub/spawn?profile=base&projects=${projects}&next=${next}`;
  window.open(spawnurl)
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

