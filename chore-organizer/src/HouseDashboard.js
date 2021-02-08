import React from "react";
import './CSS/App.css'
import ChoreList from './ChoreList'
import HouseMemberList from './HouseMemberList'

export default function HouseDashboard() {

    return (
        <div>
           <ChoreList />
           <HouseMemberList />
        </div>
    );
}
