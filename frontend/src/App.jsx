import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState("asc");

  // List of job JSON sources (PLF last)
  const sources = [
    "/jobs.json",
    "/jobs_tm.json",
    "/jobs_yaf.json",
    "/jobs_afpi.json",
    "/jobs_hudson.json",
    "/jobs_cato.json",
    "/jobs_plf.json"
    "/jobs_heritage.json",
  ];

  useEffect(() => {
    async function loadJobs() {
      let all = [];

      for (const src of sources) {
        try {
          const response = await fetch(src);
          if (response.ok) {
            const data = await response.json();
            all = [...all, ...data];
          }
        } catch (e) {
          console.log("Failed to load:", src);
        }
      }

      setJobs(all);
    }

    loadJobs();
  }, []);

  const sortTable = (column) => {
    let direction = sortDirection;

    if (sortColumn === column) {
      direction = direction === "asc" ? "desc" : "asc";
    } else {
      direction = "asc";
    }

    const sorted = [...jobs].sort((a, b) => {
      const x = a[column] ? a[column].toString().toLowerCase() : "";
      const y = b[column] ? b[column].toString().toLowerCase() : "";

      if (x < y) return direction === "asc" ? -1 : 1;
      if (x > y) return direction === "asc" ? 1 : -1;
      return 0;
    });

    setSortColumn(column);
    setSortDirection(direction);
    setJobs(sorted);
  };

  return (
    <div className="App">
      <h1>Conservative Jobs Board</h1>
      <table>
        <thead>
          <tr>
            <th onClick={() => sortTable("title")}>Job Title</th>
            <th onClick={() => sortTable("organization")}>Organization</th>
            <th onClick={() => sortTable("location")}>Location</th>
            <th onClick={() => sortTable("type")}>Type</th>
            <th>Link</th>
          </tr>
        </thead>

        <tbody>
          {jobs.map((job, index) => (
            <tr key={index}>
              <td>{job.title}</td>
              <td>{job.organization}</td>
              <td>{job.location}</td>
              <td>{job.type}</td>
              <td>
                <a href={job.link} target="_blank" rel="noreferrer">
                  Apply
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

