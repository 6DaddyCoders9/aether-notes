import { useState, useEffect, useRef } from "react";
import { FaCheckCircle, FaFilePdf } from "react-icons/fa";
import { IoMdSend } from "react-icons/io";
import downArrow from "../assets/down-arrow.png";

const features = [
  "Upload & organize PDFs, notes, and references.",
  "Ask questions across all your docs with AI-powered search.",
  "Get instant summaries & key insights.",
  "Collaborate and share with teammates.",
  "Keep your data private & secure.",
];

export default function QnA() {
  const [visibleFeatures, setVisibleFeatures] = useState<string[]>([]);
  const animated = useRef(false);

  useEffect(() => {
    if (animated.current) return;
    animated.current = true;

    features.forEach((feature, i) => {
      setTimeout(() => {
        setVisibleFeatures((prev) => [...prev, feature]);
      }, i * 800);
    });
  }, []);

  return (
    <section className="bg-gray-50 py-16">
      <div className="max-w-3xl mx-auto px-4">
        {/* Message box */}
        <div className="bg-white shadow-md rounded-t-2xl p-4 text-gray-800 font-medium justify-between flex items-center">
          <div>
          What does Aether Notes do?
          </div>
          <div>
          <button
            disabled
            className="flex items-center gap-1 text-sm font-medium text-gray-400 cursor-not-allowed"
          >
            <span>Send</span>
            <IoMdSend />
          </button>
          </div>
        </div>

        {/* Doc selector with icon & send button */}
        <div className="bg-gray-100 border border-gray-200 rounded-b-2xl p-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FaFilePdf className="text-red-500" />
            <span className="text-sm font-medium text-gray-700">
              AetherNotes.pdf
            </span>
          </div>
          <div className="bg-gray-100 items-center justify-between flex">
          <button
            disabled
            className="flex items-center gap-1 text-sm font-medium text-gray-400 cursor-not-allowed"
          >
            Select doc 
            <img src={downArrow} className="w-2 h-2 opacity-50"/>
          </button>      
          </div>    
        </div>

        {/* Animated feature list */}
        <div className="mt-6 p-4 bg-white rounded-md shadow-sm text-gray-700">
          <ul className="space-y-3">
            {visibleFeatures.map((feature, i) => (
              <li
                key={i}
                className="flex items-center gap-2 opacity-0 animate-fade-in"
              >
                <FaCheckCircle className="text-green-500 flex-shrink-0" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
