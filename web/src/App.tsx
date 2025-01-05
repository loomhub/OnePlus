import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { BankAccountsPage } from "./components/BankAccounts/BankAccountsPage";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <h1>OnePlus Realty</h1>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<BankAccountsPage />} />
            <Route path="/bank-accounts" element={<BankAccountsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
