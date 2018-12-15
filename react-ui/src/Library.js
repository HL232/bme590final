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
    myob2['email'] = 'test_email@duke.edu';
    myob2['format'] = this.state.dType ;
    myob2['image_ids'] = this.state.idArray ;
    axios.post('http://vcm-7308.vm.duke.edu:5000/api/image/get_images_zipped', myob2)
 	 .then(res => {

    var img = res.data.zip_data
    var url = 'data:application/x-zip-compressed;base64,' + img
    window.open(url);

 	 })
 	 .catch(function (error) {
  console.log(error);
 });
  }

getData = () => {
  console.log('getData')
  //axios.get("http://vcm-7308.vm.duke.edu:5000/api/image/get_current_image/test_email@duke.edu")
  //http://vcm-7308.vm.duke.edu:5000/api/user/get_original_uploads/myID@no.
  axios.get("http://vcm-7308.vm.duke.edu:5000/api/user/get_updated_uploads/test_email@duke.edu").then(res => {


    var myAr = []

    myAr = res.data

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
            TIFF </Button>
            <h2> Use these to Download Desired File Type: Click to add images then when all images have been selected press desired button</h2> <br />
      <GridList cellHeight={400} cols={3}>

        <GridListTile key="Subheader" cols={1} style={{height: 'auto'}}>
          <ListSubheader component="div"> <h1>Library</h1> </ListSubheader>
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
