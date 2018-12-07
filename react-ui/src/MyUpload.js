import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
export default class MyUpload extends Component {


	state = {
		selectedFile: null
	}

	fileSelectedHandler = event => {
		this.setState({selectedFile: event.target.files[0]})

	}

	uploadhand = () => {
		axios.post('http://duke.edu/Upload', this.state.selectedFile)
		.then(res => {
			console.log(res)
		})
		

	}


	render() {
		return (

			<div>
			<Paper className='paper'>
				<input type="file" onChange={this.fileSelectedHandler}/>

				
				<br /> <br />
				<Button color="primary" variant="contained" onClick={this.uploadhand}> Upload </Button>
			</Paper>
			</div>

		)
	}
}