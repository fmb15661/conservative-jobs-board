import React, { useEffect, useState } from "react";

function App() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadJobs() {
      const files = [
        "/jobs.json",
        "/jobs_talentmarket.json",
        "/jobs_yaf.json",
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
        } catch (err) {
          console.error("Error loading", file, err);
        }
      }

      setJobs(allJobs);
    }

    loadJobs();
  }, []);

  const filteredJobs = jobs.filter((job) => {
    const text =
      `${job.title} ${job.organization} ${job.location} ${job.type}`.toLowerCase();
    return text.includes(search.toLowerCase());
  });

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Conservative Jobs Board</h1>

      <input
        type="text"
        placeholder="Search jobs..."
        className="border p-2 mb-4 w-full rounded"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="grid grid-cols-1 gap-4">
        {filteredJobs.map((job, index) => (
          <a
            key={index}
            href={job.link}
            target="_blank"
            rel="noopener noreferrer"
            className="border p-4 rounded shadow hover:bg-gray-100"
          >
            <h2 className="text-xl font-bold text-blue-700 underline">
              {job.title}
            </h2>

            <p className="text-gray-700 font-semibold">
              {job.organization}
            </p>

            <p className="text-gray-700">
              {job.location || "N/A"}
            </p>

            <p className="text-gray-700">
              {job.type || "N/A"}
            </p>
          </a>
        ))}
      </div>
    </div>
  );
}

export default App;

