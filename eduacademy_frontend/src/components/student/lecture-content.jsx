import React from 'react';
import { QuestionForm } from './QuestionForm';

export const Lecturecontent = () => {
  return (
    <div className='lecture-content'>
        <video width="750" height="500" controls >
           <source src="" type="video/mp4"/>
        </video>
        <QuestionForm />
    </div>
  )
}