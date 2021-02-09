import React, { useState, useContext } from "react";
import { useHistory, useLocation} from 'react-router-dom';
import '../../CSS/OfferForm.css'
import Cookies from 'js-cookie';
import {ChoreContext} from '../../Contexts/ChoreContext'
import AcceptOfferItem from './AcceptOfferItem'
import {OfferContext} from '../../Contexts/OfferContext'
import {acceptOffer, getOfferedChoresByOffer} from '../../utils/apiUtils'

function useQuery() {
    return new URLSearchParams(useLocation().search);
  }

const AcceptOfferForm = (props) => {
    let history = useHistory();
    const [chores,setChores] = useContext(ChoreContext);
    const {userID, otherID} = useState({
        userID:parseInt(Cookies.get('id')), 
        otherID:parseInt(useQuery().get("offerto"))
    })[0];
    const offer = useContext(OfferContext)[0];
    const [offeredChores,setOfferedChores] = useState([]);
   

    React.useEffect(() => {
        getOfferedChoresByOffer(offer.offer_id)
        .then((res) => {
            if(res === null){
                history.push("/errorscreen");
            }
            else{
                setOfferedChores(res);
            }
        });
      },[history, offer.offer_id]);


  const isChoreInOffer = (chore) => {
    let i = 0;
    for(i=0;i<offeredChores.length;i++){
        if(parseInt(offeredChores[i].chore_id) === parseInt(chore.chore_id)){
            return true;
        }
    }
    return false;
  }
  
  const getID = (id) => {
      let i = 0;
      for(i=0;i<chores.length;i++){
          if(chores[i].chore_id === id){
              return i;
          }
      }
      return null;
  }

  const acceptOfferFunc = () => {
      acceptOffer(offer.offer_id)
      .then((res) => {
        if(res === null){
            history.push("/errorscreen");
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
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === userID)  && (!isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === userID) && (isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === otherID) && (isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === otherID) && (!isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
    </div>
    <button onClick={acceptOfferFunc}>Accept Offer</button>
    </div>
  );
}

export default AcceptOfferForm