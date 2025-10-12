import NavBar from "@/app/components/Navbar";
import ThreeBlock from "@/app/components/ThreeBlock";

export default function Home(){
    return(
        <>
            <NavBar/>
            <div className="flex flex-col min-h-screen w-full bg-gray-100 items-center justify-center py-8">
                <h1 className="font-bold text-4xl justify-self-start">Recommended</h1>
                <div className="w-full max-w-6xl mx-auto px-4">
                    <ThreeBlock/>
                </div>
            </div>
        </>
    )
}