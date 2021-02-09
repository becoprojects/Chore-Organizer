import React, {useContext, useEffect, useRef} from "react";
import {useHistory} from 'react-router-dom';
import '../../CSS/House.css'
import Cookies from 'js-cookie';
import {HouseIDContext} from '../../Contexts/HouseIDContext';

const House = (props) => {
  let history = useHistory();
  const [houseID,setHouseID] = useContext(HouseIDContext);
  const isFirstRender = useRef(true);

  const enterHouse = async () => {
    await setHouseID(props.house_id)
    console.log(houseID);
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
    <div className="OuterBorder">
        <div className="HouseSelect" onClick={enterHouse}>
            <h3>{props.name}</h3>
            <p>{props.description}</p>
        </div>
    </div>
  );
}

export default House