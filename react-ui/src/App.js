import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import LeftSide from './LeftSide' ;
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import { withStyles, MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
//import { ThreeDRotationIcon } from '@material-ui/icons/ThreeDRotation';
//import {TileData} from './tileData';
import image from './a.jpeg'
const TileData = [
  {
    img: image,
    title: 'Image',
    author: 'author',
  },


  ];
const theme = createMuiTheme({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    
  },
  gridList: {
    width: 500,
    height: 450,
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)',
  },
  palette: {
    primary: {
      main: '#43a047'
    },
    secondary: {
      main: '#00c853',
    },
    overrides: {
      Paper: {
        color: 'gray',
        background: 'gray'
      },
      MuiButton: {
        root: {
          color: 'green'
        },
      },
    },
  },
});


class App extends Component {
  render() {

    document.body.style = 'background: lightgray;';
    return (
      <MuiThemeProvider theme={theme}>

      <div>
        
      <Typography align='center' component="h2" color="green[700]" variant="h1" gutterBottom>
        X-Ray Enhancer
      </Typography>

    <Grid container direction='row' spacing={10} spacing={40}>
      
      <Grid item xs={1.5} color='gray'>
        

        <LeftSide />
        </Grid>

        <Grid xs={1}>
        </Grid>

        <Grid xs={3}>
        <Paper>
        Place Images Here <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />
        </Paper>


        <GridList cellHeight={180} cols={3}>

        <GridListTile key="Subheader" cols={2} style={{height: 'auto'}}>
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


        </Grid>
      </Grid>

      </div>
      </MuiThemeProvider>
    );
  }

}


export default App;
