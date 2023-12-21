import React from 'react'
import green from '../Assets/green.png'
import leaderboard from '../Assets/leaderboard.png'
import books from '../Assets/books.png'
import { Footer } from './footer';
import video from '../Assets/video.png';
import QA from '../Assets/QA.png';
import quiz from '../Assets/quiz.png';
import { Cards } from './card';


export const About = () => {
  return (
    <>
    <div className='container cont1'>
        <div className='p1'>
            <h1>Welcome to, EDU Academy</h1>
            <p>where learning knows no bounds! Access high-quality courses offered by educators spanning every corner of Egypt, while students earn points for unlocking additional content. Engage, learn, and grow within a community that values your feedback about courses andteachers and enjoy your first class on us!</p>
            <button className='join-us btn'>Join us now !</button>
        </div>
        <img src={green} alt="students' image" className="mission" />
    </div>

    <div className='container cont2'>
        <img src={QA} alt="students' image" className="mission" id='cont2'/>
        <div className='p1'>
            <h1>QAs Section</h1>
            <p> Allows students to ask, answer questions and upvote answers.
              Students earn points for upvoted answers and receive an additional points if his answer was correct,
              fostering a collaborative and incentivized learning environment.
              <br></br>This system encourages active participation and rewards accurate contributions.</p>
        </div>
    </div>
    <div className='container'>
        <Cards src={quiz} title="lecture Quizzes" content="Every lecture is provided with a quiz." />
        <Cards src={video}  title="Video Lectures" content="Comprehensive video lectures enhance remote education." />
        <Cards src={books} title="Freemium Approach" content="The first lecture of each course is free !" />
    </div>

    <div className='container about leader'>
        <div className='p1'>
            <h1>Leader Board</h1>
            <p>The Leaderboard recognizes and honors top-performing students on the platform based on their accumulated points. As students actively participate,
               contribute, and excel, they earn points, with the highest achievers showcased on the Leaderboard. 
               This gamified element encourages healthy competition and rewards academic excellence within the educational community.</p>
            
        </div>
        <img src={leaderboard} alt="students' image" className="mission" />
    </div>
    
    <Footer />
    </>
  )
}
