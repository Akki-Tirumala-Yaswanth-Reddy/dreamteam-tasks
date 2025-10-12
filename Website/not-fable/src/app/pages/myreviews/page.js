"use client"
import Link from "next/link";
import api from "@/app/axios";
import { useEffect, useState } from "react";
import NavBar from "@/app/components/Navbar";

export default function MyReviews(){
    const [reviews, setReviews] = useState();

    async function fetchReviews(){
        try {
            const response = await api.get('/reviews/review/user');
            const data = response.data.message;
            console.log(data);
            setReviews(data);
        }
        catch(e){
            console.log(e);
        }
    }

    useEffect(() => {
        fetchReviews();
    }, [])

    if (!reviews){
        return(
            <>
                <NavBar/>
                <div className="bg-gray-100 min-h-screen min-w-screen">
                    <p>No reviews were found</p>
                </div>
            </>
        )
    }

    return (
        <>
            <NavBar/>
            <div className="grid grid-cols-5 gap-6 p-6 bg-gray-100 min-h-screen min-w-screen">
                {
                    reviews.map((review, i) => 
                        <Link key={i} href={`/pages/review/${review.user.id}/${review.id}`}>
                            <ReviewBlock key={i} review={review}/>
                        </Link>
                    )
                }
            </div>
        </>
        
    )
}

function ReviewBlock({review}){
    return (
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 p-4 space-y-3">
            <div className="flex items-center space-x-2">
                <p className="font-medium text-gray-700">{review.user.username}</p>
            </div>
            
            <h1 className="font-semibold text-lg text-gray-800 line-clamp-2 leading-tight">
                {review.heading}
            </h1>
            
            <div className="flex items-center space-x-1">
                <div className="">⭐️</div>
                <div className="font-medium text-gray-700">{review.rating}</div>
            </div>
            
            <p className="text-gray-600 text-sm line-clamp-3 leading-relaxed">
                {review.content}
            </p>
            
            <div className="pt-2">
                <span className="text-purple-600 text-sm font-medium hover:text-teal-400">
                    Read full review
                </span>
            </div>
        </div>
    )
}
