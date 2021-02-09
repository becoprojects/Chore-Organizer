import React from 'react'
import axios from 'axios'

class LoginForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = {value: ''};
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {    
        this.setState({value: event.target.value});  
    }

    handleSubmit(event) {
        this.getDataAxios();
        event.preventDefault();
    }

    async getDataAxios(){
        await axios.get("http://localhost:5000/gethousesbyuser/" + this.state.value)
        .then(response => {console.log(response.data)})
        .catch(err => {
            if (err.response) {
                console.log("error making api request: " + err);
              } else if (err.request) {
                console.log("error making api request: " + err);
              } else {
                console.log("error making api request: " + err);
              }
        });
        
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>        
            <label for="userid">ID:</label><br/>
            <input type="text" id="userid" name="userid" value={this.state.value} onChange={this.handleChange}/><br/>
            <input type="submit" value="Login"/>
        </form>
      );
    }
  }

  export default LoginForm;