"use client"
import { useState } from "react";
import api from "../axios";
import Modal from "./Modal";

export default function CommentForm({setMessage, setPopUp, review, onUpdate}) {
    const [comment, setComment] = useState('');

    async function submitComment(){
        try{
            const response = await api.post('/reviews/review/'+ review.id +'/comment', {
                'content': comment
            });
            const data = response.data.message;
            if (!data){
                throw Error(response.data.error);
            }
            onUpdate();
        }
        catch(e){
            setMessage(String(e));
            setPopUp(true);
        }
    }

    return (
        <>
            <div className="border rounded-xl p-5 bg-white">
                <h1 className="font-semibold mb-2 text-2xl">Write a comment</h1>
                <textarea 
                value={comment}
                onChange={e => setComment(e.target.value)}
                className="border rounded-lg w-full p-2 mb-3"/>
                <button 
                className="bg-purple-700 text-white font-semibold px-4 py-2 rounded-lg hover:inset-ring-1 hover:bg-teal-400 hover:scale-106 duration-40 ease-in-out"
                onClick={submitComment}
                >
                Submit Comment
                </button>
            </div>
        </>
    )
}