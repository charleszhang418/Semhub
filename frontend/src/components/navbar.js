import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './Home';
import RepoRequest from './RepoRequest';

function Navbar() {
  return (
    <Router>
      <div>
        <nav>
          <div className="navbar-brand">Semgrep</div>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/RepoRequest">Repo Request</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/RepoRequest" element={<RepoRequest />}>
            
          </Route>
          <Route path="/" element={<Home />}>
            
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default Navbar;