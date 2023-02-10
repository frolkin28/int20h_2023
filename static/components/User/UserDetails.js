import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import LoadingPage from '../Pages/LoadingPage';
import Page404 from '../Pages/Page404';

import { useUser } from '../../context/UserContext';

function UserDetails(props) {
    const { user } = useUser();
    const [loading, setLoading] = useState(true);

    setTimeout(() => setLoading(false), 5000);

    return (
        <>
            {/*{loading === true ? (*/}
            {/*    <LoadingPage />*/}
            {/*) : loading === false && user === null && ingredients.length === 0 ? (*/}
            {/*    <Page404 />*/}
            {/*) : (*/}
            <div className='home-page ingredients' id='ingredients'>
                {user ? (
                    <>
                        <div className='ingredients-declaration'>HELLO</div>
                        <div className='ingredients-declaration'>first_name : {user.first_name}</div>
                        <div className='ingredients-declaration'>last_name : {user.last_name}</div>
                    </>

                ) : (
                    <div className='ingredients-declaration'>HELLO</div>
                )}
            </div>
        </>
    );
}

export default UserDetails;
