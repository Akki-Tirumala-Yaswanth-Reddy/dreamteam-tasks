'use client';

export default function Modal({ onClose, message }) {
    return (
        <>
            <div className="fixed flex inset-0 backdrop-blur-md bg-black/30 justify-center items-center z-40">
                <div className="mt-10 flex flex-col gap-5 bg-white p-3 rounded-xl">
                    <button className="self-end font-extrabold text-purple-700 hover:text-teal-400" onClick={onClose}>X</button>
                    <div className="font-semibold mx-3 mb-3">
                        <p>{message}</p>
                    </div>
                </div>
            </div>
        </>
    );
}