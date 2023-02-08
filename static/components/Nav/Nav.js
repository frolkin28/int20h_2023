import './style/Nav.css';
import logo from './images/logo.png';

import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

import { useUser } from '../../context/UserContext';

function Nav() {
    const [name, setName] = useState("");
    const location = useLocation();
    const searchBy = location.pathname.includes("ingredients") ? "ingredients" : "recipes";
    const { user, setUserId } = useUser();
    const onLogoutClick = (e) => {
        e.preventDefault();
        fetch("/auth/logout", {
            method: "POST"
        })
            .then((response) => response.json())
            .then((data) => {
                if (data?.status !== "success") setUserId(null);
            });
    }

    return (
        <nav className="navbar navbar-expand-lg nav">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">
                    <Link to='/' className='logo-block'>
                        <img className='navbar-brand logo' src={logo} alt='T_T' />
                    </Link>
                </a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse padding" id="navbarTogglerDemo02">
                    <ul className='navbar-nav me-auto mb-2 mb-lg-0 size'>
                        <li className='nav-item mr'><Link className='nav-link text-dark' to='/'>Home</Link></li>
                        <li className='nav-item'><Link className='nav-link text-dark' to='/ingredients'>Ingredients</Link></li>
                        {
                            user ? (
                                <>
                                    <li className='nav-item'>
                                        <Link className='nav-link text-dark' to='/user'>User</Link>
                                    </li>
                                    <li className='nav-item'>
                                        <a href='/' className='nav-link text-dark' onClick={onLogoutClick}>Logout</a>
                                    </li>
                                </>

                            ) : (
                                <>
                                    <li className='nav-item'>
                                        <Link
                                            className='nav-link text-dark'
                                            to={"/login"}
                                        >
                                            Login
                                        </Link>
                                    </li>
                                    <li className='nav-item'>
                                        <Link
                                            className='nav-link text-dark'
                                            to={"/register"}
                                        >
                                            Register
                                        </Link>
                                    </li>
                                </>

                            )
                        }
                    </ul>
                    <form className="d-flex right" role="search" action={`/recipes/search/${searchBy}/${name}`}>
                        <input className="form-control me-2" type='text'
                            placeholder={"Search by " + searchBy}
                            value={name}
                            onChange={e => setName(e.target.value)}
                            aria-label="Search"
                        />
                        <button className="btn btn-outline-success" type="submit">Search</button>
                    </form>
                </div>
            </div>
        </nav>
    );
}

export default Nav;
