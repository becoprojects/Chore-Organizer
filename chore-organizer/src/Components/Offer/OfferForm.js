import React, { useState, useContext} from "react";
import {useHistory, useLocation} from 'react-router-dom';
import '../../CSS/OfferForm.css'
import Cookies from 'js-cookie';
import {ChoreContext} from '../../Contexts/ChoreContext'
import OfferItem from './OfferItem'
import {makeOffer} from "../../utils/apiUtils"
import {DragDropContext,Droppable,Draggable} from 'react-beautiful-dnd'

function useQuery() {
    return new URLSearchParams(useLocation().search);
  }

const OfferForm = (props) => {
    let history = useHistory();
    const [chores,setChores] = useContext(ChoreContext);
    const columnList = {
        'c1':{
            name: 'C1',
            items: chores
        },
        'c2':{
            name: 'C2',
            items: []
        }
    }

    const {userID, otherID} = useState({
        userID:parseInt(Cookies.get('id')), 
        otherID:parseInt(useQuery().get("offerto"))
    })[0];
    const [columns, setColumns] = useState(columnList);
  
  const getID = (id) => {
      let i = 0;
      for(i=0;i<chores.length;i++){
          if(chores[i].chore_id === id){
              return i;
          }
      }
      return null;
  }

  const anySelected = () => {
      let i = 0;
      for(i=0;i<chores.length;i++){
          if(chores[i].selected === true){
            return true;
          }
      }
      return false;
  }

  const submitOffer = () => {
    let i = 0;
    let tempChores = [];
    for(i=0;i<chores.length;i++){
        if(chores[i].selected === true){
            tempChores.push(chores[i].chore_id);
        }
    }
    const houseID = Cookies.get("currentHouseID");
    makeOffer(houseID,userID,otherID,tempChores)
        .then((res) => {
            if(res === null){
                history.push("/errorpage");
            }   
            else{
                history.push("/chores");
            }
        });
    }

    const onDragEnd = (result,columns,setColumns) => {
        if(!result.destination){return;}
        const {source,destination} = result;
        if(source.droppableId !== destination.droppableId){
            const sourceColumn = columns[source.droppableId];
            const destColumn = columns[destination.droppableId];
            const sourceItems = [...sourceColumn.items];
            const destItems = [...destColumn.items];
            const [removed] = sourceItems.splice(source.index,1);
            destItems.splice(destination.index,0,removed);
            setColumns({
                ...columns,
                [source.droppableId]:{
                    ...sourceColumn,
                    items: sourceItems
                },
                [destination.droppableId]: {
                    ...destColumn,
                    items: destItems
                }
            })
        }
        else{
            const column = columns[source.droppableId];
            const copiedItems = [...column.items]
            const [removed] = copiedItems.splice(source.index, 1);
            copiedItems.splice(destination.index,0,removed);
            setColumns({...columns,[source.droppableId]:{
                ...column,
            items: copiedItems
        }})
        }
        
    }

  return(
      <div style={{display:"flex", justifyContent:"center", height:"100%"}}>
          <DragDropContext onDragEnd={result => onDragEnd(result,columns,setColumns)}>
            {Object.entries(columns).map(([id,column]) => {
                return (
                    <Droppable droppableId={id}>
                        {(provided,snapshot) => {
                            return (<div 
                                    {...provided.droppableProps}
                                    ref={provided.innerRef}
                                    style={{
                                        background: snapshot.isDraggingOver ? 'lightblue' : 'lightgrey',
                                        padding: 4,
                                        width: 250,
                                        minHeight: 500
                                    }}>
                                        {column.items.map((item,index) => {
                                            return(
                                                <Draggable key={JSON.stringify(item.chore_id)} draggableId={JSON.stringify(item.chore_id)} index={index}>
                                                    {(provided,snapshot) => {
                                                        return(<div ref={provided.innerRef}
                                                                {...provided.draggableProps}
                                                                {...provided.dragHandleProps}
                                                                style={{
                                                                    userSelect: 'none',
                                                                    padding: 16,
                                                                    margin: '0 0 8px 0',
                                                                    minHeight: '50px',
                                                                    backgroundColor: snapshot.isDragging ? '#263B4A' : '#456C86',
                                                                    color: 'white',
                                                                    ...provided.draggableProps.style
                                                                }}>
                                                                    {item.name}
                                                                </div>);
                                                    }}
                                                </Draggable>
                                            );
                                        })}
                                        {provided.placeholder}
                                    </div>);
                        }}
                    </Droppable>
                );
            })}
          </DragDropContext>
      </div>
  );

  return (
    <div>
    <div>
        <div>
            {chores.map((chore) => (!chore.selected&& chore.claimed && chore.owner_id === userID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div>
            {chores.map((chore) => (chore.selected && chore.claimed && chore.owner_id === userID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div>
            {chores.map((chore) => (chore.selected && chore.claimed && chore.owner_id === otherID) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
        <div>
            {chores.map((chore) => ((!chore.selected) && (chore.claimed) && (chore.owner_id === otherID)) ? (<OfferItem id={getID(chore.chore_id)} value={[chores,setChores]}/>) : null
            )}
        </div>
    </div>
    <button disabled={!anySelected()} onClick={submitOffer}>Make Offer</button>
    </div>
  );
}

export default OfferForm