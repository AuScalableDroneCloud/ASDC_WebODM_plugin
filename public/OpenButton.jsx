import React, { Component, Fragment } from "react";
import { DropdownButton, MenuItem } from "react-bootstrap";

import PropTypes from 'prop-types';
import { Button } from "react-bootstrap";
import $ from 'jquery';

import "./Button.scss";

const STATE_NONE = 0;
const STATE_QUEUED = 10;
const STATE_RUNNING = 20;
const STATE_ERROR = 30;
const STATE_COMPLETED = 40;
const STATE_CANCELLED = 50;

export default class OpenButton extends Component {
  static propTypes = {
      task: PropTypes.object.isRequired,
      pipelines: PropTypes.object.isRequired,
  };

  tid = this.props.task ? this.props.task.id : '';
  pid = this.props.task ? this.props.task.project : '';
  tname = this.props.task && this.props.task.name ? this.props.task.name : 'unnamed';
  pipelines = JSON.parse(this.props.pipelines.replaceAll("PROJECTS", this.props.task.project).replaceAll("TASKS", this.props.task.id));
  //Always use the base profile for these links for now
  //handleClick = () => window.open(`https://jupyter.${location.host}/user-redirect/asdc/import?profile=base&project=${this.pid}&task=${this.tid}&name=${this.tname}`, '_blank');
  next = encodeURIComponent(`/user-redirect/asdc/import?project=${this.pid}&task=${this.tid}&name=${this.tname}`);
  url = `https://jupyter.${location.host}/hub/spawn?profile=base&projects=${this.pid}&tasks=${this.tid}&name=${this.tname}&next=${this.next}`;
  handleClick = () => window.open(`${this.url}`, '_blank');

  //handleClickNotebook = () => window.open(`https://jupyter.${location.host}/user-redirect/asdc/import?profile=${this.profile}&project=${this.pid}&task=${this.tid}&name=${this.tname}`, '_blank');

  //next = encodeURIComponent(`/user-redirect/asdc/browse?project=${this.pid}&task=${this.tid}`);
  //handleClickFiles = () => window.open(`https://jupyter.${location.host}/hub/spawn?projects=${this.pid}&tasks=${this.tid}&next=${this.next}`, '_blank');

  render() {
    const url = this.url;

		const menuItems = this.pipelines
			.map(pipeline => (
				<MenuItem
					key={pipeline.name}
					tag={"a"}
          href={pipeline.url}
          target='_blank'
          to=''
				>
					<Fragment>
           <i className={pipeline.icon}></i>
						{"  "}
						{pipeline.name}
					</Fragment>
				</MenuItem>
			));

		const title = (
			<Fragment>
				<i className={"fas fa-stream"} />
				&nbsp; {"  "} Run Pipeline
			</Fragment>

		);

    //    <p>Task Status: {this.props.task.status}</p>
		return (
      <div className="open-buttons">
        <DropdownButton
          id={"pipelinesDropdown"}
          bsStyle={"default"}
          bsSize={"small"}
          className={"pipeline-btn"}
          title={title}
          disabled={!(this.props.task.status == STATE_NONE || this.props.task.status == STATE_COMPLETED)}
        >
          {menuItems}
        </DropdownButton>
        <a href={url} target='_blank'>
          <button className="btn btn-default btn-sm"
            disabled={!(this.props.task.status == STATE_NONE || this.props.task.status == STATE_COMPLETED)}
          >
            <i className={"fab fa-python icon"}></i>&nbsp;
            Open Notebook
          </button>
        </a>
      </div>
		);
	}
} 

