import Image from "next/image"
import { api2 } from "@/app/axios";
import Link from "next/link";

async function gettingRandomBooks(){
    const books = [];
    try {
        const response = await api2.get('/books/getbooks');
        const data = response.data.message;
        console.log(typeof(data));
        const size = Math.min(15, data.length);

        for(let i = 0 ; i < size ; i++){
            let idx = Math.floor(Math.random() * data.length);
            if (books.includes(data[idx])) {
                i--;
                continue;
            }
            books.push(data[idx]);
        }
    }
    catch(e){
        console.error(e.message);
        return [];
    }
    return books;
}

export default async function BooksContainer(){
    const books = await gettingRandomBooks();
    return (
        <>
            <div className="grid grid-cols-5 gap-6 p-6">
                {
                    books.map((book, i) => 
                        <Link key={i} href={`/pages/book/${book.google_id}`}>
                            <Block key={i} book={book}/>
                        </Link>
                    )
                }
            </div>
        </>
    )
}

function Block({book}){
    return (
        <>
            <div className="bg-white rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 p-4 cursor-pointer hover:scale-105 transition-transform duration-300">
                <div className="aspect-[3/4] relative mb-4 overflow-hidden rounded-md">
                    <Image 
                        src={book.imageUrl}
                        fill
                        className="object-cover"
                        alt={book.title + "'s image"}
                    />
                </div>
                <div className="space-y-2">
                    <h3 className="font-bold text-lg text-gray-800 line-clamp-2 leading-tight">{book.title}</h3>
                    <h4 className="text-sm text-gray-600 line-clamp-1">{book.subtitle}</h4>
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-1">
                            <span className="text-yellow-500">★</span>
                            <p className="text-sm font-medium text-gray-700">{book.rating}</p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}