function loginPage(){
    return (
        <>
            <nav className="bg-linear-to-r/decreasing from-indigo-500 to-teal-400 bg-cover border-b-1 border-indigo-200 p-5">
                <div className="">
                    <h1 className="font-bold text-white text-4xl">!Fable</h1>
                </div>
            </nav>
            <div className="flex flex-col justify-center items-center h-screen w-screen bg-linear-to-r/decreasing from-indigo-500 to-teal-400 bg-cover">
                <div className="flex flex-col justify-center p-10 rounded-2xl w-full max-w-md bg-white/30 backdrop-blur-sm">
                    <label htmlFor="username"
                    className="pb-3 text-3xl font-semibold">
                        Username</label>
                    <input id="username"
                    className="border rounded-md mb-3 p-1"/>

                    <label htmlFor="password"
                    className="pb-3 text-3xl font-semibold"
                        >Password</label>
                    <input id="password"
                    className="border rounded-md mb-3 p-1"/>

                    <div className="flex justify-between">
                        <button className="mt-3 p-2 rounded-xl  text-white font-semibold bg-purple-700 hover:inset-ring-1 hover:bg-teal-400 hover:scale-106 duration-100 ease-in-out">
                            Login
                        </button>
                        <button className="mt-3 p-2 rounded-xl text-white font-semibold bg-teal-400 hover:inset-ring-1 hover:bg-purple-700 hover:scale-106 duration-40 ease-in-out">
                            Signup
                        </button>
                    </div>
                </div>
            </div>
        </>
    )
}

export default loginPage;