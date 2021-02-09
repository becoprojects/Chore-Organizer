import React, { useContext } from "react";
import '../../CSS/OfferForm.css'
import {ChoreContext} from '../../Contexts/ChoreContext'

const AcceptOfferItem = (props) => { 
    
  const chores = useContext(ChoreContext)[0];

  return (
        <div className="accept-offer-item">
            <p>{chores[props.id].name}</p>
            <p>{chores[props.id].description}</p>
        </div>
  )
}

export default AcceptOfferItem