import React, { Component } from 'react';
import {ListSubheader, IconButton, GridList, GridListTile, GridListTileBar, Button, Typography, Grid, Paper} from '@material-ui/core';
import axios from 'axios'
import MyEnhance from './MyEnhance'
import EnhanceEditor from './EnhanceEditor'


export default class MainEnhance extends Component {

  state = {
    winStat: 0,
    imgStat: '',
  }

  handleChange = (win, im) => {
    this.setState({winStat: win});
    this.setState({imgStat: im});

  }

  eSelect = () => {
    if(this.state.winStat === 1) {
      console.log(this.state.imgStat)
      console.log(this.state.winStat)
      return (<EnhanceEditor tile={this.state.imgStat} onEnhanceEditor={this.handleChange}/>)
    }
    else {
      return (<MyEnhance onMyEnhance={this.handleChange}/>)
    }
  }

  render() {
    return (

      <div>
        {this.eSelect()}
      </div>


    )
  }
}
