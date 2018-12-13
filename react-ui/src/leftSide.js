import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import axios from 'axios'
import Library from './Library' ;
import MyUpload from './MyUpload'
import MyEnhance from './MyEnhance'
import MyDownload from './MyDownload'
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Typography, Grid, Paper} from '@material-ui/core';
import MainEnhance from './MainEnhance'

export default class LeftSide extends Component {
 

  state = {
    "winDisplay": 1
  };

  selector = () => {
    console.log(this.state.winDisplay)
    if (this.state.winDisplay === 1){
      return (<MyUpload />)
    }
    else if (this.state.winDisplay === 2){
      return <MainEnhance />
    }
    else if (this.state.winDisplay === 3){
      return <MyDownload />
    }
    else if (this.state.winDisplay === 4){
      return <Library />
    }
  } ;

  mySt = (myS) => {
    this.setState({"winDisplay": myS})

  }


	render() {

		return (
		<MuiThemeProvider>
			<div>

      <Grid container direction='row' spacing={10} spacing={40}>

      <Grid item xs={1.5} color='gray'>
        <Paper className='paper'>
				<Button onClick={() => this.mySt(1)} variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}}>
          Upload </Button> <br />
        <Button onClick={() => this.mySt(2)}variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}} >
          Enhance </Button> <br />

        <Button onClick={() => this.mySt(4)} variant="contained" fullWidth={true} size ='small' color="primary" style= {{margin: '5px'}}>
          Library </Button> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />
          </Paper>
        </Grid>

        <Grid item xs={1}>
        </Grid>

        <Grid item xs={9}>

      <div>
       {this.selector()}
      </div>

        </Grid>
      </Grid>


      </div>
    </MuiThemeProvider>
		)
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
