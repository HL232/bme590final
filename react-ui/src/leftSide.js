import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';

export default class leftSide extends Component {
	render() {
		
		return (
			<MuiThemeProvider>
			<div>
			hello
				<Button variant="contained" color="primary" >
       			Primary
      			</Button>
      		</div>
      		</MuiThemeProvider>
		)
	}
}

