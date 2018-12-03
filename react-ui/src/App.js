import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import leftSideButtons from './leftSideButtons' ;
import Button from '@material-ui/core/Button';
import axios from 'axios'

import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import red from '@material-ui/core/colors/green';

const theme = createMuiTheme({
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

    document.body.style = 'background: gray;';
    return (
      <MuiThemeProvider theme={theme}>

      <div>
        
        <Button variant="contained" color="primary" style= {{margin: '5px'}} onClick={this.Upload}>
        Upload
        </Button>

        <br />
        
        <Button variant="contained" color="primary" style= {{margin: '5px'}} >
        Enhance
        </Button>

        <br />

        <Button variant="contained" color="primary" style= {{margin: '5px'}} >
        Download
        </Button>

        <br />

        <Button variant="contained" color="primary" style= {{margin: '5px'}}>
        Image Data
        </Button>

        <br />

        <Button variant="contained" color="primary" style= {{margin: '5px'}}>
           Library
        </Button>

        <leftSideButtons />
      
      </div>
      </MuiThemeProvider>
    );
  }



  Upload = () => {

    axios.get('http://myAPI/upload')


  }








}


export default App;
