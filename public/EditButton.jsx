//See: cloudimport/public/components/ImportView.jsx
import React, { Component, Fragment } from "react";

import PropTypes from 'prop-types';
import { Button } from "react-bootstrap";
import $ from 'jquery';

import "./Button.scss";

export default class EditButton extends Component {
  static propTypes = {
      //task: PropTypes.object.isRequired,
    	projectId: PropTypes.number.isRequired,
  		//apiURL: PropTypes.string.isRequired,
		  //onNewTaskAdded: PropTypes.func.isRequired,
  };

  pid = this.props.projectId;
  //tid = this.props.task ? this.props.task.id : '';
  //pid = this.props.projectId;
  //task ? this.props.task.project : '';
  handleClick = () => window.open(`https://jupyter.${location.host}/spawn?profile=exp-${this.pid}`, '_blank');
  //handleClickNotebook = () => window.open(`https://jupyter.${location.host}/user-redirect/asdc/import?project=${this.pid}&task=${this.tid}`, '_blank');
  //handleClickFiles = () => window.open(`https://jupyter.${location.host}/hub/spawn?profile=exp-${this.pid}`, '_blank');

  render() {
    return (
      <Button
        bsStyle={"default"}
        bsSize={"small"}
        onClick={this.handleClick}
      >
        <i className={"fas fa-folder-open icon"} />
        Edit in JupyterHub
      </Button>
    );
  }
}

/*
	render() {
		const {
			currentPlatform,
			error,
			selectedFolder,
			platforms,
		} = this.state;
		return (
			<Fragment>
			{error ?
				<ErrorDialog errorMessage={error} />
			: ""}
				<PlatformSelectButton
					platforms={platforms}
					onSelect={this.onSelectPlatform}
				/>

			<DropdownButton
				id={"platformsDropdown"}
				bsStyle={"default"}
				bsSize={"small"}
				className={"platform-btn"}
				title={title}
			>
				{menuItems}
			</DropdownButton>


				{selectedFolder === null ?
					<Fragment>
						<PlatformDialog
							show={selectedFolder === null}
							platform={currentPlatform}
							apiURL={this.props.apiURL}
							onHide={this.onHideDialog}
							onSubmit={this.onSelectFolder}
						/>
						<LibraryDialog
						  show={selectedFolder === null}
						  platform={currentPlatform}
							apiURL={this.props.apiURL}
						  onHide={this.onHideDialog}
						  onSubmit={this.onSelectFolder}
						/>
					</Fragment>
				: 
					<ConfigureNewTaskDialog
					  show={selectedFolder !== null}
						folder={selectedFolder}
					  platform={currentPlatform}
					  onHide={this.onHideDialog}
					  onSaveTask={this.onSaveTask}
					/>
				}
			</Fragment>
		);
	}
}



///////////// PlatformSelectButton.jsx
import React, { PureComponent, Fragment } from "react";

import { DropdownButton, MenuItem } from "react-bootstrap";

import "./PlatformSelectButton.scss";

export default class PlatformSelectButton extends PureComponent {
	static defaultProps = {
		platforms: [],
		onSelect: () => {}
	};

	handleClick = platform => () => this.props.onSelect(platform);

	render() {
		const {
			platforms,
			onSelect,
		} = this.props;
		
		const menuItems = platforms
			.map(platform => (
				<MenuItem
					key={platform.name}
					tag={"a"}
					onClick={this.handleClick(platform)}
				>
					<Fragment>
						{"  "}
						{platform.name}
					</Fragment>
				</MenuItem>
			));

		const title = (
			<Fragment>
				<i className={"fa fa-cloud-download-alt fa-cloud-import"} />
				Cloud Import
			</Fragment>
		
		);

		return (
			<DropdownButton
				id={"platformsDropdown"}
				bsStyle={"default"}
				bsSize={"small"}
				className={"platform-btn"}
				title={title}
			>
				{menuItems}
			</DropdownButton>
		);
	}
}

*/
