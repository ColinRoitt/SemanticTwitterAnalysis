import React, { Component } from 'react';
import './css/NoProff.css';

class NoProf extends Component {
    state = {}
    render() {
        return (<h3 className={'NoProfError'} >No Profile Selected</h3>);
    }
}

export default NoProf;