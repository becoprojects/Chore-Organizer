import React, { useState, useContext } from "react";
import Button from "react-bootstrap/Button";
import AuthApi from './AuthApi'
import Cookies from 'js-cookie';
import './CSS/Login.css'

export default function Login() {
  const setAuth = useContext(AuthApi)[1];
  const [userID, setUserID] = useState("");

  const handleOnClick = () => {
    setAuth(true);
    Cookies.set("user","true");
    Cookies.set("id",userID);
  }

  const validateInput = () => {
      if(userID.length > 0){
        return true;
      }
  }


  const handleChange = (event) => {
      setUserID(event.target.value);
  }

  const handleEnter = (event) => {
    if(validateInput() && event.keyCode===13){
      handleOnClick();
    }
  }

  return (
    <div className="container loginContainer">
        <div className="row h-100">
        <div className="col-4 offset-4" align="center">
        <div className="LoginBox">
        <h3>Enter Your ID</h3>
              <input value={userID} onChange={handleChange} onKeyDown={handleEnter}></input>
              <br/>
              <Button className="LoginButton" onClick={handleOnClick} disabled={!validateInput()}>Login</Button>
        </div>
        </div>
        </div>
    </div>

  );
}
