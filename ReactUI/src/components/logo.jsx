import React, { Component } from 'react';
import './css/logo.css';

class Logo extends Component {
    state = {}
    render() {
        return (
            <span className='logo'>
                <a href='/'>Social<br />Sent</a>
            </span>
        );
    }
}

export default Logo;