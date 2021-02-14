import React, { useState, useContext } from "react";
import {useHistory} from 'react-router-dom';
import Cookies from 'js-cookie';
import HouseMember from './HouseMember'
import '../../CSS/App.css'
import {getUsersByHouse,getOffersbyHouseandUser} from '../../utils/apiUtils'
import {HouseIDContext} from '../../Contexts/HouseIDContext'

export default function HouseMemberList() {
    let history = useHistory();
    const [houseMemberList,setHouseMemberList] = useState([]);
    const [offerList,setOfferList] = useState([]);
    const houseID = useContext(HouseIDContext)[0].house_id;

    React.useEffect(() => {
        const userID = Cookies.get("id");
        getUsersByHouse(houseID)
        .then((res) => {
            if(res === null){
                history.push("/errorscreen");
            }
            else{
                setHouseMemberList(res);
            }
        });
        
        getOffersbyHouseandUser(houseID,userID)
        .then((res) => {
            if(res !== null){
                setOfferList(res);
            }
        });

      }, [history,houseID]);

    const offerPending = (houseMember) => {
        //console.log(offerList);
        const id = parseInt(houseMember.user_id);
        let i = 0;
        for(i=0;i<offerList.length;i++){
            if(parseInt(offerList[i].asking_id) === id){
                return (<HouseMember key={houseMember.user_id} full_offer={offerList[i]} houseMember_id={houseMember.user_id} offer="asking" name={houseMember.name}/>)
            }
            if(parseInt(offerList[i].receiving_id) === id){
                return (<HouseMember key={houseMember.user_id} full_offer={offerList[i]} houseMember_id={houseMember.user_id} offer="receiving" name={houseMember.name}/>)
            }
        }
        return (<HouseMember key={houseMember.user_id} full_offer={offerList[i]} houseMember_id={houseMember.user_id} offer="none" name={houseMember.name}/>)
    }

    return (
        <div className="HouseList">
            {houseMemberList.map((houseMember) => !(parseInt(Cookies.get('id')) === parseInt(houseMember.user_id)) ?
             offerPending(houseMember)
             : null)}
        </div>
    );
}
