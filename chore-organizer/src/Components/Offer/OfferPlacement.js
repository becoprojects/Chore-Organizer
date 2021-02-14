import React, { useState, useContext } from "react";
import '../../CSS/OfferForm.css'
import {PlacementContext} from '../../Contexts/PlacementContext'

const OfferPlacement = (props) => { 
  const [placements,setPlacements] = useContext(PlacementContext);

  const select = () => {
      if(props.type === 'user'){
        let temp = {...placements};
        temp.user[props.id].selected = !temp.user[props.id].selected;
        setPlacements(temp);
      }
      else{
        let temp = {...placements};
        temp.other[props.id].selected = !temp.other[props.id].selected;
        setPlacements(temp);
      }
  }


  const renderPlacement = () => {
      if(Object.keys(placements).length !== 0){
          if(props.type === 'user'){
              return (<div className="offer-item" onClick={select}>
                        <p>{"Pick order: " + JSON.stringify(placements.user[props.id].place +1)}</p>
                        <p>{"Drafts in the future: " + JSON.stringify(placements.user[props.id].future_code)}</p>
                    </div>)
          }
          else{
              return(<div className="offer-item" onClick={select}>
                         <p>{"Pick order: " + JSON.stringify(placements.other[props.id].place+1)}</p>
                         <p>{"Drafts in the future: " + JSON.stringify(placements.other[props.id].future_code)}</p>
                    </div>)
          }
      }
      return (<h1>LOADING...</h1>);
  }

  return (
        <div>
            {renderPlacement()}
        </div>
  )
            
}

export default OfferPlacement