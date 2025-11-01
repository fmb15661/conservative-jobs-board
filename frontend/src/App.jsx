import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    async function fetchJobs() {
      try {
        const res1 = await fetch("/jobs.json");
        const baseJobs = await res1.json();

        const res2 = await fetch("/jobs_talentmarket.json");
        const tmJobs = await res2.json();

        let all = [...baseJobs, ...tmJobs];

        all = all.map((j) => ({
          title: j.title || "View Job",
          organization: j.organization || "N/A",
          location: j.location || "N/A",
          type: j.type || "N/A",
          link: j.link || "#",
          date_posted: j.date_posted
            ? new Date(j.date_posted).toISOString()
            : new Date("1970-01-01").toISOString(),
        }));

        all.sort((a, b) => new Date(b.date_posted) - new Date(a.date_posted));

        setJobs(all);
      } catch (err) {
        console.error("ERROR loading jobs", err);
      }
    }

    fetchJobs();
  }, []);

  return (
    <div style={{ padding: 30, maxWidth: 1000, margin: "0 auto" }}>
      <h1 style={{ fontSize: 32, fontWeight: "bold", marginBottom: 20 }}>
        Conservative Jobs Board
      </h1>

      <table border="1" cellPadding="8" cellSpacing="0" width="100%">
        <thead>
          <tr style={{ background: "#ccc" }}>
            <th>Job Title</th>
            <th>Org</th>
            <th>Location</th>
            <th>Type</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job, i) => (
            <tr key={i}>
              <td>
                <a href={job.link} target="_blank" rel="noreferrer">
                  {job.title}
                </a>
              </td>
              <td>{job.organization}</td>
              <td>{job.location}</td>
              <td>{job.type}</td>
              <td>{job.date_posted.split("T")[0]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

