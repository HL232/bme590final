import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import leftSideButtons from './leftSideButtons' ;
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import Button from '@material-ui/core/Button';
import axios from 'axios'

class App extends Component {
  render() {

    document.body.style = 'background: gray;';
    return (
      <MuiThemeProvider>

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
