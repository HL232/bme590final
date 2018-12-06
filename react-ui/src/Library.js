 import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';

import image from './a.jpeg'
const TileData = [
  {
    img: image,
    title: 'Image',
    author: 'author',
  }]

export default class Library extends Component {

state = {
    myData: null
  }

getData = () => {

}

  render() {

    return(
      <Paper backgroundcolor= "primary">
      <GridList cellHeight={500} cols={3}>

        <GridListTile key="Subheader" cols={1} style={{height: 'auto'}}>
          <ListSubheader component="div"> Library </ListSubheader>
        </GridListTile>

        {TileData.map(tile => (
          <GridListTile key={tile.img}>
          <img src={tile.img} alt={tile.tile} />
          <GridListTileBar
            title={tile.title}
            subtitle={<span>by: {tile.author}</span>}
            actionIcon={
              <IconButton>
                
              </IconButton>
            }
          />

          </GridListTile>
          ))}
       
        </GridList>
        </Paper>
    )
  }
}


