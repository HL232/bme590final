import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import { CloudDownload } from '@material-ui/icons'

export default class Picture extends Component {
  render() {

    return (

<GridListTile cellHeight={400} cellWidth={400} key={this.props.tile.img}>
<img src={"data:image/jpeg;" + this.props.tile.img} alt={this.props.tile.title} />
//{console.log(this.props.tile.img)}
<GridListTileBar
  title={this.props.tile.title}
  subtitle={<span>by: {this.props.tile.author}</span>}
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
