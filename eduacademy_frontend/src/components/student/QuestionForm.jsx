import React from 'react'
import { useState } from 'react';

export const QuestionForm = (isQuestion) => {
    const [text, setText] = useState('');
    const [textareaHeight, setTextareaHeight] = useState('50px');

    const handleTextareaChange = (event) => {
      setText(event.target.value);
      // Adjust textarea height based on content
      setTextareaHeight(`${event.target.scrollHeight}px`);
    };
  
    return (
      <form onSubmit={(event)=>{
        event.preventDefault();
        setText('');
      }} className='wrapper'>
        <textarea
            value={text}
            onChange={handleTextareaChange}
            style={{ height: textareaHeight }}
            placeholder='write your question .....'
            autoFocus
        />
        <button>{isQuestion ? 'Ask' : 'Answer'}</button>
      </form>
    );
  };
