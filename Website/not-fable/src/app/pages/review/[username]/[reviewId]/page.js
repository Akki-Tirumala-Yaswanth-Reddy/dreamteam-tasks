'use client'

import api from "@/app/axios";
import CommentForm from "@/app/components/CommentForm";
import CommentSection from "@/app/components/CommentSection";
import Modal from "@/app/components/Modal";
import NavBar from "@/app/components/Navbar";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState} from "react";

export default function userReview(){
    const params = useParams();
    const router = useRouter();
    
    const username = params.username;
    const reviewId = params.reviewId;
    
    const [popUp, setPopUp] = useState(false);
    const [message, setMessage] = useState('');
    const [review, setReview] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function getReview(){
            try {
                setLoading(true);
                const response = await api.get('/reviews/review/' + reviewId);
                
                if (!response.data.ok){
                    throw new Error(response.data.error);
                }
                
                setReview(response.data.message);
            }
            catch(e){
                setMessage(String(e.message || e)); // || to catch axios error too.
                setPopUp(true);
            } finally {
                setLoading(false);
            }
        }
        
        getReview();
    }, [reviewId]);

    async function refreshReview() {
        if (!reviewId) return;
        
        try {
            const response = await api.get('/reviews/review/' + reviewId);
            if (response.data.ok) {
                setReview(response.data.message);
            }
        } catch(e) {
            setMessage(String(e.message || e));
            setPopUp(true);
        }
    }

    async function submitLike(){
        try {
            const response = await api.post('/reviews/review/' + review.id + '/like');
            if (!response.data.ok){
                throw new Error(response.data.error);
            }
            refreshReview();
        }
        catch(e){
            setMessage(String(e.message || e));
            setPopUp(true);
        }
    }

    async function submitDisLike(){
        try {
            const response = await api.post('/reviews/review/' + review.id + '/dislike');
            if (!response.data.ok){
                throw new Error(response.data.error);
            }
            refreshReview();
        }
        catch(e){
            setMessage(String(e.message || e));
            setPopUp(true);
        }
    }

    async function deleteReview(){
        try {
            const response = await api.delete('/reviews/review/' + review.id);
            if (!response.data.ok){
                throw new Error(response.data.error);
            }
            router.push('/pages/book/' + review.book.google_id);
        }
        catch(e){
            setMessage(String(e));
            setPopUp(true);
        }
    }

    function onClose(){
        setPopUp(false);
    }

    if (loading) {
        return (
            <>
                <NavBar/>
                <div className="flex justify-center items-center min-h-screen">
                    Loading...
                </div>
            </>
        );
    }

    if (!review) {
        return (
            <>
                <NavBar/>
                <div className="flex justify-center items-center min-h-screen">
                    Review not found
                </div>
            </>
        );
    }

    return (
        <>
        <NavBar/>
        {popUp && <Modal message={message} onClose={onClose}/>}
        <div className="bg-gray-100 w-screen h-screen">
            <div className="p-6 ">
                <h1 className="px-4 pb-2 pt-6 font-semibold text-4xl">{review.heading}</h1>
                <h2 className="px-4 text-2xl font-light pb-2">By: {review.user.username}</h2>
                <Link href={`/pages/book/${review.book.google_id}`}>
                    <h1 className="px-4 pb-2 pt-2 font-semibold text-2xl text-purple-700 hover:text-teal-400">Book: {review.book.title}</h1>
                </Link>
                <h1 className="px-4 text-lg text-gray-700">⭐️ {review.rating}</h1>
                <h2 className="px-4 text-lg font-medium text-black">{review.content}</h2>
                <div className="px-4 text-lg font-medium flex gap-4">
                    <p 
                        onClick={submitLike}
                        className="cursor-pointer hover:scale-110 transition-transform"
                    >👍🏻 {review.likes}</p> 
                    <p
                        onClick={submitDisLike}
                        className="cursor-pointer hover:scale-110 transition-transform"
                    >👎🏻 {review.dislikes}</p>  
                </div>
                {review.user.id == localStorage.getItem('user_id') ? 
                <button 
                    className="px-4 py-2 mx-3 mt-2 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out"
                    onClick={deleteReview}
                >
                    Delete
                </button> 
                : <></> 
                }
            </div>
            <div className="p-7">
                <CommentForm setMessage={setMessage} review={review} setPopUp={setPopUp} onUpdate={refreshReview} />
            </div>
            <div className="p-7">
                <CommentSection review={review} setMessage={setMessage} setPopUp={setPopUp} onUpdate={refreshReview} />
            </div>
        </div>
        </>
    )
}