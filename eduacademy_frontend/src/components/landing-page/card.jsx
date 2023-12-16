import React from 'react'

export const Cards = (props) => {
  return (
    <div className='card'>
        <img src={props.src} alt="image"></img>
        <div className='content'>
            <h5>{props.title}</h5>
            <p>{props.content}</p>
        </div>
    </div>
  )
}
