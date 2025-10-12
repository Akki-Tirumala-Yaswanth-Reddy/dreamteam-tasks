"use client"

import { useParams } from "next/navigation";

export default function UserPage(){
    const params = useParams();
    const userId = params.id;
    const [user, setUser] = useState();

    async function getUserInfo(){
        
    }

    return (
        <>

        </>
    )
}

function GroupBlock({users, groupName}){

    return (
        <div className="">
            <h1 className="">{groupName}</h1>
            {
                users.map((user, i) => 
                    <h2 className="" key={i}>{user.username}</h2>
                )
            }
            
        </div>
    )
}