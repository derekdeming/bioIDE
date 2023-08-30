import "./app.scss";
import { createBrowserRouter, Outlet, RouterProvider } from "react-router-dom";
import React from 'react'
import Home from "./pages/home/Home";
import Navbar from './components/navbar/Navbar'
import Footer from "./components/footer/Footer";
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";


function App() {
    const Layout = () => {
        return (
            <div className="app"> 
                <Navbar />
                <Outlet />
                <Footer />
            </div>
    );
    }; 

    const router = createBrowserRouter([
        {
            path: "/",
            element: <Layout />,
            children: [
                { path: "/", element: <Home/> },
                { path: "/explore", element: <div>Database</div> },
                { path: "/queries", element: <div>Queries</div> },
                { path: "/documents", element: <div>Documents of Interest</div> },
                { path: "/upload", element: <div>Upload Personal Data</div> },
                { path: "/llm", element: <div>LLM Settings</div> },

            ]
        }, 
        {
            path: "/register",
            element: <Register />,
          },
          {
            path: "/login",
            element: <Login />,
          },
    ]);

    return (
        <div>
            <RouterProvider router={router} />
        </div>
    );
}

export default App
