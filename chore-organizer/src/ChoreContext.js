import React, { useState, createContext } from "react";

export const ChoreContext = createContext();

export const ChoreProvider = (props) => {
    const [chores,setChores] = useState([]);

    return(
        <ChoreContext.Provider value={[chores,setChores]}>
            {props.children}
        </ChoreContext.Provider>
    );
}