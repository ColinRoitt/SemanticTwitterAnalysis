import React, { Component } from 'react';
import { GoogleCharts } from 'google-charts';
import './css/view.css';
import apiAccess from './apiAccess';

class View extends Component {
    state = {
        goodTweets: [],
        badTweets: [],
        neutTweets: []
    }

    componentDidMount() {
        let url = apiAccess.url + 'db/getProfileTweets?key=' + this.props.profile.key;
        fetch(url)
            .then(result => {
                // console.log(result)
                return result.json();
            })
            .then(result => {
                let goodTweets = [];
                result.filter(r => r['sentiment'] == '1').forEach(t => {
                    goodTweets.push(t);
                });
                this.setState({ goodTweets });
                let badTweets = [];
                result.filter(r => r['sentiment'] == '-1').forEach(t => {
                    badTweets.push(t);
                });
                this.setState({ badTweets });
                let neutTweets = [];
                result.filter(r => r['sentiment'] == '0').forEach(t => {
                    neutTweets.push(t);
                });
                this.setState({ neutTweets });

                //now load charts
                GoogleCharts.load(this.drawLineChart);
                GoogleCharts.load(this.drawColumnChart);
            });
    }

    drawLineChart = () => {
        let rawData = [];
        let n = this.state.goodTweets;
        this.state.badTweets.forEach(t => {
            n.push(t);
        });
        this.state.neutTweets.forEach(t => {
            n.push(t);
        });

        n.forEach(t => {
            let date = new Date(t['dateGot']);
            let words = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            // rawData.push([`${date.getDay()} ${words[date.getMonth()]} ${date.getFullYear()}`, parseInt(t['sentiment']), t['content']]);
            rawData.push([date, parseInt(t['sentiment']), t['content']]);
        });

        rawData.sort((a, b) => {
            let dateA = new Date(a[1]);
            let dateB = new Date(b[1]);
            if (dateA < dateB) return -1;
            if (dateB > dateA) return 1;
            return 0;
        });
        // console.table(rawData);

        let data = new GoogleCharts.api.visualization.DataTable();
        data.addColumn('date', 'Date');
        data.addColumn('number', 'Sentiment');
        data.addColumn({ type: 'string', role: 'tooltip' });
        data.addRows(rawData);
        let options = {
            title: 'Sentiment over time',
            legend: 'none',
            explorer: {
                axis: 'horizontal',
                keepInBounds: true,
                maxZoomIn: 15.0
            },
        };
        let chrt = new GoogleCharts.api.visualization.ScatterChart(document.getElementById('curve_chart'));

        chrt.draw(data, options);

    }

    drawColumnChart = () => {
        // console.log(this.state.goodTweets.filter(t => t['certainty'] < 50));
        let len = this.state.goodTweets.length + this.state.badTweets.length;
        let pos = [
            ((this.state.goodTweets.filter(t => t['certainty'] < 50).length) / len) * 100,
            ((this.state.goodTweets.filter(t => t['certainty'] >= 50 && t['certainty'] < 75).length) / len) * 100,
            ((this.state.goodTweets.filter(t => t['certainty'] >= 75).length) / len) * 100
        ];

        let neg = [
            ((this.state.badTweets.filter(t => t['certainty'] < 50).length) / len) * 100,
            ((this.state.badTweets.filter(t => t['certainty'] >= 50 && t['certainty'] < 75).length) / len) * 100,
            ((this.state.badTweets.filter(t => t['certainty'] >= 75).length) / len) * 100
        ];

        let neut = [
            ((this.state.neutTweets.filter(t => t['certainty'] < 50).length) / len) * 100,
            ((this.state.neutTweets.filter(t => t['certainty'] >= 50 && t['certainty'] < 75).length) / len) * 100,
            ((this.state.neutTweets.filter(t => t['certainty'] >= 75).length) / len) * 100
        ];

        let data = GoogleCharts.api.visualization.arrayToDataTable([
            ['Sentiment', '<50%', '>50%', '>75%', { role: 'annotation' }],
            ['Positive Sentiment', pos[0], pos[1], pos[2], ''],
            ['Negative Sentiment', neg[0], neg[1], neg[2], ''],
            ['Neutral Sentiment', neut[0], neut[1], neut[2], '']
        ]);

        let options = {
            width: 400,
            legend: { position: 'top', maxLines: 3 },
            bar: { groupWidth: '75%' },
            isStacked: true,
            vAxis: { minValue: 0, maxValue: 100 }
        };

        let chart = new GoogleCharts.api.visualization.ColumnChart(document.getElementById('bar_chart'));

        chart.draw(data, options);
    }

    render() {
        return (
            <React.Fragment>
                <h4>{this.props.profile.name}</h4>
                <span className='container-vieww'>
                    <span className='line'>
                        <div id="curve_chart"></div>
                    </span>
                    <span className='bar'>
                        <div id="bar_chart"></div>
                    </span>
                    <span className="tweets goodtweets">
                        <h5>Positive sentiment</h5>
                        <div className="tweet_cont">
                            {this.renderTweets(this.state.goodTweets)}
                        </div>
                    </span>
                    <span className="tweets badtweets">
                        <h5>Negative sentiment</h5>
                        <div className="tweet_cont">
                            {this.renderTweets(this.state.badTweets)}
                        </div>
                    </span>
                </span>
            </React.Fragment>
        );
    }

    renderTweets = (tweetsToRender) => {
        let tweets = tweetsToRender;
        let i = 0;
        return (
            tweets.map(t =>
                <span key={i++} className='tweet'>
                    <div className="row">
                        <div className="card">
                            <div className="card-content">
                                {t.content}
                            </div>
                        </div>
                    </div>
                </span>
            )
        )
    }
}

export default View;