import React from 'react';
import {Link} from "react-router-dom";

function NoPage() {
    return (
        <div className="container" id="notFound">
          <div className="row justify-content-center">
            <div className="col-md-8">
              <div className="card">
                <div className="card-body text-center">
                  <h2>404</h2>
                  <p>Sorry, the page you're looking for cannot be found.</p>
                  <Link to="/" className="btn btn-primary">Go Back to Home Page</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
    )
}

export default NoPage;
