'use client'
import api from "@/app/axios";
import NavBar from "@/app/components/Navbar";
import { useState, useEffect } from "react"
import Modal from "@/app/components/Modal";
import Link from "next/link";

export default function MyLists(){

    const [name, setName] = useState('');
    const [popUp, setPopUp] = useState(false);
    const [message, setMessage] = useState('');
    const [lists, setLists] = useState([]);
    const [loading, setLoading] = useState(true);

    function onClose(){
        setPopUp(false)
    }

    useEffect(() => {
        getLists();
    }, []);

    async function getLists(){
        try{
            setLoading(true);
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
        finally {
            setLoading(false);
        }
    }

    async function addNewList(){
        try{
            const req = await api.post('/reading_list/list', {'name': name});
            const data = req.data;
            if (!data.ok){
                console.log(data);
                throw Error(data.error);
            }
            setName('');
            getLists();
        }
        catch(e){
            setMessage(e.response.data.error || e.message);
            setPopUp(true);
        }
    }

    async function deleteList(list_id){
        try{
            const req = await api.delete(`/reading_list/list/${list_id}`);
            const data = req.data;
            if (!data.ok){
                throw Error(data.error);
            }
            setMessage('List is deleted');
            setPopUp(true);
            getLists();
        }
        catch(e){
            setMessage(e.response.data.error || e.message);
        }
    }

    async function removeBook(list_id, google_id){
        try{
            const req = await api.delete(`/reading_list/list/${list_id}/book/${google_id}`);
            console.log(req);
            const data = req.data;
            if (!data.ok){
                throw Error(data.error);
            }
            setMessage('Book is removed');
            setPopUp(true);
            getLists();
        }
        catch(e){
            console.log(e);
            setMessage(e.response.data.error || e.message);
        }
    }

    return (
        <>
            <NavBar/>
            {popUp && <Modal message={message} onClose={onClose}/>}
            <div className="bg-gray-100 min-h-screen w-full flex flex-col">
                <div className="px-9 mt-11 flex flex-col">
                    <label className="mb-2 text-2xl font-semibold" htmlFor="name">Add a new list</label>
                    <input id="name"
                    className="border rounded-sm px-1 w-3xs"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    />
                    <button className="px-4 py-2  mt-2 w-24 rounded-xl text-white font-semibold bg-purple-700 active:inset-ring-1 active:bg-teal-400 active:scale-106 duration-40 ease-in-out"
                    onClick={addNewList}>Add</button>
                </div>
                <div className="px-9 mt-11">
                    <h2 className="text-3xl font-semibold mb-4">My lists</h2>
                    {loading ? (
                        <p>Loading...</p>
                    ) : lists && lists.length > 0 ? (
                        lists.map((list, i) => 
                            <ListBlock list={list} key={i} removeBook={removeBook} deleteList={deleteList}/>
                        )
                    ) : (
                        <p className="text-gray-500">No lists yet.</p>
                    )}
                </div>
            </div>
        </>
    )
}

function ListBlock({list, removeBook, deleteList}){
    return(
        <>
            <div className="mb-6 bg-white rounded-lg shadow p-4">
                <div className="flex gap-3">
                    <h2 className="text-2xl font-semibold mb-3">{list.name}</h2>
                    <button className="h-8 px-3 text-sm rounded-md text-white font-semibold bg-purple-700 active:inset-ring-1 hover:bg-teal-400 active:scale-106 duration-40 ease-in-out"
                    onClick={() => deleteList(list.id)}
                    >Delete List</button>        
                </div>
                {list.books && list.books.length > 0 ? (
                    list.books.map((book, i) => 
                        <div className="flex" key={i}>
                        <Link href={`/pages/book/${book.google_id}`}> {/*😋*/}
                            <h3 className="my-2 text-lg text-gray-700 cursor-context-menu hover:text-purple-700" key={i}>{book.title}</h3>
                        </Link>
                        <button className="ml-4 my-2 px-3 py-0.5 text-sm rounded-md text-white font-semibold bg-purple-700 active:inset-ring-1 hover:bg-teal-400 active:scale-106 duration-40 ease-in-out"
                        onClick={() => removeBook(list.id, book.google_id)}
                        >    
                        Remove Book</button>
                        </div>
                    )
                ) : (
                    <p className="text-gray-400">No books in this list</p>
                )}
            </div>
        </>
    )
}