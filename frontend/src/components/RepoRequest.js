import React, { useState } from 'react';
import './RepoRequest.css';

function RepoRequest() {
  const [githubUrl, setGithubUrl] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('http://localhost:3001/add_to_queue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ github_url: githubUrl })
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleUrlChange = (event) => {
    setGithubUrl(event.target.value);
  };

  return (
    <div className='App'>
      <header className="App-header">
        <form onSubmit={handleSubmit}>
          <div className='input-container'>
            <label>
              GitHub repository URL:
              <input type="text" value={githubUrl} onChange={handleUrlChange} />
            </label>
            <button type="submit">Submit</button>
          </div>
        </form>
      </header>
    </div>
  );
}

export default RepoRequest;
