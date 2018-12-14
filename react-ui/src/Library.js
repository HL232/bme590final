 import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import image from './a.jpeg'
import { CloudDownload } from '@material-ui/icons'
import Picture from './Picture'
const TileData = [
  {
    img: image,
    title: 'Image',
    author: 'author',
  },
  {
    img: image,
    title: 'Image',
    author: 'author',
  }

]

export default class Library extends Component {

state = {
    myData: [],
    dType : '.jpg',
    passbackI: '',
		passState: 0,
    idArray:  [],

  }

  pushtoID = () => {
    var myAh = this.state.idArray
    var myI = this.state.passbackI.image_id
    myAh.push(myI)
    this.setState({idArray: myAh}, console.log(this.state.idArray))
  }

  grabfromKid = (win, im) => {
    this.setState({passState: win, passbackI: im}, () => {
      this.pushtoID() ;
    }) ;

  }

  setDtype = (myT) => {
    this.setState({dType: myT}, () => {
      this.getIms() ;
    })
  }

  getIms = () => {
    var myob2 = {}
    myob2['email'] = 'lickaD@no.';
    myob2['format'] = this.state.dType ;
    myob2['image_ids'] = this.state.idArray ;
    axios.post('http://127.0.0.1:5000/api/image/get_images_zipped', myob2)
 	 .then(res => {
     var myAr = []
     myAr.push(res.data)
     this.setState({afterIM: myAr}, () => {
       this.pullArray() ;
     })
 	 })
 	 .catch(function (error) {
  console.log(error);
 });
  }

getData = () => {
  console.log('getData')
  //axios.get("http://127.0.0.1:5000/api/image/get_current_image/myID@no.")
  //http://127.0.0.1:5000/api/user/get_original_uploads/myID@no.
  axios.get("http://127.0.0.1:5000/api/user/get_updated_uploads/lickaD@no.").then(res => {


    var myAr = []
    console.log(res.data)
    myAr = res.data
    console.log(myAr)
    this.setState({myData: myAr})
    //console.log(this.state.myData[0].image_data)
  })
}

containData = () => {
  if (this.state.myData.length === 0){
    {this.getData()}
  }
  //{console.log(image)}
}

down = () => {

}


  render() {

    return(
      <div>
      {this.containData()}

      <Paper className='paper'>
      <Button onClick={() => this.setDtype('jpg')} variant="contained"   color="primary" style= {{margin: '5px'}} >
        JPG </Button>
        <Button onClick={() => this.setDtype('png')} variant="contained"   color="primary" style= {{margin: '5px'}} >
          PNG </Button>
          <Button onClick={() => this.setDtype('TIFF')} variant="contained"   color="primary" style= {{margin: '5px'}} >
            TIFF </Button> <br />
      <GridList cellHeight={400} cols={3}>

        <GridListTile key="Subheader" cols={1} style={{height: 'auto'}}>
          <ListSubheader component="div"> Library </ListSubheader>
        </GridListTile>
        // All I have to do here is change this to myData.map and make sure
        // that the '.' parts match the data type
        // probably need a little tweaking to pull the thing out of the state though
        {this.state.myData.map(tile => (
          <Picture onSel={this.grabfromKid} dType = {this.state.dType} tile={tile}/>

        ))}

        </GridList>
        </Paper>
        </div>
    )
  }
}
