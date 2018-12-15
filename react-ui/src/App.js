import React, { Component } from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
//import logo from './logo.svg';

import './App.css';
import LeftSide from './LeftSide' ;

import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import { withStyles, MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';

//import {TileData} from './tileData';

const theme = createMuiTheme({
  appBar: {
    position: 'relative',
  },
  root: {
    display: 'flex',
    flexGrow: 1,
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: 'primary'
  },
  gridList: {
    width: 800,
    height: 600,
  },
  gridListTileBar: {
    width:800,
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

    document.body.style = 'background: #f2f2f2;';
    return (

      <MuiThemeProvider theme={theme}>
      <div>
      <AppBar position="static" color="default">
        <Toolbar>
          <Typography variant="h6" color="primary">
            X-Ray Enhancer
          </Typography>
        </Toolbar>
      </AppBar>

      <LeftSide />

      </div>
      </MuiThemeProvider>
    );
  }

}


export default App;
