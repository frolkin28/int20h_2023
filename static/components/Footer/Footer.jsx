import React from 'react';
import './style/style.css'
import linkedin from "../Pages/images/linkedin-image.png";

export const Footer = ()=>
{
    return (

            <div className="footer">
                <div className='footer-main'>
                    <div className='contact'>
                        <div className='footer-p'>Best team></div>
                    </div>

                    <div className='link-images'>
                        <a href='https://www.linkedin.com/'><img className='linkedin-image' src={linkedin} alt='T_T'/></a>
                    </div>
                </div>
            </div>

    );
}

export default Footer;
