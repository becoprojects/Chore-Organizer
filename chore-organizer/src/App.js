import React from 'react';
import './CSS/App.css';
import {BrowserRouter as Router, Switch, Route, Redirect} from 'react-router-dom';
import Login from './Components/Login/Login';
import HouseList from './Components/House/HouseList';
import AuthApi from './Contexts/AuthApi';
import Cookies from 'js-cookie';
import HouseDashboard from './Components/Dashboard/HouseDashboard'
import Nav from './Components/Misc/Nav'
import OfferForm from './Components/Offer/OfferForm';
import {ChoreProvider} from './Contexts/ChoreContext'
import {OfferProvider} from './Contexts/OfferContext'
import {HouseProvider} from './Contexts/HouseContext'
import {HouseIDProvider} from './Contexts/HouseIDContext'
import AcceptOfferForm from './Components/Offer/AcceptOfferForm'
import ErrorPage from './Components/Misc/ErrorPage'

function App(props) {
  const [auth,setAuth] = React.useState('');

  const readCookie = () => {
    const user = Cookies.get("user");
    if (user){
      setAuth(true);
    }
  }

  React.useEffect(() => {
    readCookie();
  },[]);

  return (
    <AuthApi.Provider value={[auth,setAuth]}>
      <div className="App-header">
        <Router>
          <HouseProvider>
          <HouseIDProvider>
          {auth && <Nav value={[auth,setAuth]}/>}
          <Switch>
              <Route path="/errorscreen" exact component={ErrorPage}/>
              <ProtectedLogin path="/" exact component={Login} auth={auth}/>
              <ProtectedRoute cooks={['id']} redirectLinks={['/']} path="/houses" component={HouseList}/>
              <ChoreProvider>
              <OfferProvider>
                <ProtectedRoute cooks={['id','currentHouseID']} redirectLinks={['/','/houses']} path="/chores" component={HouseDashboard}/>
                <ProtectedRoute cooks={['id','currentHouseID']} redirectLinks={['/','/houses']} path="/makeoffer" component={OfferForm}/>
                <ProtectedRoute cooks={['id','currentHouseID']} redirectLinks={['/','/houses']} path="/acceptoffer" component={AcceptOfferForm}/>
              </OfferProvider>
              </ChoreProvider>    
          </Switch>
          </HouseIDProvider>
          </HouseProvider>
        </Router>
      </div>
     </AuthApi.Provider>
  );
}

const ProtectedRoute = ({cooks,redirectLinks,component:Component,...rest}) => {
  var i;
  for(i=0; i<cooks.length; i++){
    if(Cookies.get(cooks[i]) == null){
      return (<Redirect to={redirectLinks[i]}/>);
    }
  }
  return(
    <Route
      {...rest}
      render = {() => 
        (<Component/>) 
      }
    />
  );
}

const ProtectedLogin = ({auth,component:Component,...rest}) => {
  return(
    <Route
      {...rest}
      render = {() => 
        !auth ? (<Component/>) : 
        (
          <Redirect to="/houses"/>
        )
      }
    />
  );
}

export default App;
