import React, { useContext } from "react";
import {useHistory } from 'react-router-dom';
import Cookies from 'js-cookie';
import House from './House'
import './CSS/App.css'
import { getHouseByUser } from "./utils/apiUtils";
import {HouseContext} from './HouseContext';

export default function HouseList() {
    let history = useHistory();
    const [houseList,setHouseList] = useContext(HouseContext);

    React.useEffect(() => {
        const userID = Cookies.get("id");
        getHouseByUser(userID)
        .then((res) => {
           if(res === null){
            history.push("/errorscreen");
           } 
           else{
               setHouseList(res);
           }
        });
    }, [history,setHouseList]);

    return (
        <div className="HouseList">
            {houseList.map((house) => (<House key={house.house_id} house_id={house.house_id} name={house.name} description={house.description}/>))}
        </div>
    );
}
