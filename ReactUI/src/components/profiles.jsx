import React, { Component } from 'react';
import './css/profiles.css';

class Profiles extends Component {
    render() {
        return (
            <React.Fragment>
                <span className='side'>
                    <div className='side-cont'>
                        {this.renderProfiles()}
                    </div>
                    <span>
                        <a onClick={() => { this.props.onAddProfile(prompt('Enter Name')) }} className="btn-floating btn-large waves-effect waves-light"><i className="material-icons">add</i></a>
                    </span>
                </span>
            </React.Fragment>
        );
    }

    renderProfiles() {
        let profiles = this.props.profiles
        if (profiles.length === 0) return
        return (
            profiles.map(p =>
                <div key={p.key} onClick={() => { this.props.handleProfileClick(p.key) }} className='hoverable profile-cont'>
                    <span className='profile'>{p.key}</span>
                </div>
            )
        )
    }

}

export default Profiles;