import React, { useContext } from "react";
import {useHistory} from 'react-router-dom';
import '../../CSS/House.css'
import {OfferContext} from '../../Contexts/OfferContext'

const HouseMember = (props) => {
  let history = useHistory();;
  const setOffer = useContext(OfferContext)[1];

  const goToOffer = (msg) => {
    if(msg === "asking"){
      setOffer(props.full_offer);
      history.push({
        pathname:"/acceptoffer",
        search: "offerto=" + props.houseMember_id
      });;
    }
    if(msg === "none"){
      history.push({
        pathname:"/makeoffer",
        search: "offerto=" + props.houseMember_id
      });;
    }
  }

  const getOfferMessage = (msg) => {
    if(msg === "asking"){
      return "Offer waiting for you";
    }
    if(msg === "receiving"){
      return "Offer has not been received";
    }
    if(msg === "none"){
      return "Click to make offer";
    }
  }

  const canMakeOffer = (msg) => {
    if(msg === "asking"){
      return true;
    }
    if(msg === "receiving"){
      return false;
    }
    if(msg === "none"){
      return true;
    }
  }

  return canMakeOffer(props.offer) ? (
    <div className="OuterBorder">
        <div className="HouseSelect" onClick={() => goToOffer(props.offer)}>
            <h3>{props.name}</h3>
            <h3>{getOfferMessage(props.offer)}</h3>
        </div>
    </div>
  ) :
  (
    <div className="OuterBorder">
        <div className="OfferCantSelect">
            <h3>{props.name}</h3>
            <h3>{getOfferMessage(props.offer)}</h3>
        </div>
    </div>
  );
}

export default HouseMember