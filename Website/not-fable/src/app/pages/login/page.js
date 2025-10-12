'use client'
import { useState } from "react";
import api from "@/app/axios";
import Modal from "@/app/components/Modal";
import Link from "next/link";
import { useRouter } from "next/navigation";

function loginPage(){
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [modalMessage, setModalMessage] = useState('');
    const [popup, setPopup] = useState(false);
    const router = useRouter();

    function onClose(){
        setPopup(false);
    }

    async function submitLogin(e){
        e.preventDefault();
        try{
            if (password.trim() === '' || username.trim() === ''){
                setModalMessage("Username and password cant be empty");
                setPopup(true);
                return;
            }
            else{
                const response = await api.post('/auth/login', {username: username, password: password});
                localStorage.setItem('refreshToken', response.data.refresh_token);
                localStorage.setItem('accessToken', response.data.access_token);
                localStorage.setItem('user_id', response.data.user_id);
                router.push("/pages/home");
            }
        }
        catch(err){
            console.error('Login error:', err);
            
            let errorMessage = "Login failed";
            
            if (err.response) {
                errorMessage = err.response.data?.error || "Server error";
            } else if (err.request) {
                errorMessage = "Network error - please check if the server is running and CORS is configured";
            } else {
                errorMessage = err.message || "An unexpected error occurred";
            }
            
            setModalMessage(errorMessage);
            setPopup(true);
        }
    }

    return (
        <>
            <nav className="flex justify-between">
                <h1 className="font-semibold text-4xl ml-4 my-6">📖 Not Fable</h1>
                <button className="my-6 p-2 mx-3 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out">
                    <Link href='/pages/signup'>Sign up</Link>
                </button>
            </nav>
            <div className="flex bg-gray-100 h-screen w-screen">
                {popup && <Modal onClose={onClose} message={modalMessage}/>}
                <div className="flex flex-col pt-50 items-center w-full">
                    <h2 className="text-4xl text-center">📖</h2>
                    <h2 className="text-4xl text-center font-bold mb-5">Welcome back!</h2>
                    <div className="bg-white p-3 flex flex-col min-w-md rounded-2xl">
                        <h1 className="font-semibold text-3xl my-3 text-center">Login</h1>

                        <label 
                        className="text-2xl font-semibold p-3"
                        htmlFor="username"
                        >Username</label>
                        <input
                        className="p-1 mx-3 border rounded-sm"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        id="username"/>

                        <label className="text-2xl font-semibold p-3"
                        htmlFor="password"
                        >Password</label>
                        <input 
                        className="p-1 mx-3 border rounded-sm mb-5"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        id="password"/>

                        <div className="flex justify-between px-3 my-3">
                            <button 
                            className="p-2 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out"
                            onClick={submitLogin}
                            >
                                Login</button>
                            <button 
                            className="p-2 rounded-xl text-white font-semibold bg-teal-400 active:inset-ring-1 active:bg-purple-700 active:scale-106 duration-40 ease-in-out"
                                ><Link href='/pages/signup'>Sign up</Link></button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default loginPage;