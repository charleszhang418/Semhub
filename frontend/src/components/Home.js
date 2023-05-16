
import '../App.css';
import { useEffect, useState } from 'react';
import { DisplayArea } from './displayArea'
const BACKEND_URL = 'http://127.0.0.1:3001'


function Home() {
  const [displayData, setDisplayData] = useState('');
  const [displayDataType, setDisplayDataType] = useState(false);
  const [searchValue, setSearchValue] = useState('');
  const [page, setPage] = useState(0);

  async function getSummary() {
    setDisplayDataType('summary')
    setDisplayData(await (await fetch(BACKEND_URL + '/summary')).json());
  }

  async function getRankings() {
    setDisplayData((await (await fetch(BACKEND_URL + `/rank_all?page=${page}`)).json()));
    setDisplayDataType('rank_all')
  }

  async function compareRepos() {
    setDisplayData((await (await fetch(BACKEND_URL + '/compare_repos')).json()));
    setDisplayDataType('compare_repos')
  }

  async function getTopRepos() {
      setDisplayData((await (await fetch(BACKEND_URL + '/top_repos')).json()));
      setDisplayDataType('top_repos');
  }

  // LMAO!
  const PAGE_MAPPING = {
    summary: getSummary,
    rank_all: getRankings,
    compare_repos: compareRepos,
    top_repos: getTopRepos
  }

  function refresh() {
    if (displayDataType) {
      PAGE_MAPPING[displayDataType]()
    }
   }

  const handleUrlChange = (event) => {
    setSearchValue(event.target.value);
  };
  
  async function amit() {
    if (displayDataType == 'summary' || displayDataType == 'repo_summary') {
      const ret = await (await fetch(BACKEND_URL + `/summary?repo_name=${searchValue}`)).json();
   
      setDisplayData(ret);
      setDisplayDataType('repo_summary')
    }
  }

  useEffect( () => {
     amit();

  }, [searchValue])

  useEffect(() => {refresh()}, [page])

  return (
    <div className="App">
      <header className="App-header">
        <div className='Button-container'>
          {displayDataType == 'summary' || displayDataType == 'repo_summary' ? 
          <div className='input-container'>
            <label>
              Repo Name:
              <input type="text" value={searchValue} onChange={handleUrlChange} />
            </label>
           
          </div> : <></>}
 
          <button onClick={getSummary}>Summary</button>
          <button onClick={getRankings}>Get Rankings</button>
          <button onClick={compareRepos}>Compare Repos</button>
          <button onClick={getTopRepos}>Get Top Repos</button>
        </div>
        
          <DisplayArea type={displayDataType} data={displayData}></DisplayArea>
          <button onClick={ ()=> { setPage(page + 1) }}>next page</button>
          <button onClick={ () => { setPage(Math.max(0, page - 1))}}>prev page</button>
      </header>
    </div>
  );
}

export default Home;
