import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [sortConfig, setSortConfig] = useState({
    key: "organization",
    direction: "asc",
  });

  // ALL JOB SOURCES (NOW INCLUDING AMPRINPROJ)
  const sources = [
    "/jobs_talentmarket.json",
    "/jobs_yaf.json",
    "/jobs_afpi.json",
    "/jobs_hudson.json",
    "/jobs_cato.json",
    "/jobs_plf.json",
    "/jobs_ntu.json",
    "/jobs_acton.json",
    "/jobs_aier.json",
    "/jobs_excelined.json",
    "/jobs_claremont.json",
    "/jobs_heritage.json",
    "/jobs_cei.json",
    "/jobs_tppf.json",
    "/jobs_leadership_institute.json",
    "/jobs_crc.json",
    "/jobs_alec.json",
    "/jobs_acc.json",
    "/jobs_amprinproj.json"   // ⭐ NEW — AMERICAN PRINCIPLES PROJECT
  ];

  useEffect(() => {
    async function loadJobs() {
      const collected = [];

      for (const src of sources) {
        try {
          const res = await fetch(src);
          if (!res.ok) continue;
          const data = await res.json();

          for (const job of data) {
            collected.push({
              title: job.title || "N/A",
              organization:
                job.organization ||
                job.company ||
                "N/A",
              location: job.location || "N/A",
              link: job.link || job.url || "#",
              type: job.type || "N/A",
            });
          }
        } catch (err) {
          console.error("Error loading", src, err);
        }
      }

      setJobs(collected);
    }

    loadJobs();
  }, []);

  function sortBy(key) {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  }

  const sortedJobs = [...jobs].sort((a, b) => {
    const x = a[sortConfig.key] || "";
    const y = b[sortConfig.key] || "";
    return sortConfig.direction === "asc"
      ? x.localeCompare(y)
      : y.localeCompare(x);
  });

  return (
    <div className="App">
      <h1>Conservative Jobs Board</h1>

      <table>
        <thead>
          <tr>
            <th onClick={() => sortBy("organization")}>Organization</th>
            <th onClick={() => sortBy("title")}>Title</th>
            <th onClick={() => sortBy("location")}>Location</th>
            <th onClick={() => sortBy("type")}>Type</th>
            <th>Link</th>
          </tr>
        </thead>

        <tbody>
          {sortedJobs.map((job, index) => (
            <tr key={index}>
              <td>{job.organization}</td>
              <td>{job.title}</td>
              <td>{job.location}</td>
              <td>{job.type}</td>
              <td>
                <a href={job.link} target="_blank" rel="noopener noreferrer">
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

