PluginsAPI.Dashboard.addNewTaskButton(["asdc/build/EditButton.js"],
	function(args, EditButton) {
        return React.createElement(EditButton, {
                //onNewTaskAdded: args.onNewTaskAdded,
                projectId: args.projectId,
                apiURL: "{{ api_url }}",
        });
	}
);

PluginsAPI.Dashboard.addTaskActionButton(['asdc/build/OpenButton.js'],function(args, OpenButton){
	var task = args.task;

	//if (task.available_assets !== null && task.available_assets.length > 0){
	//	return React.createElement(ShareButton, {task: task, token: "${token}"});
	//}
	return React.createElement(OpenButton, {task: args.task, projectId: args.projectId});
}
);

/*
PluginsAPI.Dashboard.addTaskActionButton(
    ["cloudimport/build/TaskView.js", "cloudimport/build/TaskView.css"],
	function(args, TaskView) {
		var reactElement;
		$.ajax({
			url: "{{ api_url }}/projects/" + args.task.project + "/tasks/" + args.task.id + "/checkforurl",
			dataType: 'json',
			async: false,
			success: function(data) {
				if (data.folder_url) {
					reactElement = React.createElement(TaskView, {
						folderUrl: data.folder_url,
					});
				}
			}
		});
		return reactElement;
	}
);
*/
