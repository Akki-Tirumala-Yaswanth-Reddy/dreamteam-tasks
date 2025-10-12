"use client"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";

export default function NavBar(){

    const [loggedIn, setloggedIn] = useState(false);
    const router = useRouter();
    const pathname = usePathname(); // We can get the url string after host number.

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            setloggedIn(true);
        }
        else{
            setloggedIn(false);
        }
    }, [pathname]);

    function handleLogout(){
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user_id');
        setloggedIn(false);
        router.push('/pages/login');
    }

    return(
        <nav className="flex justify-between">
            <h1 className="font-semibold text-4xl ml-4 my-6"><Link href="/pages/home">📖 Not Fable</Link></h1>
            <div className="flex ">
                { loggedIn &&
                <h3 className="my-6 p-2 mx-3 rounded-xl font-semibold text-purple-700 active:inset-ring-1 hover:text-teal-400 hover:scale-106 duration-40 ease-in-out">
                    <Link href='/pages/myreviews'>My Reviews</Link>
                </h3>
                }
                { loggedIn &&
                <h3 className="my-6 p-2 mx-3 rounded-xl font-semibold text-purple-700 active:inset-ring-1 hover:text-teal-400 hover:scale-106 duration-40 ease-in-out">
                    <Link href='/pages/mylists'>My Lists</Link>
                </h3>
                }
                { loggedIn ?
                <button onClick={handleLogout} className="my-6 p-2 mx-3 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out">
                    Logout
                </button>
                :
                <button className="my-6 p-2 mx-3 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out">
                    <Link href='/pages/signup'>Sign up</Link>
                </button>
                }
            </div>
        </nav>
    )
}
