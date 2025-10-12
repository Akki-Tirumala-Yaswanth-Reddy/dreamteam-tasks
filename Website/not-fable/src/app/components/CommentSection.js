import { useState } from "react"
import api from "../axios"

export default function CommentSection({review, setMessage, setPopUp, onUpdate}){

    async function deleteComment(comment){
        try {
            console.log('Deleting comment:', comment);
            console.log('Comment ID:', comment.id);
            console.log('Review ID:', review.id);
            const response = await api.delete(`/reviews/review/${review.id}/comment/${comment.id}`);
            if (!response.data.ok) {
                throw new Error(response.data.error);
            }
            
            if (onUpdate) {
                onUpdate();
            }
        }
        catch(e){
            console.error("Error deleting comment:", e);
            setMessage(e.response?.data?.error || e.message || String(e));
            setPopUp(true);
        }

    }

    return (
        <>
            <div className="">
                <h1 className="mb-3 font-bold text-2xl underline underline-offset-1">Comments</h1>
                {review.comments && review.comments.length > 0 ? (
                    review.comments.map((comment, i) => 
                        <CommentBlock 
                            comment={comment} 
                            deleteComment={deleteComment} 
                            key={i}
                        />
                    )
                ) : (
                    <p className="text-gray-500 text-center py-8">No comments yet</p>
                )}
            </div>
        </>
    )
}


function CommentBlock({comment, deleteComment}) {
    return (
        <div className="border rounded-2xl p-5 bg-white mb-5">
            <h1 className="mb-2 font-semibold text-gray-800 text-xl">{comment.user.username}</h1>
            <h2 className="mb-3 text-lg">{comment.content}</h2>
            {comment.user.id == localStorage.getItem('user_id') ? 
                <button 
                    className="px-4 py-2 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out"
                    onClick={() => deleteComment(comment)}
                >
                    Delete
                </button> 
                : <></> 
            }
        </div>
    )
}