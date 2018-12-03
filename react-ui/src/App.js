import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import leftSideButtons from './leftSideButtons' ;
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import Button from '@material-ui/core/Button';
import axios from 'axios'

class App extends Component {
  render() {
    return (
      <MuiThemeProvider>
      <div>

        <Button variant="contained" color="primary" >
        Upload
        </Button>

        <Button variant="contained" color="primary" >
        Upload
        </Button>





        <leftSideButtons />
      
      </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
