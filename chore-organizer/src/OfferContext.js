import React, { useState, createContext } from "react";

export const OfferContext = createContext();

export const OfferProvider = (props) => {
    const [offer,setOffer] = useState([]);

    return(
        <OfferContext.Provider value={[offer,setOffer]}>
            {props.children}
        </OfferContext.Provider>
    );
}