 import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import image from './a.jpeg'
const TileData = [
  {
    img: image,
    title: 'Image',
    author: 'author',
  }]

export default class Library extends Component {

state = {
    myData: []
    
  }

getData = () => {
  console.log('getData')
  axios.get("http://adpl.suyash.io/api/sites").then(res => {
    console.log(res)
    this.setState({myData: res.data})
  })
}
  
containData = () => {
  if (this.state.myData.length === 0){
    {this.getData()}
  }
}



  render() {
    
    return(
      <div>
      {this.containData()}

      <Paper backgroundcolor= "primary">
      <GridList cellHeight={500} cols={3}>

        <GridListTile key="Subheader" cols={1} style={{height: 'auto'}}>
          <ListSubheader component="div"> Library </ListSubheader>
        </GridListTile>
        // All I have to do here is change this to myData.map and make sure
        // that the '.' parts match the data type
        // probably need a little tweaking to pull the thing out of the state though
        {this.state.myData.map(tile => (
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
        </div>
    )
  }
}


