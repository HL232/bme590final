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
		myFnArray: [],
		zipContainer: '',
		curreFna: ''
	}


	fileSelectedHandler = event => {
		this.setState({selectedFile: event.target.files[0]})
	}


		onUpload = (files) => {
			const reader = new FileReader()
			//console.log(files[0].name)
			const myF = files[0]
			reader.readAsDataURL(myF);
			reader.onloadend = () => {
				this.setState({currentImageString: reader.result, curreFna: myF.name}, () => {
					this.addtoArray()
				});
			}
		}


 addtoArray = () => {
	 //console.log(this.state)


	 var helpAr = []
	 var strAr = []
	 if (this.state.myimgArray === undefined) {
		 var sst = this.state.curreFna
		 //console.log(sst)
		 strAr.push(sst)

		 //console.log(strAr)
		 this.setState({myFnArray: strAr}, console.log(this.state.myFnArray))


		 helpAr.push(this.state.currentImageString)
		 this.setState({myimgArray: helpAr}, console.log(this.state.myimgArray))
	 }
	 else {
		 console.log('Hit')
	    var myAr = this.state.myimgArray
	 		myAr.push(this.state.currentImageString)
			this.setState({myimgArray: myAr})

			var sst = this.state.curreFna
			var my2Ar = this.state.myFnArray
			my2Ar.push(sst)
			this.setState({myFnArray: my2Ar}, console.log(this.state.myFnArray))
		}
	 //iStr = iStr.split(";").pop();
 }


 pusher = () => {
	 var myob = {} ;
	 myob['image_data'] = this.state.myimgArray ;
	 myob['email'] = 'test_email@duke.edu';
	 myob['filename'] = this.state.myFnArray ;

 axios.post('http://vcm-7308.vm.duke.edu:5000/api/process/upload_image', myob)
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
	 myob['email'] = 'test_email@duke.edu';
	 myob['filename'] = 'stevenisASIAN.zip'
 axios.post('http://vcm-7308.vm.duke.edu:5000/api/process/upload_image', myob)
 .then(res => {
	console.log(res)
 })
 .catch(function (error) {
console.log(error);
});
 }

	render() {
		return (

			<Grid container direction="column" justify="flex-end" alignItems="center">
				<Paper className='paper'>


					<h2> Upload Images! (zip is uploaded automatically) </h2>
					<Button color = 'primary' variant = 'contained' style= {{margin: '5px'}}>
					<UploadField onFiles={this.onUpload}>
						Upload
						</UploadField>
						</Button>

						<Button color = 'primary' variant = 'contained' style= {{margin: '5px'}}>
						<UploadField onFiles={this.onUploadzip}>
							Upload ZIP
							</UploadField>
							</Button>

						<img src={this.state.currentImageString} />

						<Button style= {{margin: '5px'}} variant='contained' color='primary' onClick={this.pusher}>
						Confirm Upload
						</Button>



				</Paper>
			</Grid>

		)
	}
}
