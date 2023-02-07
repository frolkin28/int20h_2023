import './style/Home.css';
import React from 'react';
import UserDetails from "../User/UserDetails";

function User()
{
    return(
        <div className='home-page'>
            <UserDetails />
        </div>
    )
}

export default User;