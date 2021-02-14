import React, { useState, useContext } from "react";
import {useHistory} from 'react-router-dom';
import DraftChore from './DraftChore'
import '../../CSS/App.css'
import {ChoreContext} from '../../Contexts/ChoreContext'
import {getChoresByHouse, getCurrentPlacementByHouse} from '../../utils/apiUtils'
import {HouseIDContext} from '../../Contexts/HouseIDContext'
import Cookies from 'js-cookie';

export default function DraftPage() {
    let history = useHistory();
    const [chores,setChores] = useContext(ChoreContext);
    const house = useContext(HouseIDContext)[0];
    const userID = Cookies.get('id');
    const [placement,setPlacement] = useState({});

    React.useEffect(() => {
        getChoresByHouse(house.house_id).then((res) => {
            if(res === null){
                history.push("/errorscreen");
            }
            else{
                setChores(res);
            }
        });
        
        getCurrentPlacementByHouse(house.house_id).then((res) => {
            if(res !== null){
                setPlacement(res);
            }
        })
      }, []);

      const showDraftMessage = () => {
        console.log("test");
          if(house.current_phase != 'D'){
              console.log(1);
              return (<h3>A Draft is not currently going on.</h3>)
          }
          if(placement && (placement['user_id'] == userID)){
                console.log(2);
              return  (chores.map((chore) => (!chore.claimed) ? (<DraftChore key={chore.chore_id} claimed={chore.claimed} owner_name="Claim This"
              chore_id={chore.chore_id} name={chore.name} description={chore.description}/>) : null))
          }
          console.log(3);
          return (<h1>It is not your turn</h1>)
      }

    return (
        <div className="HouseList">
            {showDraftMessage()}
        </div>
    );
}
