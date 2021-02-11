import React, {useContext, useEffect, useRef} from "react";
import {useHistory} from 'react-router-dom';
import Cookies from 'js-cookie';
import {Dropdown,NavItem,NavLink} from 'react-bootstrap'
import {HouseContext} from '../../Contexts/HouseContext'
import {HouseIDContext} from '../../Contexts/HouseIDContext'
import Notifications from './Notifications'

const Nav = (props) => {
  let history = useHistory();
  const setAuth = props.value[1];
  const houseList = useContext(HouseContext)[0];
  const [houseID,setHouseID] = useContext(HouseIDContext);
  const isFirstRender = useRef(true);

  const logout = () => {
    Cookies.remove("user");
    setAuth(false);
    Cookies.remove("currentHouseID");
    Cookies.remove("id");
    history.push("/");
    
  }

  const goHouseList = () => {
    Cookies.remove("currentHouseID");
    history.push("/houses");
  }

  const enterHouse = (house_id) => {
    setHouseID(house_id)
  }

  useEffect(() => {
    if(!isFirstRender.current){
      Cookies.set("currentHouseID",houseID);
      history.push("/chores")
    }
  },[houseID,history])

  useEffect(() => { 
    isFirstRender.current = false;
  }, [])

  return (
  <nav className="navbar-expand-md navbar-dark bg-dark">
    <a className="navbar-brand" href="#">Test</a>
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>

    <div className="collapse navbar-collapse" id="navbarSupportedContent">
      <ul className="navbar-nav mr-auto">
      <li className="nav-item">
          <a className="nav-link" href="" onClick={goHouseList}>Home</a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="" onClick={logout}>LogOut</a>
        </li>
        <Dropdown as={NavItem}>
          <Dropdown.Toggle as={NavLink}>
            Dropdown Button
          </Dropdown.Toggle>

          <Dropdown.Menu>
            {houseList.map((house) => 
              (<Dropdown.Item onClick={() => enterHouse(house.house_id)}>{house.name}</Dropdown.Item>)
            )}
          </Dropdown.Menu>
        </Dropdown>
      </ul>

      <Notifications>

      </Notifications>
      </div>
    </nav>
  );
}

export default Nav