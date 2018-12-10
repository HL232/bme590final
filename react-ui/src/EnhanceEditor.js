import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'

export default class EnhanceEditor extends Component {

  state = {
    beforeIM: '',
    afterIM: '',
    enhtype: 1,

  }


beforeSelector = () => {
  if (this.state.beforeIM.length === 0) {
    this.setState({beforeIM: this.props.tile})
    this.setState({afterIM: this.props.tile})
  }
  else {

  }
}

afterSelector = () => {
  var enhtype = this.state.enhtype
  if (enhtype === 0){

  }
  else if (enhtype === 1) {
    axios.post('http://127.0.0.1:5000/api/process/hist_eq', {
      user_id:'myID'
    })
 	 .then(res => {
 	 	this.setState({afterIM: res.data})
 	 })
 	 .catch(function (error) {
  console.log(error);
 });
  }
  else if (enhtype === 2) {

  }
  else if (enhtype === 3) {

  }
  else if (enhtype === 4) {

  }
}

  render() {
    return(
      <div>
      {this.beforeSelector()}

      <Button color='primary' variant='contained' onClick={this.afterSelector}>
      Histogram EQ
      </Button>
      Before:
      <br />
      <img src={this.state.beforeIM.image_data} />
      <br />
      ||
      VV
      After:
      <img src={this.state.afterIM.image_data} />


      </div>
    )
  }
}
