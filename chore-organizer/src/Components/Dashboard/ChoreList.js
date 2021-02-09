import React, { useState, useContext } from "react";
import {useHistory} from 'react-router-dom';
import Cookies from 'js-cookie';
import Chore from './Chore'
import '../../CSS/App.css'
import {ChoreContext} from '../../Contexts/ChoreContext'
import {getChoresByHouse} from '../../utils/apiUtils'
import {HouseIDContext} from '../../Contexts/HouseIDContext'

export default function ChoreList() {
    let history = useHistory();
    const [chores,setChores] = useContext(ChoreContext);
    const houseID = useContext(HouseIDContext)[0];
    const userID = useState(parseInt(Cookies.get("id")))[0];

    React.useEffect(() => {
        getChoresByHouse(houseID).then((res) => {
            if(res === null){
                history.push("/errorscreen");
            }
            else{
                setChores(res);
            }
        });
      }, [history,setChores,houseID]);

    return (
        <div className="HouseList">
            {chores.map((chore) => ((parseInt(chore.owner_id)===userID) && chore.claimed) ? (<Chore key={chore.chore_id} claimed={chore.claimed} owner_name={chore.owner_name}
                                        chore_id={chore.chore_id} name={chore.name} description={chore.description}/>) : null
            )}
        </div>
    );
}
