import React, {Component} from 'react';
import "./../App.scss"
import {Map, GoogleApiWrapper} from 'google-maps-react';

const mapStyles = {
    height: "100%",
    position: "relative",
};

export class MapContainer extends Component {

    render() {
        return (
            <div style={{position: 'relative', width: '100%', paddingTop: '20px', paddingBottom: '20rem'}}>
                <div style={{position: 'relative', width: '100%', paddingBottom: '50vh'}}>
                    <Map
                        google={this.props.google}
                        zoom={14}
                        style={mapStyles}
                        initialCenter={
                            {
                                lat: 40.712776,
                                lng: -74.005974
                            }
                        }
                    />
                </div>
            </div>
        );
    }
}

export default GoogleApiWrapper({
    apiKey: 'AIzaSyA7t9tVpTx-jiwprTQfm-pMr5nd0V_PDOM'
})(MapContainer);
