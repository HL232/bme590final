import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'

import DisEnh from './DisEnh'


export default class MyEnhance extends Component {

	state = {
		myData: [],
		passbackI: '',
		passState: 0,
	}

	passUp = () => {
		var win = this.state.passState ;
		var im = this.state.passbackI ;
		this.props.onMyEnhance(win, im)
	}

	grabfromKid = (win, im) => {
		this.setState({passState: win}) ;
		this.setState({passbackI: im}) ;
		{this.passUp()} ;
	}


	containData = () => {
	  if (this.state.myData.length === 0){
	    {this.getData()}
	  }
	  //{console.log(image)}
	}

	getData = () => {
	  console.log('getData')
	  axios.get("http://127.0.0.1:5000/api/image/get_current_image/myID").then(res => {


	    var myAr = []
	    myAr.push(res.data)
	    this.setState({myData: myAr})
	    //console.log(this.state.myData[0].image_data)
	  })
	}

	render() {
		return (

			<div>
			{this.containData()}

			<Paper className='paper'>
			<GridList cellHeight={400} cols={3}>

				<GridListTile key="Subheader" cols={1} style={{height: 'auto'}}>
					<ListSubheader component="div"> Library </ListSubheader>
				</GridListTile>
				// All I have to do here is change this to myData.map and make sure
				// that the '.' parts match the data type
				// probably need a little tweaking to pull the thing out of the state though
				{this.state.myData.map(tile => (
					<DisEnh tile={tile} onSel={this.grabfromKid}/>

				))}

				</GridList>
				</Paper>

			 </div>

		)
	}
}
