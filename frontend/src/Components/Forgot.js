import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';

import { forgot, clearAuth } from "../actions/auth";

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
          email: ''
        };
      }
      //to clear the error if it comes on reload or whenever the user shifts from this page
    componentWillUnmount() {
    this.props.dispatch(clearAuth());
  }


  handleSubmitForm = (e) => {
    e.preventDefault();
    const {email} = this.state;
    if (email) {
      this.props.dispatch(forgot(email));
    }
  };
  handleEmail = (e) => {
    this.setState({
      email: e.target.value,
    });
  };
      
    render() {
        const {  inProgress, error, isLoggedIn } = this.props.auth;

        //so that logged in user don't sees the Forgot Password page even if he tries to manupalate url 
        if (isLoggedIn) {
          return <Redirect to="/" />;
        }
        return (
        <div className="home-screen">
            <div className="forgot-form">
             <h5>Please Enter your Registered Email ID</h5>
                
                <div className="form-fields">
                    {error && <div className="alert-done"><button>Error</button></div>}
                    <br></br>
                    <input type="email" placeholder="Email" required onChange={this.handleEmail} />
                    <button onClick={this.handleSubmitForm} disabled={inProgress}>Submit</button>
                    <p className="Forgot"> OR</p>
                    <p className="Forgot"><Link to="/login">Login</Link> | <Link to="/sign-up">New User</Link> </p>
                </div>

            </div>
            
        </div>
        );
    }
}
function mapStateToProps(state) {
  return {
    auth: state.auth,
  };
}

export default connect(mapStateToProps)(Login);