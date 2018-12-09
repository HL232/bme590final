import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import { CloudDownload } from '@material-ui/icons'

export default class Picture extends Component {
  render() {

    return (

<GridListTile key={this.props.tile.image_data}>
<img src={"data:image/jpeg;" + this.props.tile.image_data} alt={this.props.tile.user_id} />
//{console.log(this.props.tile.img)}
<GridListTileBar
  title={this.props.tile.user_id}
  subtitle={<span>by: {this.props.tile.format}</span>}
  actionIcon={
    <IconButton color='primary'>
      <CloudDownload />
    </IconButton>
  }
/>

</GridListTile>

);
  } ;
}
