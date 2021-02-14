import React, { useState, createContext } from "react";

export const PlacementContext = createContext();

export const PlacementProvider = (props) => {
    const [placements,setPlacements] = useState({'user':[],'other':[]});

    return(
        <PlacementContext.Provider value={[placements,setPlacements]}>
            {props.children}
        </PlacementContext.Provider>
    );
}