PluginsAPI.Dashboard.addTaskActionButton(
    ['asdc/build/OpenButton.js'],
    function(args, OpenButton) {
	      return React.createElement(OpenButton, {task: args.task});
    }
);

PluginsAPI.Dashboard.addNewTaskButton(
    ['asdc/build/EditButton.js'],
    function(args, EditButton) {
        return React.createElement(EditButton, {
            projectId: args.projectId
        });
	  }
);


