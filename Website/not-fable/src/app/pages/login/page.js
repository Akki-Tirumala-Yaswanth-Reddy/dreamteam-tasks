'use client'
import { useState } from "react";
import api from "@/app/axios";
import Modal from "@/app/components/Modal";
import Link from "next/link";

function loginPage(){
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [modalMessage, setModalMessage] = useState('');
    const [popup, setPopup] = useState(false);

    function onClose(){
        setPopup(false);
    }

    async function submitLogin(e){
        e.preventDefault();
        try{
            if (password.trim() === '' || username.trim() === ''){
                alert("Username and password cant be empty");
            }
            else{
                const response = await api.post('/login', {username: username, password: password});
                setModalMessage("You have been signed in.");
                setPopup(true);
                // Storing the refresh_token in local storage, not recommended but is used for demonstration purposes. Prefered way is storing them in httpOnly cookie.
                localStorage.setItem('refresh_token', response.data.refresh_token);
                console.log(response.data);
            }
        }
        catch(e){
            setModalMessage(e.response.data.error);
            setPopup(true);
        }
    }

    return (
        <>
            <nav className="bg-linear-to-r/decreasing from-indigo-500 to-teal-400 bg-cover border-b-1 border-indigo-200 p-5">
                <div className="">
                    <h1 className="font-bold text-white text-4xl">!Fable</h1>
                </div>
            </nav>
            <div className="flex flex-col justify-center items-center h-screen w-screen bg-linear-to-r/decreasing from-indigo-500 to-teal-400 bg-cover">
                {popup && <Modal onClose={onClose} message={modalMessage}/>}
                <div className="flex flex-col justify-center p-10 rounded-2xl w-full max-w-md bg-white/30 backdrop-blur-sm">
                    <label htmlFor="username"
                    className="pb-3 text-3xl font-semibold">
                        Username</label>
                    <input id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="border rounded-md mb-3 p-1"/>

                    <label htmlFor="password"
                    className="pb-3 text-3xl font-semibold"
                        >Password</label>
                    <input id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="border rounded-md mb-3 p-1"/>

                    <div className="flex justify-between">
                        <button className="mt-3 p-2 rounded-xl  text-white font-semibold bg-purple-700 hover:inset-ring-1 hover:bg-teal-400 hover:scale-106 duration-100 ease-in-out"
                        onClick={submitLogin}
                        >
                            Login
                        </button>
                        <button className="mt-3 p-2 rounded-xl text-white font-semibold bg-teal-400 hover:inset-ring-1 hover:bg-purple-700 hover:scale-106 duration-40 ease-in-out">
                            <Link href="/pages/signup">Signup</Link>
                        </button>
                    </div>
                </div>
            </div>
        </>
    )
}

export default loginPage;