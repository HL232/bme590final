 import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import image from './a.jpeg'
import { CloudDownload } from '@material-ui/icons'
import Picture from './Picture'
const TileData = [
  {
    img: image,
    title: 'Image',
    author: 'author',
  },
  {
    img: image,
    title: 'Image',
    author: 'author',
  }

]

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

down = () => {

}


  render() {

    return(
      <div>
      {this.containData()}

      <Paper className='paper'>
      <GridList background='white' cellHeight={500} cols={3}>

        <GridListTile key="Subheader" cols={1} style={{height: 'auto'}}>
          <ListSubheader component="div"> Library </ListSubheader>
        </GridListTile>
        // All I have to do here is change this to myData.map and make sure
        // that the '.' parts match the data type
        // probably need a little tweaking to pull the thing out of the state though
        {TileData.map(tile => (
          <Picture tile={tile}/>

          ))}

        </GridList>
        </Paper>
        </div>
    )
  }
}
