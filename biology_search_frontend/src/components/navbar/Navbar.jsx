import React, { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import "./Navbar.scss"

const Navbar = () => {

    const [active,setActive] = useState(false)
    const [open,setOpen] = useState(false)

    const {pathname} = useLocation()

    const isActive = () => {
        window.scrollY > 0 ? setActive(true) : setActive(false)
    }


    useEffect(() => {
        window.addEventListener("scroll", isActive);

        return () => {
            window.removeEventListener("scroll",isActive)
        }
    },[])

    // ideally this would be with some sort of database 
    // but for now it's just hard coded 

    const currentUser = {
        id: 1,
        username: "Derek",
        email: ""
    }

  return (
    <div className={active || pathname !=="/" ? "navbar active" : "navbar"}>
        <div className="container">
            <div className="logo">
                <Link to="/" className="link">
                <span className="text">Biology Search Tool</span>
                </Link>
            </div>
            <div className="links">
                <span>Explore Data</span>
                <span>Query Database</span>
                <span>Collected Documents</span>
                {/* <span>Sign in</span> */}
                {!currentUser?.isResearcher && <span>Researcher</span>}
                {!currentUser && <button>Join</button>}
                {currentUser && (
                    <div className="user" onClick={()=>setOpen(!open)}>
                        <img src="https://i.pinimg.com/564x/f5/ec/14/f5ec1493f8cf15a2f2d017ac9afe628d.jpg" alt="" />
                        <span>{currentUser.username}</span>
                        {open && <div className="options">
                            {
                                currentUser.isResearcher && (
                                    <>
                                    <Link className="link" to="/upload">Upload Personal Data</Link>
                                    <Link className="link" to="llm">Choose LLM Settings</Link>
                                    </>
                            )}
                            <Link className="link" to="/queries">Queries</Link>
                            <Link className="link" to="/documents">Documents of Interest</Link>
                            <Link className="link" to="/">Logout</Link>
                            
                        </div>}
                    </div>
                )}
            </div>
        </div>
        {(active || pathname !=="/") && (
        <>
            <hr />
            <div className="menu">
                {/* <span>Test1</span>
                <span>Test2</span> */}
            </div>
        </>
        )}
    </div>
  )
}

export default Navbar