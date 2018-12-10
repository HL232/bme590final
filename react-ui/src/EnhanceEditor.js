import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'

export default class EnhanceEditor extends Component {



  render() {
    return(
      <div>

      Before:
      <br />
      <img src={"data:image/jpeg;" + this.props.tile.image_data} />
      <br />

      After:
      


      </div>
    )
  }
}
