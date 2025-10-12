'use client'
import api from "@/app/axios"
import Modal from "@/app/components/Modal";
import NavBar from "@/app/components/Navbar";
import ReviewForm from "@/app/components/ReviewForm";
import ReviewsSection from "@/app/components/ReviewsSection";
import Image from "next/image"
import { useEffect, useState, use } from "react";


export default function Book({params}){

    const {id} = use(params);
    async function getBook(id){
        try {
            const response = await api.get(`books/getbook/${id}`);
            const data = response.data
            return data.message;
        }
        catch (e){
            console.log(e);
        }
    }

    const [book, setBook] = useState(null)
    const [lists, setLists] = useState();
    const [choosenList, setChoosenList] = useState();
    const [message, setMessage] = useState('');
    const [popUp, setPopUp] = useState(false);

    function onClose(){
        setPopUp(false);
    }

    useEffect(() => {
        if(!id) return ;
        async function fetchBook () {
            console.log(book);
            const bookData = await getBook(id);
            setBook(bookData);
        }
        fetchBook();
        getLists();
    },[id])

    if(!book){
        return (
            <>
                <NavBar/>
                <div className="bg-gray-100 min-h-screen w-full">
                    <p className="p-10 text-xl">Loading...</p>
                </div>
            </>
        );
    }

    async function getLists(){
        try{
            const res = await api.get('/reading_list/lists');
            const data = res.data;
            if(!data.ok){
                throw Error(data.error);
            }
            setLists(data.message);
        }
        catch(e){
            setMessage(e.response.data.error || e.message);
            setPopUp(true);
            setLists([]);
        }
    }

    async function addToList(){
        try{
            const req = await api.post(`/reading_list/list/${choosenList}/book`, {'google_id': book.google_id, 'title': book.title});
            console.log(req);
            const data = req.data;
            console.log(data);
            if (!data.ok){
                console.log(data);
                throw Error(data.error);
            }
            getLists();
            setMessage("Book added to the list");
            setPopUp(true);
        }
        catch(e){
            setMessage(e.response.data.error || e.message);
            setPopUp(true);
        }
    }

    function AddToListBlock(){
        return (
            <>
                <div className="">
                    <label htmlFor="list"
                    className="font-semibold"> Add to a list </label>
                    <select
                    id="list"
                    value={choosenList}
                    onChange={e => setChoosenList(e.target.value)}
                    className="border rounded-md my-3 ml-3">
                        <option value="">Select the list</option>
                        {lists.map((list, i) => 
                            <option value={list.id} key={i}>{list.name}</option>
                        )}
                    </select>
                    <br/>
                    <button 
                    className="bg-purple-700 text-white font-semibold px-3 py-1 rounded-lg hover:inset-ring-1 hover:bg-teal-400 hover:scale-106 duration-40 ease-in-out"
                    onClick={addToList}
                    >Add to List</button>
                </div>
            </>
        )
    }

    return (
        <>  
            <NavBar/>
            {popUp && <Modal onClose={onClose} message={message}/>}
            <div className="bg-gray-100 min-h-screen w-full">
                <h1 className="font-semibold px-10 pt-10 text-4xl">{book.title}</h1>
                <h2 className="font text-gray-600 text-xl px-11 pt-3" >{book.subtitle}</h2>
                <div className="flex p-10">
                    <Image src={book.imageUrl} width={750} height={500} alt={`POster of ${book.title}`}/>
                    <div className="px-10">
                        {
                            book.rating ? (<p>{book.rating}⭐️</p>) : <p >No rating available</p>
                        }
                        <h2 className="font-semibold text-xl mt-3">Author</h2>
                        <p className="">{book.authors}</p>
                        <h2 className="font-semibold text-xl mt-3">Description</h2>
                        <p className=""
                        dangerouslySetInnerHTML={{__html: book.description}} // There are some sentences with tags like <i> etc
                         ></p>                                               {/* they can be displayed with the setInnerHtml setting */}
                        <AddToListBlock/>
                    </div>
                </div>
                <div className="pl-10 pr-18">
                    <ReviewForm google_id={id}/>
                </div>
                <div className="p-10 pr-18"> 
                    <ReviewsSection google_id={id}/>
                </div>
            </div>
        </>
    )
}

