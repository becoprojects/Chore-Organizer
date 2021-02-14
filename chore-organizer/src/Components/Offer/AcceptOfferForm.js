import React, { useState, useContext } from "react";
import { useHistory, useLocation} from 'react-router-dom';
import '../../CSS/OfferForm.css'
import Cookies from 'js-cookie';
import {ChoreContext} from '../../Contexts/ChoreContext'
import AcceptOfferItem from './AcceptOfferItem'
import AcceptOfferPlacement from './AcceptOfferPlacement'
import {OfferContext} from '../../Contexts/OfferContext'
import {PlacementContext} from '../../Contexts/PlacementContext'
import {HouseIDContext} from '../../Contexts/HouseIDContext'
import {acceptOffer, getOfferedChoresByOffer, rejectOffer, getOfferedPlacementsByOffer, getPlacementsByHouseandUser} from '../../utils/apiUtils'

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
    const [placements,setPlacements] = useContext(PlacementContext);
    const [offeredPlacements,setOfferedPlacements] = useState([]);
    const house = useContext(HouseIDContext)[0];
   
    React.useEffect(() => {
        let placements_temp = {'user':[],'other':[]}
        getOfferedChoresByOffer(offer.offer_id)
        .then((res) => {
            if(res === null){
                history.push("/errorscreen");
            }
            else{
                setOfferedChores(res);
            }
        });
        getOfferedPlacementsByOffer(offer.offer_id)
        .then((res) => {
            if(res === null){
                history.push("/errorscreen");
            }
            else{
                setOfferedPlacements(res);
            }
        });
        getPlacementsByHouseandUser(offer.house_id,offer.receiving_id)
        .then((res) => {
            if(res !== null){
                placements_temp.user = res;
            }
            getPlacementsByHouseandUser(offer.house_id,offer.asking_id)
            .then((res) => {
                if(res !== null){
                    placements_temp.other = res;
                }
                console.log(placements_temp);
                setPlacements(placements_temp);
            })
        });
      },[history, offer.offer_id,setPlacements]);


  const isChoreInOffer = (chore) => {
    let i = 0;
    for(i=0;i<offeredChores.length;i++){
        if(parseInt(offeredChores[i].chore_id) === parseInt(chore.chore_id)){
            return true;
        }
    }
    return false;
  }

  const isPlacementInOffer = (placement) => {
    let i = 0;
    for(i=0;i<offeredPlacements.length;i++){
        if(parseInt(offeredPlacements[i].placement_id) === parseInt(placement.placement_id)){
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

  const getIDPlacement = (id,person) => {
    let i = 0;
    if(person === 'user'){
        for(i=0;i<placements.user.length;i++){
            if(placements.user[i].placement_id === id){
                return i;
            }
        }
        return null;
    }
    if(person === 'other'){
        for(i=0;i<placements.other.length;i++){
            if(placements.other[i].placement_id === id){
                return i;
            }
        }
        return null;
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

  const rejectOfferFunc = () => {
    rejectOffer(offer.offer_id)
    .then((res) => {
      if(res === null){
          history.push("/errorscreen");
      }
      else{
          history.push("/chores");
      }
    });
}

  return (house.current_phase === 'D') ? (<h1>Offer cannot be accepted while a draft is ongoing</h1>) : (
    <div>
    <div className="grid-container">
        <div className="item-grid">
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === userID)  && (!isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)}/>) : null
            )}
            {placements.user.map((placement) => (!isPlacementInOffer(placement)) ? (<AcceptOfferPlacement futureCode={placement.future_code} place={placement.place}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === userID) && (isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
            {placements.user.map((placement) => (isPlacementInOffer(placement)) ? (<AcceptOfferPlacement futureCode={placement.future_code} place={placement.place}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === otherID) && (isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
            {placements.other.map((placement) => (isPlacementInOffer(placement)) ? (<AcceptOfferPlacement futureCode={placement.future_code} place={placement.place}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((chore.claimed) && (chore.owner_id === otherID) && (!isChoreInOffer(chore))) ? (<AcceptOfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
            {placements.other.map((placement) => (!isPlacementInOffer(placement)) ? (<AcceptOfferPlacement futureCode={placement.future_code} place={placement.place}/>) : null
            )}
        </div>
    </div>
    <button onClick={acceptOfferFunc}>Accept Offer</button>
    <button onClick={rejectOfferFunc} >Reject Offer</button>
    </div>
  );
}

export default AcceptOfferForm