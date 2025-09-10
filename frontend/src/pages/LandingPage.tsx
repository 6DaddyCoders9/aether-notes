import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Summary from "../components/Summary";
import QnA from "../components/QnA";
import Footer from "../components/Footer";

export default function LandingPage() {
  return (
    <>
      <Navbar />
      <div className="pt-20"> {/* padding so content isn't hidden behind navbar */}
        <h1 className="text-4xl font-bold text-center">Landing Page</h1>
      </div>
      <Hero />
      <Summary />
      <QnA />
      <Footer />
    </>
  );
}
