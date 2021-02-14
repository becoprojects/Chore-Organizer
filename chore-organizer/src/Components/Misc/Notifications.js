import React, {useEffect, useState} from "react";
import {useHistory} from 'react-router-dom';
import '../../CSS/Nav.css'
import {Dropdown, NavItem, NavLink} from 'react-bootstrap'
import {getUnseenNotificationsByUser,setSeenNotifications} from '../../utils/apiUtils'
import Cookies from 'js-cookie';

const Notifications = () => {
    const [notifications, setNotifications] = useState([]);
    const [seen, setSeen] = useState(false);
    let history = useHistory();

    useEffect(() => {
        const userID = Cookies.get('id');
        getUnseenNotificationsByUser(userID).then((res) => {
            if(res !== null){
                setNotifications(res);
            }
        });
    },[])

    const viewNotifications = () => {
        if(!seen && notifications.length > 0){
            let i=0;
            let data = {'notification_id_list':[]}
            for(i=0;i<notifications.length;i++){
                data['notification_id_list'].push(notifications[i].notification_id);
            }
            setSeenNotifications(data).then((res) => {
                if(res === null){
                    history.push("/errorscreen");
                }
                else{
                    setSeen(true);
                }
            })
        }
    }

    return (
        <div className="NotificationDiv">
            <Dropdown as={NavItem} onClick={viewNotifications}>
                <Dropdown.Toggle as={NavLink}>
                    {((notifications.length > 0) && (seen === false)) ? (<img src={process.env.PUBLIC_URL + '/notification-bell-on.png'} alt="Notifications" width="50" height="50"/>) :
                        (<img src={process.env.PUBLIC_URL + '/notification-bell.png'} alt="Notifications" width="50" height="50"/>)}
                </Dropdown.Toggle>
                
                <Dropdown.Menu>
                    {notifications.map((notification) => (
                    <Dropdown.Item>
                        <div>
                            <h1>{notification.title}</h1>
                            <h3>{notification.description}</h3>
                        </div>
                    </Dropdown.Item>))}
                </Dropdown.Menu>
            </Dropdown>
           
        </div>
        
    );
}

export default Notifications;