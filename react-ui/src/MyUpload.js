import React, { Component } from 'react';
import ReactDOM from 'react-dom'
import Button from '@material-ui/core/Button';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import { UploadField } from '@navjobs/upload'


export default class MyUpload extends Component {

	constructor() {
			super();
			this.state= {
					currentImageString: '',
			}
	}

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
		onUpload = (files) => {
			const reader = new FileReader()
			const myF = files[0]
			reader.readAsDataURL(myF);
			reader.onloadend = () => {
				console.log(reader.result);
				this.setState({currentImageString: reader.result});
			}
			axios.post('http://duke.edu/Upload', this.state.currentImageString)
			.then(res => {
				console.log(res)
			})

		}




	render() {
		return (

			<div>
			<Paper className='paper'>


				<h2> Upload Images! </h2>
				<Button color = 'primary' variant = 'contained'>
				<UploadField onFiles={this.onUpload}>


					Upload here

					</UploadField>
					</Button>
					<img src={this.state.currentImageString} />


			</Paper>
			</div>

		)
	}
}
