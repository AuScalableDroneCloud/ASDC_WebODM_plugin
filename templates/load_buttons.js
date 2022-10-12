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
        return React.createElement(EditButton, {
            projectId: args.projectId
        });
	  }
);*/


