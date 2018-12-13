import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import { CloudDownload } from '@material-ui/icons'
import { CameraEnhance } from '@material-ui/icons'
export default class DisEnh extends Component {


state = {
  myI: '',
  myS: 0 ,
}

startPass = () => {
  this.setState({myS: 1, myI: this.props.tile}, () => {
    this.passIt()
  });
}

passIt = () => {
  var win = this.state.myS ;
  var im = this.state.myI ;
  this.props.onSel(win, im) ;
  console.log(this.state.myI) ;
}

  render() {

    return (

<GridListTile key={this.props.tile.image_data}>
<img src={"data:image/jpeg;" + this.props.tile.image_data} alt={this.props.tile.user_id} />

<GridListTileBar
  title={this.props.tile.user_id}
  subtitle={<span>by: {this.props.tile.format}</span>}
  actionIcon={
    <IconButton onClick={this.startPass} color='primary'>
      <CameraEnhance fill='primary' />
    </IconButton>
  }
/>

</GridListTile>

);
  } ;
}
