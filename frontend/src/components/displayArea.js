import './Home.css';

export function DisplayArea({ type, data }) {

    if (type == 'summary') {
        return <ul>
            <li>Total Owners: {data.totalOwners}</li>
            <li>Total Organizations: {data.totalOrgs}</li>
            <li>Total Users: {data.totalUsers}</li>
            <li>Total Repos: {data.totalRepos}</li>
            <li>Total Issues: {data.totalIssues}</li>
        </ul>
    } if (type == 'repo_summary') {
        try {

        
        return <table border="3" height="50%" width="50%" bordercolor="white" cellpadding ="10">
        <tr>
            <th>Repository</th>

            <th># Issues</th>

        </tr>
        {data.map((repoData) =>
        <tr key={repoData[0]}>
            <th>{repoData[0]}</th>
            <th>{repoData[1]}</th>
        </tr>
        )}
    </table>
        } catch {
            return <></>
        }
    } else if (type === 'compare_repos') {
        return <table border="3" height="50%" width="50%" bordercolor="white" cellpadding ="10">
            <tr>
                <th>Repository</th>
                <th>Owner</th>
                <th>Stars</th>
                <th># Issues</th>
                <th>Max Impact</th>
                <th>AVG Impact</th>
                <th>Impact</th>
                <th>update</th>
            </tr>
            {data.impact.map((repoData) =>
            <tr key={repoData[0]}>
                <th>{repoData[0]}</th>
                <th>{repoData[1]}</th>
                <th>{repoData[2]}</th>
                <th>{repoData[3]}</th>
                <th>{repoData[4]}</th>
                <th>{repoData[5]}</th>
                <th>{repoData[6]}</th>
                <th><button onClick={async () => {      const response = await fetch('http://localhost:3001/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_name: repoData[0], owner: repoData[1] })
      });}}>update</button></th>
            </tr>
            )}
        </table>
    } else if (type == 'rank_all') {
        return <table  border="3" height="50%" width="50%" bordercolor="white" cellpadding ="10">
            <tr>
                <th>Repository</th>
                <th>Owner</th>
                <th># Issues</th>
                <th>Ranking</th>
                <th>Update</th>
            </tr>
            {data.rankings.map((repoData) => <tr key={repoData[0]}>
                <th>{repoData[0]}</th>
                <th>{repoData[1]}</th>
                <th>{repoData[2]}</th>
                <th>{repoData[3]}</th>
                <th><button onClick={async () => {      const response = await fetch('http://localhost:3001/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_name: repoData[0], owner: repoData[1] })
      });}}>update</button></th>
            </tr>)}
        </table>
    } else if (type == 'top_repos') {
        return <table border="3" height="50%" width="50%" bordercolor="white" cellpadding ="10">
            <tr>
                <th>Repository</th>
                <th>Owner</th>
                <th>Overall Issue Impact</th>
            </tr>
            {data.top_repos.map((repoData) => <tr key={repoData[0]}>
                <th>{repoData[0]}</th>
                <th>{repoData[1]}</th>
                <th>{repoData[2]}</th>
            </tr>)}
        </table>
    } else {
        return <></>
    }
}