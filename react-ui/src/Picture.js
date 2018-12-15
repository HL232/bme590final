import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import { CloudDownload, PlaylistAdd } from '@material-ui/icons'

export default class Picture extends Component {

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
    
  }


  render() {

    return (

<GridListTile key={this.props.tile.image_data}>
<img src={"data:image/jpeg;base64," + this.props.tile.image_data} alt={this.props.tile.user_id}/>

<GridListTileBar
  title={this.props.tile.height + 'x' + this.props.tile.width}
  subtitle={<span>Type: {this.props.tile.format}</span>}
  actionIcon={
    <IconButton color='primary'>
      <PlaylistAdd onClick={this.startPass} />

    </IconButton>

  }
/>

</GridListTile>

);
  } ;
}
