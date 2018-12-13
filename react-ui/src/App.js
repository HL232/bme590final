import React, { Component } from 'react';
//import logo from './logo.svg';
import './App.css';
import LeftSide from './LeftSide' ; 

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
    backgroundColor: 'primary'
  },
  gridList: {
    width: 500,
    height: 500,
  },
  gridListTileBar: {
    width:500,
  },
  icon: {
    color: 'rgba(0, 0, 0, 0.54)',
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

      <Typography align='center' component="h2" color="primary" variant="h1" gutterBottom>
        X-Ray Enhancer
      </Typography>

      <LeftSide />

      </div>
      </MuiThemeProvider>
    );
  }

}


export default App;
