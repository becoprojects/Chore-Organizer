import React from "react";
import {useHistory} from 'react-router-dom';
import '../../CSS/House.css';
import Cookies from 'js-cookie';
import {makeDraftPick} from '../../utils/apiUtils'

const DraftChore = (props) => {
  const userID = Cookies.get('id');
  let history = useHistory();

  const draftChore = () => {
    makeDraftPick(userID,props.chore_id).then((res) => {
      if(res === null){
        history.push("/errorscreen");
      }
      else{
        history.push("/chores");
      }
    });
  }

  return (
    <div className="OuterBorder">
        <div className="HouseSelect" onClick={draftChore}>
            <h1>{props.name}</h1>
            <p>{props.description}</p>
            <p>{props.claimed ? "Owner: " + props.owner_name : null}</p>
        </div>
    </div>
  );
}

export default DraftChore