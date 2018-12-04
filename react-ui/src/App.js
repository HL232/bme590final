import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import leftSide from './leftSide' ;
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import { withStyles, MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
import { ThreeDRotationIcon } from '@material-ui/icons/ThreeDRotation';
import tileData from './tileData';

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
        <Button variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}} onClick={this.Upload}>
         Upload
       </Button>

          <br />
        
        <Button variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}} >
         Enhance 
        </Button>

         <br />

        <Button variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}} >
         Download
       </Button>

         <br />

        <Button variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}}>
          Image Data
        </Button>

         <br />

        <Button variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}}>
             Library
        </Button>

        <leftSideButtons />
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

        {tileData.map(tile => (
          <GridListTile key={tile.img}>
          <img src={tile.img} alt={tile.tile} />
          <GridListTileBar
            title={tile.title}
            subtitle={<span>by: {tile.author}</span>}
            actionIcon={
              <IconButton>
                <ThreeDRotationIcon />
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



  Upload = (img) => {

    axios.post('http://MYAPI/Upload', {
    firstName: 'Fred',
    lastName: 'Flintstone'
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });

  }








}


export default App;
