import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';

export default class leftSideButtons extends Component {
	render() {
		
		return (
			<MuiThemeProvider>
			<div>
				<Button variant="contained" color="primary" >
       			Primary
      			</Button>
      		</div>
      		</MuiThemeProvider>
		)
	}
}

//export default leftSideButtons;