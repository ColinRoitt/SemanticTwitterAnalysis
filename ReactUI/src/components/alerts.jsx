import React, { Component } from 'react';
import './css/alerts.css';
import apiAccess from './apiAccess';

class Alerts extends Component {
    state = {
        alerts: []
    }
    render() {
        return (
            <React.Fragment>
                <h4>{this.props.profile.name}</h4>
                <span className='container-alerts'>
                    <span className='alerts'>
                        <div className="row">
                            <div className="card">
                                <div className="card-content">
                                    <ul className="collection with-header">
                                        <li className="collection-header">
                                            <h4>Alerts</h4>
                                        </li>
                                        {this.renderAlerts()}
                                    </ul>
                                    <a onClick={this.addAlert} className="FLOATY btn-floating btn-large waves-effect waves-light"><i className="material-icons">add</i></a>
                                </div>
                            </div>
                        </div>
                    </span>
                </span>
            </React.Fragment>
        );
    }

    componentDidMount() {
        this.updateAlerts();

    }

    updateAlerts = () => {
        let url = apiAccess.url + 'db/getTasks?key=' + this.props.profile.key;
        fetch(url)
            .then(result => {
                return result.json();
            })
            .then(result => {
                let alerts = [];
                result.forEach(t => {
                    let task = {
                        TaID: t['TaID'],
                        name: t['name'],
                        sentiment: t['class'],
                        symbol: t['compariator'],
                        bound: t['bound']
                    }
                    alerts.push(task);
                });
                this.setState({ alerts });
            });
    }

    addAlert = () => {
        let name = prompt('Enter a name');
        let sentiment = prompt('1 or -1');
        let symbol = prompt('Enter a symbol, > or <');
        let bound = prompt('Enter a bound, 1-99');

        let url = apiAccess.url + `db/addTask?key=${this.props.profile.key}&name=${name}&class=${sentiment}&comparator=${symbol}&bound=${bound}`

        fetch(url)
            .then(r => {
                this.updateAlerts();
            })
    }

    deleteTask = id => {
        let url = apiAccess.url + `db/deleteTask?key=${this.props.profile.key}&TID=${id}`;
        fetch(url)
            .then(result => {
                // console.log(result);
                this.updateAlerts();
            });
    }

    renderAlerts = () => {
        return (
            this.state.alerts.map(a =>
                <li key={a.name} className="collection-item">
                    <div>{a.name} - <em>{a.sentiment} {a.symbol} {a.bound}%</em>
                        <a href="#!" className="secondary-content">
                            <i onClick={() => this.deleteTask(a.TaID)} className="del material-icons">delete_outline</i>
                        </a>
                    </div>
                </li>)
        )
    }
}

export default Alerts;