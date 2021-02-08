import React, {useContext, useEffect, useRef} from "react";
import {useHistory} from 'react-router-dom';
import './CSS/House.css'
import Cookies from 'js-cookie';
import {Dropdown,NavItem,NavLink} from 'react-bootstrap'
import {HouseContext} from './HouseContext'
import {HouseIDContext} from './HouseIDContext'

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
      <form className="form-inline my-2 my-lg-0">
        <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
        <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
      </form>
      </div>
    </nav>
  );
}

export default Nav