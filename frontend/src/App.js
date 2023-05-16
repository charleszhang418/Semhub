
import Navbar from './components/navbar';
import Home from './components/Home';

import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import { DisplayArea } from './components/displayArea'

import { createContext, useEffect } from 'react';
const BACKEND_URL = 'http://127.0.0.1:3001'


const ThemeContext = createContext({
  theme: "dark",
  changeTheme: () => {},
})



function App() {
  const [theme, setTheme] = useState("dark");
  useEffect(() => {
    if (theme == "dark") {
      document.body.classList.add('dark-mode');
      document.body.classList.remove('light-mode');
    } else {
      document.body.classList.add('light-mode');
      document.body.classList.remove('dark-mode');
    }
  }, [theme])

  const changeTheme = () => {
    if (theme == "dark") {
      setTheme("light");
    } else {
      setTheme("dark");
    }
  }

  return (
    <ThemeContext.Provider value={{ theme: theme, changeTheme }}>
      <button className="mode" onClick={changeTheme}>{theme} mode</button>
      <Navbar></Navbar>
    </ThemeContext.Provider>
  );
}

export default App;
