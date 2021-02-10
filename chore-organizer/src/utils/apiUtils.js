import axios from 'axios'

const base = 'http://192.168.2.25:5000';

export async function getHouseByUser(userID){
    try{
        const res = await axios.get(base + "/gethousesbyuser/" + userID);
        if(res.status === 200){
            return res.data.response;
        }   
        else{
            return null;
        }
    }
    catch(Exception){
        return null;
    }
}

export async function getChoresByHouse(houseID){
    try{
        const res = await axios.get(base + "/getchoresbyhouse/" + houseID)
        if(res.status === 200){
            let i = 0;
            let choreList = res.data.response
            for(i=0;i<choreList.length;i++){
                choreList[i].selected = false;
            }
            console.log(choreList);
            return choreList;
        }   
        else{
            console.log("error: " + res);
            return null;
        }
    }
    catch(Exception){
        return null;
    }
}

export async function getUsersByHouse(houseID){
    try{
        const res = await axios.get(base + "/getusersbyhouse/" + houseID)
        if(res.status === 200){
            return res.data.response;
        }   
        else{
            return null;
        }
    }
    catch(Exception){
        return null;
    }
}

export async function getOffersbyHouseandUser(houseID,userID){
    try{
        const res = await axios.get(base + "/getoffersbyhouseanduser/" + houseID + "/" + userID);
        if(res.status === 200){
            return res.data.response;
        }   
        else{
            return null;
        }
    }
    catch(Exception){
        return null;
    }
}

export async function makeOffer(houseID,askingID,receivingID,chores){
    let json_input = {
        'house_id':parseInt(houseID),
        'asking_id':parseInt(askingID),
        'receiving_id':parseInt(receivingID),
        'chores':chores,
        'placements':[]}
        console.log(json_input);
    try{
        const res = await axios.post(base + "/addoffer",json_input);
        if(res.status === 200){
            return res.data.response;
        }   
        else{
            console.log(res);
            return null;
        }
    }
    catch(Exception){
        console.log(Exception);
        return null;
    }
        
}

export async function acceptOffer(offerID){
    try{
        const res = await axios.post(base + "/acceptoffer/" + offerID);
        if(res.status === 200){
            return res.data.response;
        }   
        else{
            return null;
        }
    }
    catch(Exception){
        return null;
    }
}

export async function getOfferedChoresByOffer(offerID){
    try{
        const res = await axios.get(base + "/getofferedchoresbyoffer/" + offerID);
        if(res.status === 200){
            return res.data.response;
        }   
        else{
            return null;
        }
    }
    catch(Exception){
        return null;
    }
}

export async function rejectOffer(offerID){
    try{
        const res = await axios.delete(base + "/rejectoffer/" + offerID);
        if(res.status === 200){
            return res.data;
        }   
        else{
            return null;
        }
    }
    catch(Exception){
        return null;
    }
}
