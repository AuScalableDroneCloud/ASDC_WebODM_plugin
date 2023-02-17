import React, { Component, Fragment } from "react";

import PropTypes from 'prop-types';
import { Button } from "react-bootstrap";
import $ from 'jquery';

import "./Button.scss";

export default class OpenButton extends Component {
  static propTypes = {
      task: PropTypes.object.isRequired,
  };

  tid = this.props.task ? this.props.task.id : '';
  pid = this.props.task ? this.props.task.project : '';
  tname = this.props.task ? this.props.task.name : '';
  next = encodeURIComponent(`/user-redirect/asdc/browse?project=${this.pid}&task=${this.tid}`);
  handleClickNotebook = () => window.open(`https://jupyter.${location.host}/user-redirect/asdc/import?project=${this.pid}&task=${this.tid}&name=${this.tname}`, '_blank');
  handleClickFiles = () => window.open(`https://jupyter.${location.host}/hub/spawn?projects=${this.pid}&tasks=${this.tid}&next=${this.next}`, '_blank');

  render() {
    return (
		<>
      <Button
        bsStyle={"primary"}
        bsSize={"small"}
        onClick={this.handleClickFiles}
      >
        <i className={"fas fa-folder-open icon"} />
        Edit in JupyterHub
      </Button>

      <Button
        bsStyle={"primary"}
        bsSize={"small"}
        onClick={this.handleClickNotebook}
      >
        <i className={"fab fa-python icon"} />
        Open Notebook
      </Button>
		</>
    );
  }
}


