import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    async function loadJobs() {
      const files = [
        "/jobs.json",
        "/jobs_yaf.json",
        "/jobs_talentmarket.json",
        "/jobs_afpi.json",
        "/jobs_cei.json",
        "/jobs_claremont.json",
        "/jobs_leadership_institute.json",
        "/jobs_tppf.json"
      ];

      let allJobs = [];

      for (const file of files) {
        try {
          const res = await fetch(file);
          if (!res.ok) continue;
          const data = await res.json();
          allJobs = allJobs.concat(data);
        } catch (e) {
          console.error("Error loading", file, e);
        }
      }

      // Sort with newest first IF date exists, otherwise push to bottom
      allJobs.sort((a, b) => {
        const da = new Date(a.date_posted || "2000-01-01");
        const db = new Date(b.date_posted || "2000-01-01");
        return db - da;
      });

      setJobs(allJobs);
    }

    loadJobs();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Conservative Jobs Board</h1>

      <div className="grid grid-cols-1 gap-4">
        {jobs.map((job, index) => (
          <a
            key={index}
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className="border p-4 rounded shadow hover:bg-gray-100"
          >
            <h2 className="text-xl font-bold">{job.title}</h2>
            <p className="text-gray-700">{job.organization}</p>
            <p className="text-gray-700">{job.location || "N/A"}</p>
            <p className="text-gray-700">{job.type || "N/A"}</p>
            {job.date_posted && (
              <p className="text-gray-500 text-sm">{job.date_posted}</p>
            )}
          </a>
        ))}
      </div>
    </div>
  );
}

export default App;

