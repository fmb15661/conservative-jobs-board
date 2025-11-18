import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState("asc");

  // ALL job JSON sources (updated to include AIER + ExcelinEd)
  const sources = [
    "/jobs.json",
    "/jobs_tm.json",
    "/jobs_yaf.json",
    "/jobs_afpi.json",
    "/jobs_hudson.json",
    "/jobs_cato.json",
    "/jobs_plf.json",
    "/jobs_ntu.json",
    "/jobs_acton.json",
    "/jobs_aier.json",
    "/jobs_excelined.json"
  ];

  useEffect(() => {
    async function loadJobs() {
      let allJobs = [];

      for (const src of sources) {
        try {
          const res = await fetch(src);
          if (!res.ok) continue;

          const data = await res.json();
          if (Array.isArray(data)) {
            allJobs = [...allJobs, ...data];
          }
        } catch (e) {
          console.error("Failed to load:", src, e);
        }
      }

      setJobs(allJobs);
    }

    loadJobs();
  }, []);

  function sortBy(column) {
    let direction = sortDirection;

    if (sortColumn === column) {
      direction = direction === "asc" ? "desc" : "asc";
    } else {
      direction = "asc";
    }

    setSortColumn(column);
    setSortDirection(direction);

    const sorted = [...jobs].sort((a, b) => {
      const x = (a[column] || "").toLowerCase();
      const y = (b[column] || "").toLowerCase();
      if (x < y) return direction === "asc" ? -1 : 1;
      if (x > y) return direction === "asc" ? 1 : -1;
      return 0;
    });

    setJobs(sorted);
  }

  function header(label, column) {
    return (
      <th onClick={() => sortBy(column)} style={{ cursor: "pointer" }}>
        {label} {sortColumn === column ? (sortDirection === "asc" ? "▲" : "▼") : ""}
      </th>
    );
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Conservative Jobs Board</h1>

      <table border="1" cellPadding="8" cellSpacing="0" width="100%">
        <thead>
          <tr>
            {header("Title", "title")}
            {header("Company", "company")}
            {header("Location", "location")}
            {header("Type", "type")}
            {header("Link", "url")}
          </tr>
        </thead>
        <tbody>
          {jobs.map((job, i) => (
            <tr key={i}>
              <td>{job.title}</td>
              <td>{job.company}</td>
              <td>{job.location || ""}</td>
              <td>{job.type || ""}</td>
              <td>
                <a href={job.url} target="_blank" rel="noopener noreferrer">
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

