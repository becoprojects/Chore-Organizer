import React, { useState, useContext, useEffect} from "react";
import {useHistory, useLocation} from 'react-router-dom';
import '../../CSS/OfferForm.css'
import Cookies from 'js-cookie';
import {ChoreContext} from '../../Contexts/ChoreContext'
import {HouseIDContext} from '../../Contexts/HouseIDContext'
import OfferItem from './OfferItem'
import {makeOffer, getPlacementsByHouseandUser} from "../../utils/apiUtils"
import OfferPlacement from './OfferPlacement'
import {PlacementContext} from '../../Contexts/PlacementContext'

function useQuery() {
    return new URLSearchParams(useLocation().search);
  }

const OfferForm = () => {
    let history = useHistory();
    const [chores,setChores] = useContext(ChoreContext);
    const {userID, otherID} = useState({
        userID:parseInt(Cookies.get('id')), 
        otherID:parseInt(useQuery().get("offerto"))
    })[0];
    const house = useContext(HouseIDContext)[0];
    const houseID = house.house_id;
    const [placements,setPlacements] = useContext(PlacementContext);

  useEffect(() => {
    const placements_temp = {user:[],other:[]}
    getPlacementsByHouseandUser(houseID,userID).then((res) => {
        if(res === null){
            history.push("/errorscreen");
        }
        else{
            let i=0;
            for(i=0;i<res.length;i++){
                res[i]['selected'] = false;
            }
            placements_temp.user = res;
        }
        getPlacementsByHouseandUser(houseID,otherID).then((res) => {
            if(res === null){
                history.push("/errorscreen");
            }
            else{
                let i=0;
                for(i=0;i<res.length;i++){
                    res[i]['selected'] = false;
                }
                placements_temp.other = res;
            }
            setPlacements(placements_temp);
        });
    });
    
  },[setPlacements]);
  
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

  const anySelected = () => {
      let i = 0;
      for(i=0;i<chores.length;i++){
          if(chores[i].selected === true){
            return true;
          }
      }
      for(i=0;i<placements.user.length;i++){
          if(placements.user[i].selected === true){
              return true;
          }
      }
      for(i=0;i<placements.other.length;i++){
        if(placements.other[i].selected === true){
            return true;
        }
    }
      return false;
  }

  const submitOffer = () => {
    let i = 0;
    let tempChores = [];
    let tempPlacements = []
    for(i=0;i<chores.length;i++){
        if(chores[i].selected === true){
            tempChores.push(chores[i].chore_id);
        }
    }
    for(i=0;i<placements.user.length;i++){
        if(placements.user[i].selected === true){
            tempPlacements.push(placements.user[i].placement_id);
        }
    }
    for(i=0;i<placements.other.length;i++){
        if(placements.other[i].selected === true){
            tempPlacements.push(placements.other[i].placement_id);
        }
    }
    const houseID = Cookies.get("currentHouseID");
    makeOffer(houseID,userID,otherID,tempChores,tempPlacements)
        .then((res) => {
            if(res === null){
                history.push("/errorpage");
            }   
            else{
                history.push("/chores");
            }
        });
    }

  return (house.current_phase === 'D') ? (<h1>Cannot make an offer while a Draft is in progress</h1>) : (
    <div>
        {console.log(house)}
    <div className="grid-container">
        <div className="item-grid">
        {chores.map((chore) => (!chore.selected&& chore.claimed && chore.owner_id === userID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
        )}
        {placements.user.map((placement) => (!placement.selected) ? (<OfferPlacement type='user' id={getIDPlacement(placement.placement_id,'user')} value={[placements,setPlacements]}/>) : null
            )}
            
        </div>
        <div className="item-grid">
            {chores.map((chore) => (chore.selected && chore.claimed && chore.owner_id === userID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
            {placements.user.map((placement) => (placement.selected) ? (<OfferPlacement type='user' id={getIDPlacement(placement.placement_id,'user')} value={[placements,setPlacements]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => (chore.selected && chore.claimed && chore.owner_id === otherID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
            {placements.other.map((placement) => (placement.selected) ? (<OfferPlacement type='other' id={getIDPlacement(placement.placement_id,'other')} value={[placements,setPlacements]}/>) : null
            )}
        </div>
        <div className="item-grid">
            {chores.map((chore) => ((!chore.selected) && (chore.claimed) && (chore.owner_id === otherID)) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
            {placements.other.map((placement) => (!placement.selected) ? (<OfferPlacement type='other' id={getIDPlacement(placement.placement_id,'other')} value={[placements,setPlacements]}/>) : null
            )}
        </div>
    </div>
    <button disabled={!anySelected()} onClick={submitOffer}>Make Offer</button>
    </div>
  );
}

export default OfferForm