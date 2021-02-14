import React, { useState, createContext } from "react";

export const AcceptPlacementContext = createContext();

export const AcceptPlacementProvider = (props) => {
    const [placements,setPlacements] = useState([]);

    return(
        <AcceptPlacementContext.Provider value={[placements,setPlacements]}>
            {props.children}
        </AcceptPlacementContext.Provider>
    );
}