import './style/NoContentPage.css';
import React from 'react';

function LoadingPage()
{
    return(
        <div className='home-page loading-page'>
            <div className='message' id='message'>Loading</div>
            <div className='message' id='message'>Please wait</div>
        </div>
    );
}

export default LoadingPage;
