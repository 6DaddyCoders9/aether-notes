import Navbar from "../components/Navbar";
import Hero from "../components/Hero/Hero";
import Summary from "../components/Summary";
import QnA from "../components/QnA";
import Footer from "../components/Footer";

export default function LandingPage() {
  return (
    <>
      <Navbar />
      <Hero />
      <Summary />
      <QnA />
      <Footer />
    </>
  );
}
