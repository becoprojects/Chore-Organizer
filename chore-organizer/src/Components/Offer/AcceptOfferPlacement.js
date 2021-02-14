import React, { useContext,useEffect } from "react";
import '../../CSS/OfferForm.css'
import {PlacementContext} from '../../Contexts/PlacementContext'

const AcceptOfferItem = (props) => { 

  return (
    <div className="accept-offer-item">
        <p>{"Pick order: " + JSON.stringify(parseInt(props.place)+1)}</p>
        <p>{"Drafts in the future: " + JSON.stringify(props.futureCode)}</p>
    </div>
  )
}

export default AcceptOfferItem