import React, { Component } from 'react';
//import logo from './logo.svg';
import './App.css';
import LeftSide from './LeftSide' ;
import Library from './Library' ;
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import { withStyles, MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';

//import {TileData} from './tileData';

const theme = createMuiTheme({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: 'white'
  },
  gridList: {
    width: 800,
    height: 500,
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

        <Grid xs={5}>
        

       <Library />


        </Grid>
      </Grid>

      </div>
      </MuiThemeProvider>
    );
  }

}


export default App;
