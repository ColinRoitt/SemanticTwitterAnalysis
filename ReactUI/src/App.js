import React, { Component } from 'react';
import './App.css';
import Nav from './components/nav';
import Profiles from './components/profiles';
import Logo from './components/logo';
import Edit from './components/edit';
import View from './components/view';
import Alerts from './components/alerts';
import NoProf from './components/NoProf';
import apiAccess from './components/apiAccess';

class App extends Component {
  state = {
    profiles: [],
    activeProfile: {},
    activeScreen: 'NoProf'
  }

  render() {
    return (
      <React.Fragment>
        <div className='container-template'>
          <Nav onChangeScreen={this.setActiveScreen} />
          <Logo />
          <Profiles
            onAddProfile={this.handleAddProfile}
            handleProfileClick={this.changeSelectedProfile}
            profiles={this.state.profiles} />
          {this.getActiveScreen()}
        </div>
      </React.Fragment>
    );
  }

  componentDidMount = () => {
    this.updateProfileList();
  }

  changeSelectedProfile = profile => {
    let prof = this.state.profiles.filter(p => p.key === profile);
    this.setState({ activeProfile: prof[0] });
    let activeScreen = 'Edit';
    // this.setActiveScreen('Edit');
    this.setState({ activeScreen });
  }

  setActiveScreen = screen => {
    let activeScreen = screen;
    if (this.state.activeScreen !== activeScreen) {
      this.setState({ activeScreen });
    }
  }

  getActiveScreen = () => {
    if (this.state.activeProfile === {}) {

    }
    let screen = this.state.activeScreen;
    switch (screen) {
      case 'Edit':
        return (
          <div className='container-edit'>
            <Edit onDeleteProfile={this.updateProfileList} profile={this.state.activeProfile} />
          </div>
        )
      case 'Alert':
        return (
          <div className='container-alert'>
            <Alerts profile={this.state.activeProfile} />
          </div>
        )
      case 'View':
        return (
          <div className='container-view'>
            <View profile={this.state.activeProfile} />
          </div>
        )
      case 'NoProf':
        return (
          <div className='container-view'>
            <NoProf />
          </div>
        )
      default:
        break;
    }
  }

  updateProfileList = () => {
    fetch(apiAccess.url + 'db/getProfiles')
      .then(results => {
        return results.json()
      })
      .then(r => {
        this.setState({ profiles: r })
      });
    this.setState({ activeProfile: 'NoProf' })
  }

  handleAddProfile = name => {
    if (name !== null) {
      if (name.length > 3) {
        let apiUrl = apiAccess.url + `db/addProfile?` +
          `name=${name}&` +
          `search=&` +
          `social=&` +
          `start=&` +
          `countPerDay=`.trim();
        console.log(apiUrl);

        fetch(apiUrl)
          .then(results => {
            console.log(results)
            this.updateProfileList();
          });
      }
    } else {
      alert('Name must be longer than 3 characters');
    }
  }

  // deleteProfile = () => {
  //   let newProfs = []
  //   this.state.profiles.forEach(p => {
  //     if (this.state.activeProfile != p) {
  //       newProfs.push(p);
  //     }
  //   });
  //   this.setState({ profiles: newProfs })
  // }

}


export default App;
