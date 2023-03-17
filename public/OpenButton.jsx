import React, { Component, Fragment } from "react";
import { DropdownButton, MenuItem } from "react-bootstrap";

import PropTypes from 'prop-types';
import { Button } from "react-bootstrap";
import $ from 'jquery';

import "./Button.scss";

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
  nextbase = `/user-redirect/asdc/import?project=${this.pid}&task=${this.tid}&name=${this.tname}`;
  //next = encodeURIComponent(nextbase);
  //url = `https://jupyter.${location.host}/hub/spawn?profile=base&projects=${this.pid}&tasks=${this.tid}&name=${this.tname}&next=${this.next}`;
  //handleClick = () => window.open(`${this.url}`, '_blank');
  base = `https://jupyter.${location.host}/hub/spawn?profile=base&projects=${this.pid}&tasks=${this.tid}&name=${this.tname}`

  //handleClickNotebook = () => window.open(`https://jupyter.${location.host}/user-redirect/asdc/import?profile=${this.profile}&project=${this.pid}&task=${this.tid}&name=${this.tname}`, '_blank');

  //next = encodeURIComponent(`/user-redirect/asdc/browse?project=${this.pid}&task=${this.tid}`);
  //handleClickFiles = () => window.open(`https://jupyter.${location.host}/hub/spawn?projects=${this.pid}&tasks=${this.tid}&next=${this.next}`, '_blank');

  //Should probably load this data from ExportAssetPanel rather than duplicating, also check for available assets...
  assets = [{"name" : "Orthophoto", "icon" : "fa fa-image",
             "url" : `${this.base}&next=${encodeURIComponent(this.nextbase + '&asset=orthophoto.tif')}`,
              "disabled" : this.props.task.available_assets.indexOf('orthophoto.tif') == -1},
            {"name" : "Surface Model", "icon" : "fa fa-chart-area",
              "url" : `${this.base}&next=${encodeURIComponent(this.nextbase + '&asset=dsm.tif')}`,
              "disabled" : this.props.task.available_assets.indexOf('dsm.tif') == -1},
            {"name" : "Point Cloud", "icon" : "fa fa-cube",
              "url" : `${this.base}&next=${encodeURIComponent(this.nextbase + '&asset=georeferenced_model.laz')}`,
              "disabled" : this.props.task.available_assets.indexOf('georeferenced_model.laz') == -1},
            {"name" : "Textured Model", "icon" : "fab fa-connectdevelop",
              "url" : `${this.base}&next=${encodeURIComponent(this.nextbase + '&asset=textured_model.zip')}`,
              "disabled" : this.props.task.available_assets.indexOf('textured_model.zip') == -1},
            {"name" : "Textured Model (gLTF)", "icon" : "fab fa-connectdevelop",
              "url" : `${this.base}&next=${encodeURIComponent(this.nextbase + '&asset=textured_model.glb')}`,
              "disabled" : this.props.task.available_assets.indexOf('textured_model.glb') == -1},
           ]

  render() {
    const url = this.url;

		const nMenuItems = this.assets
			.map(asset => (
				<MenuItem
					key={asset.name}
					tag={"a"}
          href={asset.url}
          target='_blank'
          to=''
          disabled={asset.disabled}
				>
					<Fragment>
           <i className={asset.icon}></i>
						{"  "}
						{asset.name}
					</Fragment>
				</MenuItem>
			));

		const ntitle = (
			<Fragment>
				<i className={"fab fa-python"} />
				&nbsp; {"  "} Open Notebook
			</Fragment>

		);

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
			<Fragment>
        <DropdownButton
          id={"pipelinesDropdown"}
          bsStyle={"default"}
          bsSize={"small"}
          className={"pipeline-btn"}
          title={title}
        >
          {menuItems}
        </DropdownButton>
        <DropdownButton
          id={"notebookDropdown"}
          bsStyle={"default"}
          bsSize={"small"}
          className={"notebook-btn"}
          title={ntitle}
        >
          {nMenuItems}
        </DropdownButton>
			</Fragment>
		);
	}
} 

