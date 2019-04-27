import React, { Component } from 'react';
import M from 'materialize-css';
import './css/tabs.css';

class Tabs extends Component {
    state = {}

    componentDidMount() {
        M.Tabs.init(document.querySelector('.tabsToInit'));
    };

    render() {
        return (
            <React.Fragment>
                <ul className="tabsToInit z-depth-1 tabs tabs-fixed-width">
                    <li onClick={() => this.props.onChangeScreen('Edit')} className="tab">
                        <a href="/">
                            <i className="small material-icons">create</i>
                        </a>
                    </li>
                    <li onClick={() => this.props.onChangeScreen('View')} className="tab">
                        <a href="/">
                            <i className="small material-icons">show_chart</i>
                        </a>
                    </li >
                    <li onClick={() => this.props.onChangeScreen('Alert')} className="tab">
                        <a href="/">
                            <i className="small material-icons">add_alert</i>
                        </a>
                    </li >
                </ul >
            </React.Fragment >
        );
    }
}


export default Tabs;