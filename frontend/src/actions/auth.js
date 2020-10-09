import {
    LOGIN_START,
    LOGIN_FAILURE,
    LOGIN_SUCCESS,
    SIGNUP_START,
    SIGNUP_FAILURE,
    SIGNUP_SUCCESS,
    AUTHENTICATE_USER,
    LOG_OUT,
    CLEAR_AUTH_STATE,
    FORGOT_START,
    FORGOT_FAILURE,
    FORGOT_SUCCESS,

} from './actionTypes';
// @ts-ignore
import jwt_decode from "jwt-decode";


//Form Body
//converting data in format variable1=key1&variable2=key2...
//this needs to be checked with django api if this format not accepted then send json object
function getFormBody(params) {
    let FormBody = [];
    for (let property in params) {
        let encodedKey = encodeURIComponent(property);
        let encodedValue = encodeURIComponent(params[property]);
        FormBody.push(encodedKey + '=' + encodedValue);
    }
    return FormBody.join('&');
}

//login
export function startLogin() {
    return {
        type: LOGIN_START,
    };
}

export function loginFailed(errormsg) {
    return {
        type: LOGIN_FAILURE,
        error: errormsg,
    };
}

export function loginSuccess(successmsg, username, email) {
    return {
        type: LOGIN_SUCCESS,
        username,
        email,
        success: successmsg,
    };
}


export function login(username, password) {
    return (dispatch) => {
        var success = false;
        dispatch(startLogin());
        const url = '/api/token/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: getFormBody({
                username: username,
                password
            }),
        })
            .then((response) => {
                if (response.status === 200) {
                    success = true;
                    return response.json();
                } else {
                    return response.json();
                }
            })
            .then((data) => {
                if (success) {
                    localStorage.setItem('DONNA', data.token);
                    const user = jwt_decode(data.token);
                    dispatch(loginSuccess("Login Successfull", user.username, user.email));

                } else {
                    dispatch(loginFailed("Username or Password is Incorrect"));
                }

            });
    };
}

//signup
export function startsignup() {
    return {
        type: SIGNUP_START,
    };
}

export function signupFailed(errormsg) {
    return {
        type: SIGNUP_FAILURE,
        error: errormsg,
    };
}

export function signupSuccess(msg) {
    return {
        type: SIGNUP_SUCCESS,
        success: msg,
    };
}

export function signup(email, password, confirmpassword, name, fname, lname) {
    return (dispatch) => {
        var success = false;
        dispatch(startsignup());
        const url = '/register';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: getFormBody({
                username: name,
                email,
                password,
                password_confirm: confirmpassword,
                first_name: fname,
                last_name: lname
            }),
        })
            .then((response) => {
                if (response.status === 201) {
                    success = true;
                    return response.json();
                } else {
                    return response.json();
                }
            })
            .then((data) => {
                if (success) {
                    dispatch(signupSuccess("SignUp successfull please LogIn to continue"));
                    return;
                }
                if (data.username) {
                    dispatch(signupFailed("User with this UserName already exists"));

                } else if (data.password) {
                    dispatch(signupFailed("Password and Confirm Password fields Don't match"));

                } else {
                    dispatch(signupFailed("Signup Failed Please Try Again"));
                }

            });
    };
}

//authenticate and logout
export function authenticateUser(user) {
    return {
        type: AUTHENTICATE_USER,
        user: user.name,
    };
}

export function logoutUser() {
    return {
        type: LOG_OUT,
    };
}

export function clearAuth() {
    return {
        type: CLEAR_AUTH_STATE,
    };
}


//FORGOT PASSWORD
export function startForgot() {
    return {
        type: FORGOT_START,
    };
}

export function forgotFailed(errormsg) {
    return {
        type: FORGOT_FAILURE,
        error: errormsg,
    };
}

export function forgotSuccess(successmsg) {
    return {
        type: FORGOT_SUCCESS,
        success: successmsg,
    };
}


export function forgot(email) {
    return (dispatch) => {
        dispatch(startForgot());
        var success = false;
        const url = '/api/password_reset/';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: getFormBody({email}),
        })
            .then((response) => {
                if (response.status === 200) {
                    success = true;
                    return response.json();
                } else {
                    return response.json();
                }
            })
            .then((data) => {
                console.log(data);

                if (success) {
                    dispatch(forgotSuccess("Reset Link Sent to your Registered Email Id"));

                } else if (data.email) {
                    dispatch(forgotFailed(data.email));

                }

            });
    };
}
