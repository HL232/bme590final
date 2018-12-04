import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import axios from 'axios'
export default class leftSide extends Component {
	render() {
		
		return (
			<MuiThemeProvider>
			<div>
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

