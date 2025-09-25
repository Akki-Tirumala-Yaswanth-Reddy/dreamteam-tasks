'use client';
import { useState } from "react";
import api from "@/app/axios";
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
                await api.post('/signup',{username: username, password: password, email: email});
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
            <nav className="bg-linear-to-r/decreasing from-indigo-500 to-teal-400 bg-cover border-b-1 border-indigo-200 p-5">
                <div className="">
                    <h1 className="font-bold text-white text-4xl">!Fable</h1>
                </div>
            </nav>
            <div className="flex justify-center items-center h-screen w-screen bg-linear-to-r/decreasing from-indigo-500 to-teal-400 bg-cover">
            {popup && <Modal onClose={onClose} message={modalMessage}/>}
                <div className="flex flex-col justify-center p-10 rounded-2xl w-full max-w-md bg-white/30 backdrop-blur-sm">
                    <label htmlFor="username"
                    className="pb-3 text-3xl font-semibold">
                        Username</label>
                    <input id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="border rounded-md mb-3 p-1"/>

                    <label htmlFor="email"
                    className="pb-3 text-3xl font-semibold"
                        >Email</label>
                    <input id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="border rounded-md mb-3 p-1"/>

                    <label htmlFor="password"
                    className="pb-3 text-3xl font-semibold"
                        >Password</label>
                    <input id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="border rounded-md mb-3 p-1"/>

                    <label htmlFor="password2"
                    className="pb-3 text-3xl font-semibold"
                        >Re-enter the password</label>
                    <input id="password2"
                    value={password2}
                    onChange={(e) => setPassword2(e.target.value)}
                    className="border rounded-md mb-3 p-1"/>

                    <div className="flex justify-between">
                        <button className="mt-3 p-2 rounded-xl  text-white font-semibold bg-purple-700 hover:inset-ring-1 hover:bg-teal-400 hover:scale-106 duration-100 ease-in-out"
                        onClick={submitSignup}
                        >
                            Signup
                        </button>
                        <button className="mt-3 p-2 rounded-xl text-white font-semibold bg-teal-400 hover:inset-ring-1 hover:bg-purple-700 hover:scale-106 duration-40 ease-in-out">
                            <Link href="/pages/login">Login</Link>
                        </button>
                    </div>
                </div>
            </div>
        </>
    )
}

export default signupPage;