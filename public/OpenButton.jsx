import React, { Component, Fragment } from "react";

import PropTypes from 'prop-types';
import { Button } from "react-bootstrap";

import "./OpenButton.scss";

export default class OpenButton extends Component {
  static propTypes = {
      task: PropTypes.object.isRequired,
  };

  tid = this.props.task ? this.props.task.id : '';
  pid = this.props.task ? this.props.task.project : '';
  //handleClick = () => window.open(`https://jupyter.asdc.cloud.edu.au/user-redirect/jupyter_oauth2/custom?project=${this.pid}&task=${this.tid}`, '_blank');
  handleClick = () => window.open(`https://jupyter.asdc.cloud.edu.au/user-redirect/asdc/import?project=${this.pid}&task=${this.tid}`, '_blank');

  render() {
    return (
      <Button
        bsStyle={"primary"}
        bsSize={"small"}
        onClick={this.handleClick}
      >
        <i className={"fab fa-python icon"} />
        Open in JupyterHub
      </Button>
    );
  }
}


