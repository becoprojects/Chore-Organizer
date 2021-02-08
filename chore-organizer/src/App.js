import React from 'react';
import './CSS/App.css';
import {BrowserRouter as Router, Switch, Route, Redirect} from 'react-router-dom';
import Login from './Login';
import HouseList from './HouseList';
import AuthApi from './AuthApi';
import Cookies from 'js-cookie';
import HouseDashboard from './HouseDashboard'
import Nav from './Nav'
import OfferForm from './OfferForm';
import {ChoreProvider} from './ChoreContext'
import {OfferProvider} from './OfferContext'
import {HouseProvider} from './HouseContext'
import {HouseIDProvider} from './HouseIDContext'
import AcceptOfferForm from './AcceptOfferForm'
import ErrorPage from './ErrorPage'

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
