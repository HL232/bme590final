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
		myimgArray: [],
	}

	fileSelectedHandler = event => {
		this.setState({selectedFile: event.target.files[0]})

	}

		onUpload = (files) => {
			const reader = new FileReader()
			const myF = files[0]
			reader.readAsDataURL(myF);
			reader.onloadend = () => {
				this.setState({currentImageString: reader.result});
			}


		}

 pusher = () => {

	 //console.log(this.state)
	 var myob = {}

	 var helpAr = []
	 if (this.state.myimgArray.length === 0) {

		 helpAr.push(this.state.currentImageString)
		 this.setState({myimgArray: helpAr})
	 }
	 else {
	    var myAr = this.state.myimgArray
	 		helpAr = myAr.push(this.state.currentImageString)
			this.setState({myimgArray: helpAr})
		}
	 //iStr = iStr.split(";").pop();
		 myob['image_data'] = helpAr
		 myob['email'] = 'myID@no.';
		 myob['filename'] = 'stevenisaTWAT'

	 axios.post('http://127.0.0.1:5000/api/process/upload_image', myob)
	 .then(res => {
	 	console.log(res)
	 })
	 .catch(function (error) {
 console.log(error);
});
 }


	render() {
		return (

			<div>
			<Paper className='paper'>


				<h2> Upload Images! </h2>
				<Button color = 'primary' variant = 'contained' style= {{margin: '5px'}}>
				<UploadField onFiles={this.onUpload}>


					Upload here

					</UploadField>
					</Button>
					<img src={this.state.currentImageString} />

					<Button style= {{margin: '5px'}} variant='contained' color='primary' onClick={this.pusher}>
					Confirm Upload?
					</Button>


			</Paper>
			</div>

		)
	}
}
