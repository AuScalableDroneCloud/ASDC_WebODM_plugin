PluginsAPI.Dashboard.addTaskActionButton(['asdc/build/OpenButton.js'],function(args, OpenButton){
	var task = args.task;

	//if (task.available_assets !== null && task.available_assets.length > 0){
	//	return React.createElement(ShareButton, {task: task, token: "${token}"});
	//}
	return React.createElement(OpenButton, {task: args.task, projectId: args.projectId});
}
);

