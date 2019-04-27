import React, { Component } from "react";
import './css/nav.css';
import Tabs from './tabs';

class Nav extends Component {
    state = {}
    render() {
        return (
            <div className='top'>
                <Tabs onChangeScreen={this.props.onChangeScreen} />
            </div>
        );
    }
}

export default Nav;
