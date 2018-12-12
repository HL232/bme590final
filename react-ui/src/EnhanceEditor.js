import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'

export default class EnhanceEditor extends Component {

  state = {
    beforeIM: '',
    afterIM: [],
    enhtype: 1,

  }

setImage = () => {
  var myob = {}
  var iStr2 = this.state.afterIM.image_id
  //iStr = iStr.split(";").pop();
    myob['user_id'] = 'myID';
    myob['image_id'] = iStr2 ;

  axios.post('http://127.0.0.1:5000/api/process/change_image', myob)
  .then(res => {
   console.log(res)
  })
  .catch(function (error) {
console.log(error);
});
}

beforeSelector = () => {
  if (this.state.beforeIM.length === 0) {
    this.setState({beforeIM: this.props.tile})
    this.setState({afterIM: this.props.tile})
    {this.setImage()} ;
  }
  else {
    //console.log(this.state.afterIM)
  }
}

afterSelector = () => {
  var enhtype = this.state.enhtype
  if (enhtype === 0){

  }
  else if (enhtype === 1) {
    var myob2 = {}
    myob2['user_id'] = this.state.beforeIM.user_id
    axios.get('http://127.0.0.1:5000/api/process/blur', myob2)
 	 .then(res => {
     var myAr = []
     myAr.push(res.data)
     this.setState({afterIM: myAr})
 	 })
 	 .catch(function (error) {
  console.log(error);
 });
  }
  else if (enhtype === 2) {

  }
  else if (enhtype === 3) {

  }
  else if (enhtype === 4) {

  }
}

  render() {
    return(
      <div>
      {this.beforeSelector()}

      <Button color='primary' variant='contained' onClick={this.afterSelector}>
      Histogram EQ
      </Button>
      Before:
      <br />
      <img src={this.state.beforeIM.image_data} />
      <br />
      ||
      VV
      After:
      <img src={"data:image/jpeg;" + this.state.afterIM.image_data} />


      </div>
    )
  }
}
