import React from "react";
import './CSS/House.css'

const Chore = (props) => {

  return (
    <div className="OuterBorder">
        <div className="HouseSelect">
            <h1>{props.name}</h1>
            <p>{props.description}</p>
            <p>{props.claimed ? "Owner: " + props.owner_name : null}</p>
        </div>
    </div>
  );
}

export default Chore