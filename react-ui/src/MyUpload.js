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
		zipContainer: '',
	}


	fileSelectedHandler = event => {
		this.setState({selectedFile: event.target.files[0]})
	}


		onUpload = (files) => {
			const reader = new FileReader()
			const myF = files[0]
			reader.readAsDataURL(myF);
			reader.onloadend = () => {
				this.setState({currentImageString: reader.result}, () => {
					this.addtoArray()
				});
			}
		}


 addtoArray = () => {
	 //console.log(this.state)


	 var helpAr = []
	 if (this.state.myimgArray === undefined) {

		 helpAr.push(this.state.currentImageString)
		 this.setState({myimgArray: helpAr})
	 }
	 else {
		 console.log('Hit')
	    var myAr = this.state.myimgArray
			console.log(myAr)
	 		myAr.push(this.state.currentImageString)
			this.setState({myimgArray: myAr})
		}
	 //iStr = iStr.split(";").pop();
 }


 pusher = () => {
	 var myob = {} ;
	 myob['image_data'] = this.state.myimgArray ;
	 myob['email'] = 'myID@no.';
	 myob['filename'] = 'stevenisaTWAT'
	 console.log(this.state.myimgArray)
 axios.post('http://127.0.0.1:5000/api/process/upload_image', myob)
 .then(res => {
	console.log(res)
 })
 .catch(function (error) {
console.log(error);
});
 }

 onUploadzip = (files) => {
	 const reader = new FileReader()
	 const myF = files[0]
	 reader.readAsDataURL(myF);
	 reader.onloadend = () => {
		 this.setState({zipContainer: reader.result}, () => {
			 this.pusherZIP()
		 });
	 }
 }

 pusherZIP = () => {
	 var myob = {} ;
	 myob['image_data'] = this.state.zipContainer;
	 myob['email'] = 'myID@no.';
	 myob['filename'] = 'stevenisaTWAT.zip'
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


				<h2> Upload Images! (zip is uploaded automatically) </h2>
				<Button color = 'primary' variant = 'contained' style= {{margin: '5px'}}>
				<UploadField onFiles={this.onUpload}>
					Upload JPG
					</UploadField>
					</Button>

					<Button color = 'primary' variant = 'contained' style= {{margin: '5px'}}>
					<UploadField onFiles={this.onUploadzip}>
						Upload ZIP
						</UploadField>
						</Button>

					<img src={this.state.currentImageString} />

					<Button style= {{margin: '5px'}} variant='contained' color='primary' onClick={this.pusher}>
					Confirm JPG Upload?
					</Button>



			</Paper>
			</div>

		)
	}
}
