'use client';
import { useState } from "react";
import {api2} from "@/app/axios";
import Modal from "@/app/components/Modal";
import { useRouter } from "next/navigation";
import Link from "next/link";

function signupPage(){
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [popup, setPopup] = useState(false);
    const [modalMessage, setModalMessage] = useState('');
    const router = useRouter();

    async function submitSignup(e){
        e.preventDefault();
        var arr = [password, password2, username, email];
        if (arr.some(i => i.trim() === '')){
            setModalMessage('The given fields cannot be empty');
            setPopup(true);
            return;
        }
        else if(password !== password2){
            setModalMessage('The given password and the re-entered password are different');
            setPopup(true);
        }
        else if(password.length < 8){
            setModalMessage('The given password is shorter than 8 characters');
            setPopup(true);
        }
        else {
            try{
                await api2.post('/auth/signup',{username: username, password: password, email: email});
                router.push("/pages/login");
            }
            catch(e){
                setModalMessage(e.response.data.error);
                setPopup(true);
            }
        }
    }

    function onClose(){
        setPopup(false);
    }

    return (
        <>
            <nav className="flex justify-between">
                <h1 className="font-semibold text-4xl ml-4 my-6">📖 Not Fable</h1>
                <button className="my-6 p-2 mx-3 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out">
                    <Link href='/pages/login'>Login</Link>
                </button>
            </nav>
            <div className="flex bg-gray-100 h-screen w-screen">
                {popup && <Modal onClose={onClose} message={modalMessage}/>}
                <div className="flex flex-col pt-30 items-center w-full">
                    <h2 className="text-4xl text-center">📖</h2>
                    <h2 className="text-4xl text-center font-bold mb-5">Hello!!</h2>
                    <div className="bg-white p-3 flex flex-col min-w-md rounded-2xl">
                        <h1 className="font-semibold text-3xl my-3 text-center">Sign Up</h1>

                        <label 
                        className="text-2xl font-semibold p-3"
                        htmlFor="username"
                        >Username</label>
                        <input
                        className="p-1 mx-3 border rounded-sm"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        id="username"/>

                        <label 
                        className="text-2xl font-semibold p-3"
                        htmlFor="email"
                        >Email</label>
                        <input
                        className="p-1 mx-3 border rounded-sm"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        id="email"/>

                        <label className="text-2xl font-semibold p-3"
                        htmlFor="password"
                        >Password</label>
                        <input 
                        className="p-1 mx-3 border rounded-sm"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        id="password"/>

                        <label className="text-2xl font-semibold p-3"
                        htmlFor="password2"
                        >Re-Enter the password</label>
                        <input 
                        className="p-1 mx-3 border rounded-sm mb-5"
                        value={password2}
                        onChange={e => setPassword2(e.target.value)}
                        id="password2"/>

                        <div className="flex justify-between px-3 my-3">
                            <button 
                            className="p-2 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out"
                            onClick={submitSignup}
                            >
                                Signup</button>
                            <button 
                            className="p-2 rounded-xl text-white font-semibold bg-teal-400 active:inset-ring-1 active:bg-purple-700 active:scale-106 duration-40 ease-in-out"
                                ><Link href='/pages/login'>Login</Link></button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default signupPage;