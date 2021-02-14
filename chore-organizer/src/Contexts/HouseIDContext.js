import React, { useState, createContext } from "react";

export const HouseIDContext = createContext();

export const HouseIDProvider = (props) => {
    const [houseID,setHouseID] = useState({});

    return(
        <HouseIDContext.Provider value={[houseID,setHouseID]}>
            {props.children}
        </HouseIDContext.Provider>
    );
}