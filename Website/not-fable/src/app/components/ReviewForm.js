"use client"

import { useState } from "react"
import api from "../axios";
import Modal from "./Modal";

export default function ReviewForm({google_id}){
    const [heading, setHeading] = useState('');
    const [content, setContent] = useState('');
    const [rating, setRating] = useState('');
    const [popUp, setPopUp] = useState(false);
    const [message, setMessage] = useState('');

    function onClose(){
        setPopUp(false);
    }

    async function submitForm(){
        try {
            if (heading.trim().length == 0 || content.trim().length == 0){
                throw Error('Heading and content cannot be empty');
            }
            if (!rating){
                throw Error('Select a rating');
            }
            const response = await api.post('/books/bookReview', {
                'google_id': google_id,
                'heading': heading, 
                'content': content,
                'rating': rating
            });
            const info = response.data;
            console.log(info);
            if (!info.ok){
                throw Error(info.error);
            }
        }
        catch(e){
            setMessage(String(e));
            setPopUp(true);
        }
    }

    return (
        <div className="border p-5 rounded-2xl bg-white">
            {popUp && <Modal onClose={onClose} message={message}/>}
            <h1 className="font-semibold text-2xl underline mb-6"
            >Write a review</h1>
            
            <div className="mb-4">
                <label htmlFor="heading" 
                className="block text-lg font-medium text-gray-700 mb-2">
                    Heading
                </label>
                <input 
                    id="heading"
                    className="border rounded-sm w-full p-2"
                    value={heading}
                    onChange={e => setHeading(e.target.value)}
                />
            </div>

            <div >
                <label htmlFor="rating"
                className=""> Rating </label>
                <select
                id="rating"
                value={rating}
                onChange={e => setRating(e.target.value)}
                className="border rounded-md my-3 ml-3">
                    <option value="">Select a rating</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                </select>
            </div>
            
            <div className="mb-4">
                <label 
                htmlFor="content" 
                className="block text-lg font-medium text-gray-700 mb-2">
                    Content
                </label>
                <textarea 
                    className="w-full border rounded-xl p-2" 
                    value={content}
                    onChange={e => setContent(e.target.value)}
                    placeholder="Markdown can be used here"
                    id="content"
                    rows={6}
                />
            </div>
            
            <button 
            className="bg-purple-700 text-white font-semibold px-4 py-2 rounded-lg hover:inset-ring-1 hover:bg-teal-400 hover:scale-106 duration-40 ease-in-out"
            onClick={submitForm}
            >
                Submit Review
            </button>
        </div>
    )
}