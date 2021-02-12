import React, { useContext } from "react";
import '../../CSS/OfferForm.css'
import {ChoreContext} from '../../Contexts/ChoreContext'

const OfferItem = (props) => { 
    
  const [chores,setChores] = useContext(ChoreContext);

  const select = () => {
      let temp = [...chores];
      temp[props.id].selected = !temp[props.id].selected;
      setChores(temp);
  }

  return (
        <div className="offer-item" onClick={select}>
            <p>{chores[props.id].name}</p>
            <p>{chores[props.id].description}</p>
        </div>
  )
}

export default OfferItem