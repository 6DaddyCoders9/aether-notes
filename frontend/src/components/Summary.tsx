import { useState, useEffect } from "react";

const message =
  "Aether Notes helps researchers, students, and knowledge workers instantly find, summarise, and connect insights across all their documents.";

export default function Summary() {
  const [text, setText] = useState("");
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < message.length) {
      const timeout = setTimeout(() => {
        setText((prev) => prev + message[index]);
        setIndex(index + 1);
      }, 40); // typing speed
      return () => clearTimeout(timeout);
    }
  }, [index]);

  return (
    <section className="bg-white py-5 text-left">
      <div className="max-w-4xl mx-auto px-4">
        {/* Prompt line */}
        <p className="text-lg font-mono text-gray-500 mb-4">
          {"> Summarise AetherNotes.pdf"}
        </p>

        {/* Answer with cursor */}
        <h2 className="text-2xl md:text-3xl text-gray-800 font-semibold">
          {text}
          <span className="animate-pulse">|</span>
        </h2>

        <h1 className=" text-2xl font-mono text-gray-700 mt-10 mb-2">Our Vision:</h1>
        <p className="font-mono text-lg text-black mb-2">Knowledge workers, researchers, and students are overloaded with documents, notes, and reference materials spread across many tools (Notion, Google Docs, PDFs, scattered files). Searching across them is slow, and extracting insights requires repetitive manual work. Existing note-taking apps are good for storage, but weak in intelligent retrieval, summarization, and synthesis.</p>
      </div>
    </section>
  );
}
