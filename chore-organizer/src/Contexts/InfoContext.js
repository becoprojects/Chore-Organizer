import React, {useState, createContext} from 'react';

export const InfoContext = createContext();

export const InfoProvider = props => {
    const [currentUser, setCurrentUser] = useState(0);


    return(
        <InfoContext.Provider value={[currentUser, setCurrentUser]}>
            {props.children}
        </InfoContext.Provider>
    );
}