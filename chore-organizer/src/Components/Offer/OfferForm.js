import React, { useState, useContext} from "react";
import {useHistory, useLocation} from 'react-router-dom';
import '../../CSS/OfferForm.css'
import Cookies from 'js-cookie';
import {ChoreContext} from '../../Contexts/ChoreContext'
import OfferItem from './OfferItem'
import {makeOffer} from "../../utils/apiUtils"

function useQuery() {
    return new URLSearchParams(useLocation().search);
  }

const OfferForm = (props) => {
    let history = useHistory();
    const [chores,setChores] = useContext(ChoreContext);
    const {userID, otherID} = useState({
        userID:parseInt(Cookies.get('id')), 
        otherID:parseInt(useQuery().get("offerto"))
    })[0];
  
  const getID = (id) => {
      let i = 0;
      for(i=0;i<chores.length;i++){
          if(chores[i].chore_id === id){
              return i;
          }
      }
      return null;
  }

  const anySelected = () => {
      let i = 0;
      for(i=0;i<chores.length;i++){
          if(chores[i].selected === true){
            return true;
          }
      }
      return false;
  }

  const submitOffer = () => {
    let i = 0;
    let tempChores = [];
    for(i=0;i<chores.length;i++){
        if(chores[i].selected === true){
            tempChores.push(chores[i].chore_id);
        }
    }
    const houseID = Cookies.get("currentHouseID");
    makeOffer(houseID,userID,otherID,tempChores)
        .then((res) => {
            if(res === null){
                history.push("/errorpage");
            }   
            else{
                history.push("/chores");
            }
        });
    }

  return (
    <div>
    <div className="grid-container">
        <div className="item-grid">
            {chores.map((chore) => (!chore.selected&& chore.claimed && chore.owner_id === userID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => (chore.selected && chore.claimed && chore.owner_id === userID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => (chore.selected && chore.claimed && chore.owner_id === otherID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((!chore.selected) && (chore.claimed) && (chore.owner_id === otherID)) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
    </div>
    <button disabled={!anySelected()} onClick={submitOffer}>Make Offer</button>
    </div>
  );
}

export default OfferForm