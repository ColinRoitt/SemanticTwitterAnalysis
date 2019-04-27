import React, { Component } from 'react';
import M from 'materialize-css';
import './css/edit.css';
import apiAccess from './apiAccess';

class Edit extends Component {
    state = { running: false }

    componentDidMount() {
        // M.Chips.init(document.querySelectorAll('.chips'));
        M.FormSelect.init(document.querySelectorAll('select'));

        this.setChips();
        this.setCount();
        this.setStart();
        this.updateIsRunning();
    }

    componentDidUpdate() {
        if (this.props.profile) {
            this.setChips();
            this.setCount();
            this.setStart();
            this.updateIsRunning();
        }
    }

    setChips() {
        M.Chips.init(document.querySelectorAll('.chips'));
        let inst = M.Chips.getInstance(document.querySelector('.chips'));
        let chips = this.props.profile['search'].split(',');
        chips.forEach(c => {
            inst.addChip({ tag: c });
        });
    }

    setStart() {
        M.Datepicker.init(document.querySelectorAll('.datepicker'), {
            format: 'yyyy-mm-dd'
        });
        let inst = M.Datepicker.getInstance(document.querySelector('.datepicker'));
        let dt = new Date(this.props.profile['start']);
        inst.setDate(dt);
        // bodge it
        document.querySelector('.datepicker').click();
        document.querySelectorAll('.btn-flat')[2].click();

    }

    setCount() {
        M.Range.init(document.querySelectorAll("input[type=range]"));
        let val = this.props.profile['countPerDay'];
        document.querySelector('input[type=range]').value = val;
    }

    handleSaveAndRun() {
        let profileData = this.props.profile;

        let instChip = M.Chips.getInstance(document.querySelector('.chips'));
        let newChips = instChip.chipsData.map(p => p.tag).join(',');
        profileData['search'] = newChips;

        let newSocial = document.querySelector('#socialSelector').value;
        profileData['social'] = newSocial;

        let instDate = M.Datepicker.getInstance(document.querySelector('.datepicker'));
        let newStart = instDate.toString();
        profileData['start'] = newStart;

        let newCount = document.querySelector('input[type=range]').value;
        profileData['countPerDay'] = newCount;

        let apiUrl = apiAccess.url + `db/updateProfile?` +
            `key=${profileData['key']}&` +
            `name=${profileData['name']}&` +
            `search=${profileData['search']}&` +
            `social=${profileData['social']}&` +
            `start=${profileData['start']}&` +
            `countPerDay=${profileData['countPerDay']}`.trim();
        fetch(apiUrl)
            .then(results => {
                // console.log(results)
            });
    }

    handleDeleteProfile() {
        if (window.confirm('Are you sure you want to delete this profile')) {

            let apiUrl = apiAccess.url + `db/deleteProfile?key=${this.props.profile.key}`;
            fetch(apiUrl)
                .then(results => {
                    this.props.onDeleteProfile();
                });
        }
    }

    runProfile() {
        if (this.state.running) {
            let url = apiAccess.url + 'sessMan/stopProfile?key=' + this.props.profile.key
            fetch(url)
                .then(result => {
                    console.log(result);
                    this.updateIsRunning();
                });
        } else {
            let url = apiAccess.url + 'sessMan/getTweets?key=' + this.props.profile.key
            fetch(url)
                .then(result => {
                    console.log(result);
                    this.updateIsRunning();
                });
        }
    }

    renderButton = () => {
        let classList = "submit waves-effect waves-light btn";
        let text = 'Run';
        if (this.state.running === true) {
            classList += ' red';
            text = 'Stop';
        } else {
            classList += ' green';
        }
        return <a id='runButton' className={classList} onClick={() => this.runProfile()}>{text}</a>
    }

    updateIsRunning = () => {
        let url = apiAccess.url + `sessMan/isRunning?key=${this.props.profile.key}`;
        fetch(url)
            .then(results => {
                return results.text();
            })
            .then(result => {
                // console.log(result)
                if (result == 'True' && !this.state.running) {
                    let running = true;
                    this.setState({ running });
                } else if (result == 'False' && this.state.running) {
                    let running = false;
                    this.setState({ running });
                }
            });
    }

    render() {
        return (
            <div id='containerEdit' >
                <span id='edit'>
                    <h4>{this.props.profile.name}</h4>
                    <div id='chips' className="chips chips-placeholder input-field">
                        <input className='input' placeholder='Search terms' />
                    </div>
                    <span className='social'>
                        Social media to access
                        <div className="input-field col s12">
                            <select id='socialSelector' defaultValue='Choose a social media'>
                                {/* <option value="" disabled selected>Choose a social media</option> */}
                                <option value="twitter">Twitter</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </span>
                    <span className='date'>
                        Earliest tweets (max 30 days)
                        <input type="text" className="datepicker" placeholder="Pick a date to search from" />
                    </span>
                    <span className='number'>
                        Number of tweets to pull per day
                        <p className="range-field">
                            <input type="range" id="test5" min="1" max="100" />
                        </p>
                    </span>
                    <a className="submit waves-effect waves-light btn" onClick={() => this.handleSaveAndRun()}>Save</a>
                    <a id='deleteBtn' className="submit red waves-effect waves-light btn" onClick={() => this.handleDeleteProfile()}>Delete</a>
                    {this.renderButton()}
                </span>
            </div >
        );
    }
}

export default Edit;