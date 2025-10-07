import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreatePresentationPage from "./pages/CreatePresentationPage";
import PresentationPage from "./pages/PresentationPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CreatePresentationPage />} />
        <Route path="/presentation/:id" element={<PresentationPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
