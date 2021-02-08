import React, { useState, createContext } from "react";

export const HouseContext = createContext();

export const HouseProvider = (props) => {
    const [houseList,setHouseList] = useState([]);

    return(
        <HouseContext.Provider value={[houseList,setHouseList]}>
            {props.children}
        </HouseContext.Provider>
    );
}